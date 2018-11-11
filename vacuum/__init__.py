from gym.envs.registration import register

register(
    id='VacuumEnv-v1',
    entry_point='vacuum.vacuum:VacuumEnv',
)
