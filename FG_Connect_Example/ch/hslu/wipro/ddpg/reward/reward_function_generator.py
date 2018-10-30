from ch.hslu.wipro.ddpg.reward.damage_rewards import DamageRewards
from ch.hslu.wipro.ddpg.reward.landing_reward import LandingReward
from ch.hslu.wipro.ddpg.reward.position_rewards import PositionRewards
from ch.hslu.wipro.ddpg.reward.reward_function import RewardFunction
from ch.hslu.wipro.ddpg.reward.touchdown_reward import TouchdownReward


def generate_checkpoint2_reward_function():
    reward_function = RewardFunction([DamageRewards(), LandingReward(), TouchdownReward(), PositionRewards()])
    return reward_function


