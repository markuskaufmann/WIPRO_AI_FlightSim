"""
################################################################
FILE FROM OPEN AI BASELINES https://github.com/openai/baselines
################################################################
"""

import datetime
import os
import pickle
import time
from collections import deque

import numpy as np

import ch.hslu.wipro.ddpg.algorithm.common.tf_util as U
from ch.hslu.wipro.ddpg.algorithm import logger
from ch.hslu.wipro.ddpg.algorithm.common import set_global_seeds
from ch.hslu.wipro.ddpg.algorithm.ddpg_fg_restart_observer import DDPGFGRestartObserver
from ch.hslu.wipro.ddpg.algorithm.ddpg_learner import DDPG
from ch.hslu.wipro.ddpg.algorithm.memory import Memory
from ch.hslu.wipro.ddpg.algorithm.models import Actor, Critic
from ch.hslu.wipro.ddpg.algorithm.noise import AdaptiveParamNoiseSpec, NormalActionNoise, OrnsteinUhlenbeckActionNoise
from ch.hslu.wipro.fg.main.fg_broker_restart import FGRestartBroker
from ch.hslu.wipro.fg.main.fg_start_stop import FGStartStop

try:
    from mpi4py import MPI
except ImportError:
    MPI = None


def learn(network, env,
          seed=None,
          total_timesteps=None,
          nb_epochs=1000000,  # with default settings, perform 1M steps total
          nb_epoch_cycles=40,
          nb_rollout_steps=60,
          reward_scale=1.0,
          render=False,
          render_eval=False,
          noise_type='adaptive-param_0.5',
          normalize_returns=False,
          normalize_observations=True,
          critic_l2_reg=1e-2,
          actor_lr=1e-5,
          critic_lr=1e-4,
          popart=False,
          gamma=0.99,
          clip_norm=None,
          nb_train_steps=50,  # per epoch cycle and MPI worker,
          nb_eval_steps=100,
          batch_size=64,  # per MPI worker
          tau=0.01,
          eval_env=None,
          param_noise_adaption_interval=50,
          load_path=None,
          save_path=None,
          **network_kwargs):
    set_global_seeds(seed)

    if total_timesteps is not None:
        assert nb_epochs is None
        nb_epochs = int(total_timesteps) // (nb_epoch_cycles * nb_rollout_steps)

    if MPI is not None:
        rank = MPI.COMM_WORLD.Get_rank()
    else:
        rank = 0

    sp = env.action_space
    nb_actions = env.action_space.shape[-1]
    assert (np.abs(env.action_space.low) == env.action_space.high).all()  # we assume symmetric actions.

    memory = Memory(limit=int(1e6), action_shape=env.action_space.shape, observation_shape=env.observation_space.shape)
    critic = Critic(network=network, **network_kwargs)
    actor = Actor(nb_actions, network=network, **network_kwargs)

    action_noise = None
    param_noise = None
    if noise_type is not None:
        for current_noise_type in noise_type.split(','):
            current_noise_type = current_noise_type.strip()
            if current_noise_type == 'none':
                pass
            elif 'adaptive-param' in current_noise_type:
                _, stddev = current_noise_type.split('_')
                param_noise = AdaptiveParamNoiseSpec(initial_stddev=float(stddev), desired_action_stddev=float(stddev))
            elif 'normal' in current_noise_type:
                _, stddev = current_noise_type.split('_')
                action_noise = NormalActionNoise(mu=np.zeros(nb_actions), sigma=float(stddev) * np.ones(nb_actions))
            elif 'ou' in current_noise_type:
                _, stddev = current_noise_type.split('_')
                action_noise = OrnsteinUhlenbeckActionNoise(mu=np.zeros(nb_actions),
                                                            sigma=float(stddev) * np.ones(nb_actions))
            else:
                raise RuntimeError('unknown noise type "{}"'.format(current_noise_type))

    max_action = env.action_space.high
    logger.info('scaling actions by {} before executing in env'.format(max_action))

    agent = DDPG(actor, critic, memory, env.observation_space.shape, env.action_space.shape,
                 gamma=gamma, tau=tau, normalize_returns=normalize_returns,
                 normalize_observations=normalize_observations,
                 batch_size=batch_size, action_noise=action_noise, param_noise=param_noise, critic_l2_reg=critic_l2_reg,
                 actor_lr=actor_lr, critic_lr=critic_lr, enable_popart=popart, clip_norm=clip_norm,
                 reward_scale=reward_scale)

    logger.info('Using agent with the following configuration:')
    logger.info(str(agent.__dict__.items()))

    eval_episode_rewards_history = deque(maxlen=100)
    episode_rewards_history = deque(maxlen=100)
    sess = U.get_session()
    # Prepare everything.
    agent.initialize(sess)

    if load_path is not None:
        U.load_variables(load_path)
        logger.log('Loaded model from {}'.format(load_path))

    sess.graph.finalize()

    agent.reset()

    obs = env.reset()
    if eval_env is not None:
        eval_obs = eval_env.reset()

    episode_reward = 0  # vector
    episode_step = 0  # vector
    episodes = 0  # scalar
    t = 0  # scalar

    epoch = 0

    start_time = time.time()

    epoch_episode_rewards = []
    epoch_episode_steps = []
    epoch_actions = []
    epoch_qs = []
    epoch_episodes = 0
    first_epoch = True
    fg_restart_count = 0

    for epoch in range(nb_epochs):
        print("Epoch {0} of {1}".format(epoch, nb_epochs))
        if not first_epoch and epoch % 10 == 0:
            fg_restart_count += 1
            observer = restart_fg(epoch, fg_restart_count)
            while not observer.ready:
                time.sleep(0.05)
        first_epoch = False

        for cycle in range(nb_epoch_cycles):
            obs = env.reset()
            # Perform rollouts.
            for t_rollout in range(nb_rollout_steps):
                # Predict next action.
                action, q, _, _ = agent.step(obs, apply_noise=True, compute_Q=True)

                # Execute next action.
                if rank == 0 and render:
                    env.render()

                # max_action is of dimension A, whereas action is dimension (nenvs, A) - the multiplication gets broadcasted to the batch
                new_obs, r, done, info = env.step(
                    max_action * action)  # scale for execution in env (as far as DDPG is concerned, every action is in [-1, 1])
                # note these outputs are batched from vecenv
                print("Epoch: {0} || Cycle: {1} || Step: {2} || &&&&&&&&&&&&&=>> Reward: {3}".format(epoch, cycle, t_rollout, r))
                print("############################################################")
                t += 1
                episode_reward += r
                episode_step += 1

                # Book-keeping.
                epoch_actions.append(action)
                epoch_qs.append(q)
                agent.store_transition(obs, action, r, new_obs,
                                       done)  # the batched data will be unrolled in memory.py's append.

                obs = new_obs

                if done:
                    # Episode done.
                    epoch_episode_rewards.append(episode_reward)
                    episode_rewards_history.append(episode_reward)
                    epoch_episode_steps.append(episode_step)
                    episode_reward = 0.
                    episode_step = 0
                    epoch_episodes += 1
                    episodes += 1
                    agent.reset()
                    break

            # Train.
            epoch_actor_losses = []
            epoch_critic_losses = []
            epoch_adaptive_distances = []
            for t_train in range(nb_train_steps):
                # Adapt param noise, if necessary.
                if memory.nb_entries >= batch_size and t_train % param_noise_adaption_interval == 0:
                    distance = agent.adapt_param_noise()
                    epoch_adaptive_distances.append(distance)

                cl, al = agent.train()
                epoch_critic_losses.append(cl)
                epoch_actor_losses.append(al)
                agent.update_target_net()

            # Evaluate.
            eval_episode_rewards = []
            eval_qs = []
            if eval_env is not None:
                nenvs_eval = eval_obs.shape[0]
                eval_episode_reward = np.zeros(nenvs_eval, dtype=np.float32)
                for t_rollout in range(nb_eval_steps):
                    eval_action, eval_q, _, _ = agent.step(eval_obs, apply_noise=False, compute_Q=True)
                    eval_obs, eval_r, eval_done, eval_info = eval_env.step(
                        max_action * eval_action)  # scale for execution in env (as far as DDPG is concerned, every action is in [-1, 1])
                    if render_eval:
                        eval_env.render()
                    eval_episode_reward += eval_r

                    eval_qs.append(eval_q)
                    for d in range(len(eval_done)):
                        if eval_done[d]:
                            eval_episode_rewards.append(eval_episode_reward[d])
                            eval_episode_rewards_history.append(eval_episode_reward[d])
                            eval_episode_reward[d] = 0.0

        filename = "network_ep" + str(epoch) + "_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M") + ".pkl"
        U.save_variables(save_path + filename)

        if MPI is not None:
            mpi_size = MPI.COMM_WORLD.Get_size()
        else:
            mpi_size = 1

        # Log stats.
        # XXX shouldn't call np.mean on variable length lists
        duration = time.time() - start_time
        stats = agent.get_stats()
        combined_stats = stats.copy()
        combined_stats['rollout/return'] = np.mean(epoch_episode_rewards)
        combined_stats['rollout/return_history'] = np.mean(episode_rewards_history)
        combined_stats['rollout/episode_steps'] = np.mean(epoch_episode_steps)
        combined_stats['rollout/actions_mean'] = np.mean(epoch_actions)
        combined_stats['rollout/Q_mean'] = np.mean(epoch_qs)
        combined_stats['train/loss_actor'] = np.mean(epoch_actor_losses)
        combined_stats['train/loss_critic'] = np.mean(epoch_critic_losses)
        combined_stats['train/param_noise_distance'] = np.mean(epoch_adaptive_distances)
        combined_stats['total/duration'] = duration
        combined_stats['total/steps_per_second'] = float(t) / float(duration)
        combined_stats['total/episodes'] = episodes
        combined_stats['rollout/episodes'] = epoch_episodes
        combined_stats['rollout/actions_std'] = np.std(epoch_actions)
        # Evaluation statistics.
        if eval_env is not None:
            combined_stats['eval/return'] = eval_episode_rewards
            combined_stats['eval/return_history'] = np.mean(eval_episode_rewards_history)
            combined_stats['eval/Q'] = eval_qs
            combined_stats['eval/episodes'] = len(eval_episode_rewards)

        def as_scalar(x):
            if isinstance(x, np.ndarray):
                assert x.size == 1
                return x[0]
            elif np.isscalar(x):
                return x
            else:
                raise ValueError('expected scalar, got %s' % x)

        combined_stats_sums = np.array([np.array(x).flatten()[0] for x in combined_stats.values()])
        if MPI is not None:
            combined_stats_sums = MPI.COMM_WORLD.allreduce(combined_stats_sums)

        combined_stats = {k: v / mpi_size for (k, v) in zip(combined_stats.keys(), combined_stats_sums)}

        # Total statistics.
        combined_stats['total/epochs'] = epoch + 1
        combined_stats['total/steps'] = t

        for key in sorted(combined_stats.keys()):
            logger.record_tabular(key, combined_stats[key])

        if rank == 0:
            logger.dump_tabular()
        logger.info('')

        logdir = logger.get_dir()
        if rank == 0 and logdir:
            if hasattr(env, 'get_state'):
                with open(os.path.join(logdir, 'env_state.pkl'), 'wb') as f:
                    pickle.dump(env.get_state(), f)
            if eval_env and hasattr(eval_env, 'get_state'):
                with open(os.path.join(logdir, 'eval_env_state.pkl'), 'wb') as f:
                    pickle.dump(eval_env.get_state(), f)

    return agent


def restart_fg(epoch: int, fg_restart_count: int) -> DDPGFGRestartObserver:
    observer = DDPGFGRestartObserver()
    FGRestartBroker(observers=[observer],
                    start_delegate=FGStartStop.start_fg,
                    stop_delegate=FGStartStop.stop_fg,
                    log_file_suffix="ep_{0}_rst_{1}".format(epoch, fg_restart_count)).request_fg_restart()
    return observer
