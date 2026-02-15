import pygame
from pygame.locals import *
import random
import matplotlib.pyplot as plt

# Initialize
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 14)

# Make game window
screen = pygame.display.set_mode((1100, 600))

# Manually make the maze
matrix = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Board size
size = len(matrix)

# Agent position
agent_row, agent_col = size - 1, size - 1

# Q-thingy init
q_table = {}
q_val = 0

alpha = 0.1 # Learning Rate
gamma = 0.9 # Discount Factor
epsilon = 1.0 # Curiosity
decay_rate = 0.995

for i in range(size):
    for j in range(size):
        q_table[(i, j)] = {'up': 0.0, 'down': 0.0, 'left': 0.0, 'right': 0.0}

# Episode
episode = 1

# Record History
steps = []
current_step = 0

reward = []
q_sum = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((250, 250, 250))

    # Move logic
    move = ['up', 'down', 'left', 'right']
    direction = ''

    # Exploration
    if random.random() < epsilon:
        direction = random.choice(move)
    # Exploitation
    else:
        max_vals = max(q_table[(agent_row, agent_col)].values())
        max_keys = [key for key, value in q_table[(agent_row, agent_col)].items() if value == max_vals]
        direction = random.choice(max_keys)

    # Save previous position
    old_row, old_col = agent_row, agent_col

    # Update agent
    if direction == 'left':
        agent_col = max(0, agent_col - 1)
    elif direction == 'right':
        agent_col = min(size - 1, agent_col + 1)
    elif direction == 'up':
        agent_row = max(agent_row - 1, 0)
    elif direction == 'down':
        agent_row = min(agent_row + 1, size - 1)

    current_step += 1

    # Reward count
    # Lava
    if matrix[agent_row][agent_col] == 2:
        q_val = -1
    # End point
    elif matrix[agent_row][agent_col] == 1:
        q_val = 100
    # Path
    elif matrix[agent_row][agent_col] == 0:
        q_val = -0.1

    q_sum += q_val

    # Bellman Equation
    previous_state = (old_row, old_col)
    current_state = (agent_row, agent_col)

    if matrix[agent_row][agent_col] == 0:
        observed = q_val + gamma * max(q_table[current_state].values())
    else:
        observed = q_val

    # Temporal Difference Error
    expected = q_table[previous_state][direction]
    td_err = observed - expected

    # Update Q-Table
    q_table[previous_state][direction] = expected + alpha * td_err

    # Render board
    for i in range(size):
        for j in range(size // 2):
            if i % 2 == 0:
                first = 100
                second = 120
            else:
                first = 120
                second = 100
            # Checker 1
            pygame.draw.rect(screen, (238, 238, 238), pygame.Rect(first + (40 * j), 100 + 20 * i, 20, 20))
            # Checker 2
            pygame.draw.rect(screen, (220, 220, 220), pygame.Rect(second + (40 * j), 100 + 20 * i, 20, 20))
        
        for k in range(size):
            if matrix[i][k] == 2:
                # Obstacle
                pygame.draw.rect(screen, (250, 104, 104), pygame.Rect(100 + 20 * k, 100 + 20 * i, 20, 20))

    # Get max State-Value
    state_values = [max(actions.values()) for actions in q_table.values()]

    # Get global min and max
    global_min = min(state_values)
    global_max = max(state_values)

    # Render State-Value Heatmap
    for i in range(size):
        for j in range(size):
            if global_max == global_min:
                scaled = 0.5
            else:
                scaled = (max(q_table[(i, j)].values()) - global_min) / ((global_max - global_min))
            pygame.draw.rect(screen, (int((1 - scaled) * 255), int(scaled * 255), 0), pygame.Rect(600 + 20 * j, 100 + 20 * i, 20, 20))

    # Render text
    episode_track = font.render(f"Episode: {episode}", True, (30, 30, 30))
    screen.blit(episode_track, (100, 50))

    epsilon_track = font.render(f"Curiosity: {epsilon:.2%}", True, (30, 30, 30))
    screen.blit(epsilon_track, (100, 70))

    # End point
    pygame.draw.rect(screen, (250, 206, 104), pygame.Rect(100, 100, 20, 20))
    pygame.draw.rect(screen, (250, 206, 104), pygame.Rect(600, 100, 20, 20))
            
    # Render agent
    pygame.draw.rect(screen, (183, 189, 247), pygame.Rect(100 + (20 * agent_col), 100 + (20 * agent_row), 20, 20))

    pygame.display.flip()

    # Teleport back
    if matrix[agent_row][agent_col] != 0:
        if matrix[agent_row][agent_col] == 1:
            pygame.time.delay(2000)
        episode += 1
        steps.append(current_step)
        reward.append(q_sum)
        current_step = 0
        q_sum = 0
        epsilon = epsilon * decay_rate
        agent_row, agent_col = size - 1, size - 1

    # Delay movement frame
    # pygame.time.delay(50)

# Quit game
pygame.quit()

plt.subplot(1, 2, 1)
plt.title("Episodic Reward History")
plt.plot(reward)

plt.subplot(1, 2, 2)
plt.title("Steps per Episode History")
plt.plot(steps)
plt.show()