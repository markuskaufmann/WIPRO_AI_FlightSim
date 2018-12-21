import argparse

import numpy as np
# import gym
import tensorflow as tf
import datetime

from ch.hslu.wipro.ddpg.FlightGearEnv import FlightGearEnv
from ch.hslu.wipro.ddpg.algorithm import ddpg, logger


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
from ch.hslu.wipro.ddpg.algorithm.common import tf_util

CURRENT_USER = "Cyrille"
LOG_PATH = "C:\\Users\\" + CURRENT_USER + "\\Documents\\FG_Logs_Graphs\\"

def train(args):
    seed = args['random_seed']
    alg_kwargs = {}

    env = FlightGearEnv()
    np.random.seed(int(args['random_seed']))
    tf.set_random_seed(int(args['random_seed']))
    env.seed(int(args['random_seed']))

    alg_kwargs['network'] = 'mlp'
    learn = ddpg.learn
    timestamp = datetime.datetime.now().strftime("openai-%Y-%m-%d-%H-%M-%S-%f")
    logger.configure(LOG_PATH + timestamp + "\\", ['log', 'tensorboard'])
    model = learn(
        env=env,
        seed=seed,
        save_path=LOG_PATH + timestamp + "\\Networks\\",
        # If you want to load an existing network for TRAINING, remove the following comment tag
        # load_path=LOG_PATH + "openai-2018-11-26-15-52-14-875708\\Networks\\network_ep119_2018_11_27_02_23.pkl",
        **alg_kwargs
    )

    return model, env


def play_result():
    learn = ddpg.learn
    env = FlightGearEnv()
    alg_kwargs = {}
    alg_kwargs['network'] = 'mlp'

    model = learn(
        env=env,
        nb_epochs=0,
        load_path=LOG_PATH + "demo\\2.pkl",
        **alg_kwargs
    )

    while True:
        obs, done = env.reset(), False
        episode_rew = 0
        while not done:
            for i in range(30):
                obs, rew, done, _ = env.step(model.step(obs[None], apply_noise=False)[0])
                episode_rew += rew

                if done:
                    break

def get_learn_function(alg):
    return ddpg.learn


def start_reinforcement_learning():
    # configure logger, disable logging in child MPI processes (with rank > 0)
    parser = argparse.ArgumentParser(description='provide arguments for DDPG agent')

    # Add seed for repeatability
    parser.add_argument('--random_seed', help='random seed for repeatability', default=1234)

    args = vars(parser.parse_args())

    train(args)
