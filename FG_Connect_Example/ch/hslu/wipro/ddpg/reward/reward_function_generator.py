from ch.hslu.wipro.ddpg.reward.position_rewards import PositionRewards
from ch.hslu.wipro.ddpg.reward.reward_function import RewardFunction


def generate_checkpoint2_reward_function():
    reward_function = RewardFunction([PositionRewards()])
    return reward_function


