# Maze Escape: A Q-Learning Experiment

### What I explored

A simple grid-based environment where an agent learns to navigate a maze and avoid obstacles (lava). Alongside the maze, a real-time heatmap visually maps out how the agent evaluates the safest route over time. The project is written in Python using PyGame.

### Why I was curious

I wanted to understand how Reinforcement Learning works under the hood. I was curious about how an agent learns from its mistakes, remembers its environment, and eventually figures out a solution. This project was a space to observe how basic math formulas translate into decision-making behavior.

### Notes and Observations

Documenting a few takeaways from building this:

* **Curiosity and Memory:** The agent starts with zero knowledge and wanders randomly. Every time it hits a wall, falls into lava, or finds the goal, it updates its internal map. Over thousands of attempts, the random exploration decreases, and the agent begins to rely on its stored memory to navigate safely.
* **The Heatmap:** By assigning a high score (1000) to the goal and a penalty (-1) to the lava, the "value" of the goal slowly spreads backward across the map over time. The green path on the heatmap isn't a hardcoded route—it emerges naturally as the agent follows the highest values it remembers.
* **Boundaries:** Initially, the code prevented the agent from walking into walls to avoid errors. I later realized this prevented the agent from fully learning the layout. Allowing it to hit the wall and receive a step penalty forced it to learn spatial awareness organically.

### The Results

**1. The Learning Phase (Heatmap Evolution)**

<img width="1653" height="826" alt="Learning" src="https://github.com/user-attachments/assets/4cb78170-3318-49ab-9d1a-d6f2e4e98a48" />

> In the early episodes, the agent is still learning the layout. The heatmap shows fragmented paths as it explores the maze through trial and error.

**2. The Final Understanding (Convergence)**

<img width="1637" height="826" alt="Final" src="https://github.com/user-attachments/assets/3cea6eee-e373-43ca-a8f6-463f014ef149" />

> The final heatmap reflects the agent's understanding of the maze. It establishes a primary safe route along the outer walls while also mapping efficient shortcuts through the central gaps.

**3. Convergence Analytics**

<img width="1920" height="1003" alt="Record" src="https://github.com/user-attachments/assets/15b36120-131e-4bb3-88d3-70365feac572" />

> The charts track the learning progress. The step count starts high and chaotic, but eventually flattens out into a straight line once the safest path is memorized.

### Tools / Methods

* **Language:** Python
* **Libraries:** PyGame, Matplotlib
* **Method:** Q-Learning

### Running the Simulation

To run the simulation locally:

```bash
pip install pygame matplotlib
python board.py

```
