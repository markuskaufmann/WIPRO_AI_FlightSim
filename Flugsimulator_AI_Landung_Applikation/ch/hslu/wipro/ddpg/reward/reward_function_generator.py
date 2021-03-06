from ch.hslu.wipro.ddpg.reward.damage_penalty import DamagePenalty
from ch.hslu.wipro.ddpg.reward.landing_reward import LandingReward
from ch.hslu.wipro.ddpg.reward.position_discrepancy_reset_penalty import PositionDiscrepancyResetPenalty
from ch.hslu.wipro.ddpg.reward.position_on_ground_pitch_reward import PositionOnGroundPitchReward
from ch.hslu.wipro.ddpg.reward.position_over_ground_airspeed_reward import PositionOverGroundAirspeedReward
from ch.hslu.wipro.ddpg.reward.position_over_ground_pitch_reward import PositionOverGroundPitchReward
from ch.hslu.wipro.ddpg.reward.position_runway_reward import PositionRunwayReward
from ch.hslu.wipro.ddpg.reward.reward_function import RewardFunction
from ch.hslu.wipro.ddpg.reward.touchdown_reward import TouchdownReward


def generate_checkpoint2_reward_function():
    reward_function = RewardFunction(
        [DamagePenalty(), PositionDiscrepancyResetPenalty(), PositionRunwayReward(),
         PositionOverGroundPitchReward(), PositionOverGroundAirspeedReward(),
         TouchdownReward(), LandingReward(), PositionOnGroundPitchReward()])

    return reward_function
