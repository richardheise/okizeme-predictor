import itertools
import random

DEFENSIVE_ACTIONS = ["Block", "Guard_jump", "Delayed_tech", "Button", "Throw", "Reversal", "Parry_high", "Parry_low"]

OFFENSIVE_ACTIONS = ["Throw", "Delayed_tc", "Meaty_high", "Meaty_low", "Shimmy_lp"]

class MarkovChain():

    DECAY = 0.9

    def __init__(self, order, actions) -> None:

        # Create a state for each combination of 'order' number of previous observations
        states = actions.copy()
        for _ in range(order - 1):
            for state in itertools.product(actions, states):
                states.append(''.join(state))

        self.markov_matrix = {}
        for state in states:
            # Chance for each action to happen in given state
            self.markov_matrix[state] = {}
            for action in actions:
                self.markov_matrix[state][action] = {'prob' : 1 / len(actions), 'n_obs' : 0 }

    def update_matrix(self, state, action_taken):

        # Apply decay to state
        total_obs = 1
        for action in self.markov_matrix[state].keys():
            self.markov_matrix[state][action]['n_obs'] = self.DECAY * self.markov_matrix[state][action]['n_obs']
            total_obs += self.markov_matrix[state][action]['n_obs']

        self.markov_matrix[state][action_taken]['n_obs'] += 1
        
        # Re estimate probabiblities
        for action in self.markov_matrix[state].keys():
            self.markov_matrix[state][action]['prob'] = self.markov_matrix[state][action]['n_obs'] / total_obs

    def predict(self, state):

        # Find max probabily 
        state_actions = list(self.markov_matrix[state].items())
        max_prob = max([action[1]['prob'] for action in state_actions])

        # Randonly choose between the actions with highest probability
        return max_prob, random.choice([action[0] for action in state_actions if action[1]['prob'] == max_prob])


def_markov = MarkovChain(3, DEFENSIVE_ACTIONS)
def_markov.update_matrix("Block", "Block")
def_markov.update_matrix("Block", "Throw")
def_markov.update_matrix("Block", "Reversal")
def_markov.update_matrix("Block", "Block")
print(def_markov.predict("Throw"))