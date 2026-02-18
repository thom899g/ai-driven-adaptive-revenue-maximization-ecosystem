import gym
from typing import Dict, Any
import numpy as np

class MarketEnvironment(gym.Env):
    def __init__(self, data_collector: MarketDataCollector):
        super().__init__()
        self.data_collector = data_collector
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(4,))
        self.action_space = gym.spaces.Discrete(3)
        self.current_data = None

    def reset(self) -> Dict:
        """
        Resets the environment with new market data.
        
        Returns:
            Initial observation of the environment state.
        """
        # Get new data
        start_date = "2024-01-01"
        end_date = "2024-01-31"
        self.current_data = self.data_collector.fetch_data(start_date, end_date)
        
        # Initial observation (example)
        initial_obs = np.array([self.current_data.iloc[0].price]*4)
        return initial_obs

    def step(self, action: int) -> Dict:
        """
        Executes one step of the environment simulation.
        
        Args:
            action: Action taken by the agent.
            
        Returns:
            Tuple containing (observation, reward, done, info).
        """
        # Simulate market response
        current_price = self.current_data.iloc[self.ptr].price
        if action == 0:
            new_price = max(current_price * 0.95, 10)
        elif action == 1:
            new_price = current_price
        else:
            new_price = min(current_price * 1.05, 200)
            
        # Calculate reward (simplified example)
        reward = (new_price - current_price) / current_price
        
        self.ptr += 1
        done = self.ptr >= len(self.current_data) - 1
        observation = np.array([self.current_data.iloc[self.ptr].price]*4) if not done else None
        info = {'action': action, 'reward': reward}
        
        return observation, reward, done, info