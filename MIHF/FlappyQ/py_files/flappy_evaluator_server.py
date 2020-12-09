from homework.flappy_agent import FlappyAgent
from flappy_env_server import Environment

n_iterations = int(2e5)
iteration = 0
epoch = 0

print_epoch_interval = 500

env = Environment()
agent = FlappyAgent(observation_space_size=env.observation_space_size,
                    action_space=env.action_space,
                    n_iterations=n_iterations)

while iteration < n_iterations:
    state = env.reset()

    epoch_iteration, epoch_reward_sum = 0, 0
    done = False

    while not done:
        action = agent.step(state)

        assert action in env.action_space, \
            "Invalid action! Expected would be some of {}; given: {}"\
                .format(env.action_space, action)

        next_state, reward, done, info = env.step(action)
        agent.learn(state, action, next_state, reward)

        state = next_state

        epoch_iteration += 1
        epoch_reward_sum += reward
        
        iteration += 1

    agent.epoch_end(epoch_reward_sum)

    epoch += 1

agent.train_end()

n_max_reward = 25
test_iteration = 0
reward_sum = 0

done = False
state = env.reset()

while not done and reward_sum < n_max_reward:
    action = agent.step(state)
    state, reward, done, _ = env.step(action)

    assert action in env.action_space, \
        "Invalid action! Expected would be some of {}; given: {}" \
            .format(env.action_space, action)

    reward_sum += reward
    test_iteration += 1

del agent
print()
print(int(reward_sum), end='')


