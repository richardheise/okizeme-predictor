import itertools
import random

DEFENSIVE_ACTIONS = ["Block", "Guard_jump", "Delayed_tech", "Button", "Throw", "Reversal", "Parry_high", "Parry_low"]

OFFENSIVE_ACTIONS = ["Throw", "Delayed_tc", "Meaty_high", "Meaty_low", "Shimmy_lp"]

class MarkovChain():

    DECAY = 0.9

    def __init__(self, order, actions) -> None:

        self.order = order

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

        self.curr_state = [random.choice(actions)]

    def update_matrix(self, action_taken):

        state_str = ''.join(self.curr_state)
        print(state_str)

        # Apply decay to state
        total_obs = 1
        for action in self.markov_matrix[state_str].keys():
            self.markov_matrix[state_str][action]['n_obs'] = self.DECAY * self.markov_matrix[state_str][action]['n_obs']
            total_obs += self.markov_matrix[state_str][action]['n_obs']

        self.markov_matrix[state_str][action_taken]['n_obs'] += 1
        
        # Re estimate probabiblities
        for action in self.markov_matrix[state_str].keys():
            self.markov_matrix[state_str][action]['prob'] = self.markov_matrix[state_str][action]['n_obs'] / total_obs

        self.curr_state.append(action_taken)
        if len(self.curr_state) > self.order:
            self.curr_state.pop(0)

    def predict(self):

        state_str = ''.join(self.curr_state)

        # Find max probabily 
        state_actions = list(self.markov_matrix[state_str].items())
        max_prob = max([action[1]['prob'] for action in state_actions])

        # Randonly choose between the actions with highest probability
        return max_prob, random.choice([action[0] for action in state_actions if action[1]['prob'] == max_prob])


def_markov = MarkovChain(3, DEFENSIVE_ACTIONS)
def_markov.update_matrix("Block")
def_markov.update_matrix("Throw")
def_markov.update_matrix("Reversal")
def_markov.update_matrix("Block")
print(def_markov.predict())