from gym.envs.registration import register
from gym.envs.registration import spec

register(
    id='DrivingEnv-v0',
    entry_point='gym_driving.envs:DrivingEnv',
    kwargs={'wrapper_config.TimeLimit.max_episode_steps': 100},
)

register(
    id='SupervisorDrivingEnv-v0',
    entry_point='gym_driving.envs:SupervisorDrivingEnv',
    kwargs={'wrapper_config.TimeLimit.max_episode_steps': 100},
)

# print("SPEC", spec('DrivingEnv-v0'))