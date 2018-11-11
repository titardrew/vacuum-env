if __name__ == '__main__':
    env = VacuumEnv(size=8, max_episodes=100, gen_proba=0.5, collide='sym')

    env.reset()
    info = None
    while not env.done:
        sleep(0.1)
        env.render()
        obs, r, _, info = env.step()
        if not done:
            assert r == 0

    assert r < 0
    print(info['garbage_count'])

