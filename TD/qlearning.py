"""
Q-learning Agent

Here's an example:
    from qlearning import QLearningAgent

    agent = QLearningAgent(
        alpha=0.5,epsilon=0.25,discount=0.99,
        getLegalActions = lambda s: actions_from_that_state)
    action = agent.getAction(state)
    agent.update(state,action, next_state,reward)
    agent.epsilon *= 0.99
"""

import random

import numpy as np
from collections import defaultdict


class QLearningAgent(object):
    """
      Q-Learning Agent

      The two main methods are
      - self.getAction(state) - returns agent's action in that state
      - self.update(state,action,nextState,reward) - returns agent's next action

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
        - self.getQValue(state,action)
          which returns Q(state,action)
        - self.setQValue(state,action,value)
          which sets Q(state,action) := value

      !!!Important!!!
      NOTE: please avoid using self._qValues directly to make code cleaner
    """

    def __init__(self, alpha, epsilon, discount, getLegalActions):
        "We initialize agent and Q-values here."
        self.getLegalActions = getLegalActions
        self._qValues = defaultdict(lambda: defaultdict(lambda: 0))
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount = discount

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
        """
        return self._qValues[state][action]

    def setQValue(self, state, action, value):
        """
          Sets the Qvalue for [state,action] to the given value
        """
        self._qValues[state][action] = value

    def getValue(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.
        """

        possibleActions = self.getLegalActions(state)
        # If there are no legal actions, return 0.0
        if len(possibleActions) == 0:
            return 0.0

        return max([self.getQValue(state, a) for a in possibleActions])

    def getPolicy(self, state):
        """
          Compute the best action to take in a state.

        """
        possibleActions = self.getLegalActions(state)

        # If there are no legal actions, return None
        if len(possibleActions) == 0:
            return None

        best_action = possibleActions[
            np.argmax([self.getQValue(state, a) for a in possibleActions])]
        return best_action

    def getAction(self, state):
        """
          Compute the action to take in the current state, including exploration.

          With probability self.epsilon, we should take a random action.
          otherwise - the best policy action (self.getPolicy).

        """

        # Pick Action
        possibleActions = self.getLegalActions(state)
        action = None

        # If there are no legal actions, return None
        if len(possibleActions) == 0:
            return None

        # agent parameters:
        epsilon = self.epsilon

        if np.random.random() <= epsilon:
            action = random.choice(possibleActions)
        else:
            action = self.getPolicy(state)
        return action

    def update(self, state, action, nextState, reward):
        """
          You should do your Q-Value update here
        """
        # agent parameters
        gamma = self.discount
        learning_rate = self.alpha

        reference_qvalue = reward + gamma * self.getValue(nextState)
        updated_qvalue = (1 - learning_rate) * self.getQValue(state, action) + \
                         learning_rate * reference_qvalue
        self.setQValue(state, action, updated_qvalue)
