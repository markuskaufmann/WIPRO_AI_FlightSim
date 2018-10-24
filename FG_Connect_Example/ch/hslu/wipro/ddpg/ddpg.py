"""
Implementation of DDPG - Deep Deterministic Policy Gradient

Algorithm and hyperparameter details can be found here:
    http://arxiv.org/pdf/1509.02971v2.pdf

The algorithm is tested on the Pendulum-v0 OpenAI gym task
and developed with tflearn + Tensorflow

Author: Patrick Emami
"""
import argparse
import pprint as pp

import numpy as np
import tensorflow as tf

from ch.hslu.wipro.ddpg.FlightGearEnv import FlightGearEnv
from ch.hslu.wipro.ddpg.networks.ActorNetwork import ActorNetwork
from ch.hslu.wipro.ddpg.networks.CriticNetwork import CriticNetwork
from ch.hslu.wipro.ddpg.utility.OrnsteinUhlenbeckActionNoise import OrnsteinUhlenbeckActionNoise
from ch.hslu.wipro.ddpg.utility.replay_buffer import ReplayBuffer


# ==========================
#   Tensorflow Summary Ops
# ===========================

def build_summaries():
    episode_reward = tf.Variable(0.)
    tf.summary.scalar("Reward", episode_reward)
    episode_ave_max_q = tf.Variable(0.)
    tf.summary.scalar("Qmax Value", episode_ave_max_q)

    summary_vars = [episode_reward, episode_ave_max_q]
    summary_ops = tf.summary.merge_all()

    return summary_ops, summary_vars


# ===========================
#   Agent Training
# ===========================

def train(sess, env, args, actor, critic, actor_noise):
    # Set up summary Ops
    summary_ops, summary_vars = build_summaries()

    sess.run(tf.global_variables_initializer())
    writer = tf.summary.FileWriter(args['summary_dir'], sess.graph)

    # Initialize target network weights
    actor.update_target_network()
    critic.update_target_network()

    # Initialize replay memory
    replay_buffer = ReplayBuffer(int(args['buffer_size']), int(args['random_seed']))

    # Needed to enable BatchNorm.
    # This hurts the performance on Pendulum but could be useful
    # in other environments.
    # tflearn.is_training(True)

    for i in range(int(args['max_episodes'])):

        s = env.reset()

        print("environment reseted")

        ep_reward = 0
        ep_ave_max_q = 0

        for j in range(5+(int(i/30))):
            # Added exploration noise

            # TODO: Predict has to return a dictionary with the action!
            a = actor.predict(np.reshape(s, (1, actor.s_dim))) + actor_noise()

            s2, r, terminal, info = env.step(a[0])

            replay_buffer.add(np.reshape(s, (actor.s_dim,)), np.reshape(a, (actor.a_dim,)), r,
                              terminal, np.reshape(s2, (actor.s_dim,)))

            # Keep adding experience to the memory until
            # there are at least minibatch size samples
            if replay_buffer.size() > int(args['minibatch_size']):
                s_batch, a_batch, r_batch, t_batch, s2_batch = \
                    replay_buffer.sample_batch(int(args['minibatch_size']))

                # Calculate targets
                target_q = critic.predict_target(
                    s2_batch, actor.predict_target(s2_batch))

                y_i = []
                for k in range(int(args['minibatch_size'])):
                    if t_batch[k]:
                        y_i.append(r_batch[k])
                    else:
                        y_i.append(r_batch[k] + critic.gamma * target_q[k])

                # Update the critic given the targets
                predicted_q_value, _ = critic.train(
                    s_batch, a_batch, np.reshape(y_i, (int(args['minibatch_size']), 1)))

                ep_ave_max_q += np.amax(predicted_q_value)

                # Update the actor policy using the sampled gradient
                a_outs = actor.predict(s_batch)
                grads = critic.action_gradients(s_batch, a_outs)
                actor.train(s_batch, grads[0])

                # Update target networks (not updating the networks directly so the alg is more stable
                actor.update_target_network()
                critic.update_target_network()

            s = s2
            ep_reward = r

            summary_str = sess.run(summary_ops, feed_dict={
                summary_vars[0]: ep_reward,
                summary_vars[1]: ep_ave_max_q / float(j+1)
            })

            writer.add_summary(summary_str, i)
            writer.flush()

            print('| Reward: {:d} | Episode: {:d} | Qmax: {:.4f}'.format(int(ep_reward), j,
                                                                         (ep_ave_max_q / float(j+1))))

            if terminal:
                break


def _start_learning(args):
    with tf.Session() as sess:

        env = FlightGearEnv()
        np.random.seed(int(args['random_seed']))
        tf.set_random_seed(int(args['random_seed']))
        env.seed(int(args['random_seed']))

        state_dim = len(env.observation_space.spaces)
        action_dim = len(env.action_space.spaces)

        # TODO: Check for problems
        action_bound = 1

        # Ensure action bound is symmetric TODO: Check if has to be symmetric
        # assert (env.action_space.high == -env.action_space.low)

        actor = ActorNetwork(sess, state_dim, action_dim, action_bound,
                             float(args['actor_lr']), float(args['tau']),
                             int(args['minibatch_size']))

        critic = CriticNetwork(sess, state_dim, action_dim,
                               float(args['critic_lr']), float(args['tau']),
                               float(args['gamma']),
                               actor.get_num_trainable_vars())

        actor_noise = OrnsteinUhlenbeckActionNoise(mu=np.zeros(action_dim))

        #if args['use_gym_monitor']:
        #    if not args['render_env']:
        #        env = wrappers.Monitor(
        #            env, args['monitor_dir'], video_callable=False, force=True)
        #    else:

        #        env = wrappers.Monitor(env, args['monitor_dir'], force=True)

        train(sess, env, args, actor, critic, actor_noise)

        #if args['use_gym_monitor']:
        #    env.monitor.close()


# if __name__ == '__main__':
def start_reinforcement_learning():
    parser = argparse.ArgumentParser(description='provide arguments for DDPG agent')

    # agent parameters
    parser.add_argument('--actor-lr', help='actor network learning rate', default=0.0001)
    parser.add_argument('--critic-lr', help='critic network learning rate', default=0.001)
    parser.add_argument('--gamma', help='discount factor for critic updates', default=0.99)
    parser.add_argument('--tau', help='soft target update parameter', default=0.001)
    parser.add_argument('--buffer-size', help='max size of the replay buffer', default=1000000)
    parser.add_argument('--minibatch-size', help='size of minibatch for minibatch-SGD', default=64)

    # run parameters
    # parser.add_argument('--env', help='choose the gym env- tested on {Pendulum-v0}', default='Pendulum-v0')
    parser.add_argument('--random-seed', help='random seed for repeatability', default=1234)
    parser.add_argument('--max-episodes', help='max num of episodes to do while training', default=50000)
    parser.add_argument('--max_episode_len', help='max length of 1 episode', default=300)
    # parser.add_argument('--render-env', help='render the gym env', action='store_true')
    # parser.add_argument('--use-gym-monitor', help='record gym results', action='store_true')
    parser.add_argument('--monitor-dir', help='directory for storing gym results', default='./results/FG_ddpg')
    parser.add_argument('--summary-dir', help='directory for storing tensorboard info', default='./results/tf_ddpg')

    # parser.set_defaults(render_env=True)
    # parser.set_defaults(use_gym_monitor=False)

    args = vars(parser.parse_args())

    pp.pprint(args)

    _start_learning(args)


if __name__ == '__main__':
    start_reinforcement_learning()
