from ch.hslu.wipro.ddpg.reward.damage_rewards import DamageRewards
from ch.hslu.wipro.ddpg.reward.landing_reward import LandingReward
from ch.hslu.wipro.ddpg.reward.on_ground_rewards import OnGroundRewards
from ch.hslu.wipro.ddpg.reward.position_altitude_reward import PositionAltitudeReward
from ch.hslu.wipro.ddpg.reward.position_discrepancy_reset_reward import PositionDiscrepancyResetReward
from ch.hslu.wipro.ddpg.reward.position_in_air_pitch_reward import PositionInAirPitchReward
from ch.hslu.wipro.ddpg.reward.position_over_ground_airspeed_reward import PositionOverGroundAirspeedReward
from ch.hslu.wipro.ddpg.reward.position_over_ground_pitch_reward import PositionOverGroundPitchReward
from ch.hslu.wipro.ddpg.reward.position_runway_reward import PositionRunwayReward
from ch.hslu.wipro.ddpg.reward.reward_function import RewardFunction
from ch.hslu.wipro.ddpg.reward.touchdown_reward import TouchdownReward


def generate_checkpoint2_reward_function():
    reward_function = RewardFunction([DamageRewards(), PositionAltitudeReward(), PositionDiscrepancyResetReward(),
                                      PositionRunwayReward(), PositionInAirPitchReward(),
                                      PositionOverGroundAirspeedReward(), PositionOverGroundPitchReward(),
                                      LandingReward(), OnGroundRewards()]) #TouchdownReward()
    return reward_function
