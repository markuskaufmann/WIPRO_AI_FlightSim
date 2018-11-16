import argparse

import numpy as np
# import gym
import tensorflow as tf

from ch.hslu.wipro.ddpg.FlightGearEnv import FlightGearEnv
from ch.hslu.wipro.ddpg.new import ddpg, logger


#_game_envs = defaultdict(set)
#for env in gym.envs.registry.all():
#    # TODO: solve this with regexes
#    env_type = env._entry_point.split(':')[0].split('.')[-1]
#    #_game_envs[env_type].add(env.id)

# reading benchmark names directly from retro requires
# importing retro here, and for some reason that crashes tensorflow
# in ubuntu
#_game_envs['retro'] = {
#    'SuperMarioBros-Nes',
#    'TwinBee3PokoPokoDaimaou-Nes',
#    'SpaceHarrier-Nes',
#    'SonicTheHedgehog-Genesis',
#    'Vectorman-Genesis',
#    'FinalFight-Snes',
#    'SpaceInvaders-Snes',
#}
#
from ch.hslu.wipro.ddpg.new.common import tf_util


def train(args, extra_args):
    total_timesteps = 100000
    seed = args['random_seed']


    alg_kwargs = {}

    env = FlightGearEnv()
    np.random.seed(int(args['random_seed']))
    tf.set_random_seed(int(args['random_seed']))
    env.seed(int(args['random_seed']))

    #if args.save_video_interval != 0:
    #    env = VecVideoRecorder(env, osp.join(logger.Logger.CURRENT.dir, "videos"), record_video_trigger=lambda x: x % args.save_video_interval == 0, video_length=args.save_video_length)
    alg_kwargs['network'] = 'mlp'
    #if args.network:
    #    alg_kwargs['network'] = args.network
    #else:
    #    if alg_kwargs.get('network') is None:
    #        alg_kwargs['network'] = get_default_network(env_type)
    learn = ddpg.learn

    model = learn(
        env=env,
        seed=seed,
        total_timesteps=total_timesteps,
        **alg_kwargs
    )

    return model, env


#def build_env(args):
#    ncpu = multiprocessing.cpu_count()
#    if sys.platform == 'darwin': ncpu //= 2
#    nenv = args.num_env or ncpu
#    alg = args.alg
#    seed = args.seed
#
#    env_type, env_id = get_env_type(args.env)
#
#    #if env_type in {'atari', 'retro'}:
#    #    if alg == 'deepq':
#    #        env = make_env(env_id, env_type, seed=seed, wrapper_kwargs={'frame_stack': True})
#    #    elif alg == 'trpo_mpi':
#    #        env = make_env(env_id, env_type, seed=seed)
#    #    else:
#    #        frame_stack_size = 4
#    #        env = make_vec_env(env_id, env_type, nenv, seed, gamestate=args.gamestate, reward_scale=args.reward_scale)
#    #        env = VecFrameStack(env, frame_stack_size)
##
#    #else:
#    config = tf.ConfigProto(allow_soft_placement=True,
#                            intra_op_parallelism_threads=1,
#                         inter_op_parallelism_threads=1)
#    config.gpu_options.allow_growth = True
#    get_session(config=config)
#    env = make_vec_env(env_id, env_type, args.num_env or 1, seed, reward_scale=args.reward_scale)
#    if env_type == 'mujoco':
#        env = VecNormalize(env)
#
#    return env


#def get_env_type(env_id):
#    if env_id in _game_envs.keys():
#        env_type = env_id
#        env_id = [g for g in _game_envs[env_type]][0]
#    else:
#        env_type = None
#        for g, e in _game_envs.items():
#            if env_id in e:
#                env_type = g
#                break
#        assert env_type is not None, 'env_id {} is not recognized in env types'.format(env_id, _game_envs.keys())
#
#    return env_type, env_id


#def get_default_network(env_type):
#    if env_type in {'atari', 'retro'}:
#        return 'cnn'
#    else:
#        return 'mlp'#

#def get_alg_module(#, submodule=None):
#    submodule = submodule or alg
#    try:
#        # first try to import the alg module from baselines
#        alg_module = import_module('.'.join(['baselines', alg, submodule]))
#    except ImportError:
#        # then from rl_algs
#        alg_module = import_module('.'.join(['rl_' + 'algs', alg, submodule]))
#
#    return alg_module


def get_learn_function(alg):
    return ddpg.learn


#def get_learn_function_defaults(alg, env_type):
#    try:
#        alg_defaults = #(alg, 'defaults')
#        kwargs = getattr(alg_defaults, env_type)()
#    except (ImportError, AttributeError):
#        kwargs = {}
#    return kwargs



#def parse_cmdline_kwargs(args):
#    '''
#    convert a list of '='-spaced command-line arguments to a dictionary, evaluating python objects when possible
#    '''
#    def parse(v):
#
#        assert isinstance(v, str)
#        try:
#            return eval(v)
#        except (NameError, SyntaxError):
#            return v
#
#    return {k: parse(v) for k,v in #(args).items()}
#


def start_reinforcement_learning():
    # configure logger, disable logging in child MPI processes (with rank > 0)

    parser = argparse.ArgumentParser(description='provide arguments for DDPG agent')

    # agent parameters
    parser.add_argument('--actor-lr', help='actor network learning rate', default=0.00001)
    parser.add_argument('--critic-lr', help='critic network learning rate', default=0.0001)
    parser.add_argument('--gamma', help='discount factor for critic updates', default=0.95)
    parser.add_argument('--tau', help='soft target update parameter', default=0.001)
    parser.add_argument('--buffer-size', help='max size of the replay buffer', default=2000000)
    parser.add_argument('--minibatch-size', help='size of minibatch for minibatch-SGD', default=254)

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

    train(args, None)


def start_with_existing_network(filename):
    # logger.log("Loading trained model")
    # env = FlightGearEnv()
    # obs = env.reset()
    #
    # tf_util.load_variables(filename)
    #
    # def initialize_placeholders(nlstm=128, **kwargs):
    #     return np.zeros((args.num_env or 1, 2 * nlstm)), np.zeros((1))
    #
    # state, dones = initialize_placeholders(**extra_args)
    # while True:
    #     actions, _, state, _ = model.step(obs, S=state, M=dones)
    #     obs, _, done, _ = env.step(actions)
    #     env.render()
    #     done = done.any() if isinstance(done, np.ndarray) else done
    #
    #     if done:
    #         obs = env.reset()
    #
    # env.close()
    pass
