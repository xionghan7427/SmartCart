import numpy as np
import random
import pyautogui
from collections import deque
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Simulation Environment
class CursorEnv:
    def __init__(self, screen_width=200, screen_height=200):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_pos = None
        self.target = None

    def reset(self):
        # Random start position and target
        self.current_pos = (
            np.random.randint(0, self.screen_width),
            np.random.randint(0, self.screen_height)
        )
        self.target = (
            np.random.randint(0, self.screen_width),
            np.random.randint(0, self.screen_height)
        )
        return self._get_state()

    def _get_state(self):
        # State is [delta_x, delta_y] from current position to target
        dx = self.target[0] - self.current_pos[0]
        dy = self.target[1] - self.current_pos[1]
        return np.array([dx, dy])

    def step(self, action):
        x, y = self.current_pos
        # Action: 0=up, 1=down, 2=left, 3=right
        if action == 0:    y = max(0, y - 10)
        elif action == 1:  y = min(self.screen_height, y + 10)
        elif action == 2:  x = max(0, x - 10)
        elif action == 3:  x = min(self.screen_width, x + 10)
        
        self.current_pos = (x, y)
        next_state = self._get_state()
        
        # Calculate reward
        distance = np.sqrt(next_state[0]**2 + next_state[1]**2)
        done = distance < 5  # Close enough to target
        reward = -distance  # Penalize for distance
        
        if done:
            reward += 100  # Large reward for reaching target
            
        return next_state, reward, done, {}

# DQN Agent
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        state = np.reshape(state, [1, self.state_size])
        q_values = self.model.predict(state, verbose=0)
        return np.argmax(q_values[0])

    def replay(self, batch_size=32):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        states = np.array([t[0] for t in minibatch])
        actions = np.array([t[1] for t in minibatch])
        rewards = np.array([t[2] for t in minibatch])
        next_states = np.array([t[3] for t in minibatch])
        dones = np.array([t[4] for t in minibatch])

        targets = self.model.predict(states, verbose=0)
        next_q_values = self.model.predict(next_states, verbose=0)
        targets[range(batch_size), actions] = rewards + self.gamma * np.max(next_q_values, axis=1) * (1 - dones)

        self.model.fit(states, targets, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# Training Loop
def train_agent(episodes=1000):
    env = CursorEnv()
    state_size = 2
    action_size = 4
    agent = DQNAgent(state_size, action_size)
    
    for e in range(episodes):
        state = env.reset()
        total_reward = 0
        done = False
        
        while not done:
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward
            
            agent.replay()
        
        print(f"Episode: {e+1}/{episodes}, Total Reward: {total_reward:.2f}, Epsilon: {agent.epsilon:.2f}")

# After training, use this to control real cursor
def move_to_target(target_x, target_y, model):
    while True:
        current_x, current_y = pyautogui.position()
        dx = target_x - current_x
        dy = target_y - current_y
        state = np.array([dx, dy])
        action = np.argmax(model.predict(np.reshape(state, [1, 2]), verbose=0)[0])
        
        # Take action
        if action == 0: pyautogui.move(0, -10)  # Up
        elif action == 1: pyautogui.move(0, 10)  # Down
        elif action == 2: pyautogui.move(-10, 0)  # Left
        elif action == 3: pyautogui.move(10, 0)   # Right
        
        # Check if close enough
        if np.sqrt(dx**2 + dy**2) < 5:
            break

# Uncomment to train
train_agent(episodes=100)

# After training, save the model and use it like:
# agent.model.save('cursor_agent.h5')
# Then load and use move_to_target(target_x, target_y, model)