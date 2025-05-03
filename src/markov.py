import itertools
import random

class MarkovChain():

    DECAY = 0.9
    PREDICT_NUM = 5
    PRED_THRES = 0.1

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
                self.markov_matrix[state][action] = {'prob' : 1 / len(actions), 'n_obs' : 1.0 }

        self.curr_state = None

    def update_matrix(self, action_taken):

        if self.curr_state is None:
            self.curr_state = [action_taken]
            return

        curr_state_str = ''.join(self.curr_state)

        # Update all states that start with the current state
        for state in list(self.markov_matrix.keys()):
            if not state.startswith(curr_state_str):
                continue

            # Apply decay to state
            total_obs = 1
            for action in self.markov_matrix[state].keys():
                self.markov_matrix[state][action]['n_obs'] = self.DECAY * self.markov_matrix[state][action]['n_obs']
                total_obs += self.markov_matrix[state][action]['n_obs']

            self.markov_matrix[state][action_taken]['n_obs'] += 1
            
            # Re estimate probabiblities
            for action in self.markov_matrix[state].keys():
                self.markov_matrix[state][action]['prob'] = self.markov_matrix[state][action]['n_obs'] / total_obs

        self.curr_state.append(action_taken)
        if len(self.curr_state) > self.order:
            self.curr_state.pop(0)

    def predict(self):

        if self.curr_state is None:
            state = random.choice(list(self.markov_matrix.keys()))
            return random.choices(list(self.markov_matrix[state].items()), k=self.PREDICT_NUM)

        state_str = ''.join(self.curr_state)

        # Find max probabily 
        state_actions = list(self.markov_matrix[state_str].items())
        max_prob = max([action[1]['prob'] for action in state_actions])

        # Filter actions with probability above threshold
        possible_actions = [action for action in state_actions if action[1]['prob'] >= (max_prob - self.PRED_THRES)]
        possible_actions = sorted(possible_actions, key=lambda action: action[1]['prob'], reverse=True)[:self.PREDICT_NUM]

        return possible_actions
    
    def __str__(self) -> str:
        markov_str = f"Markov Chain - Order: {self.order}\n"
        for state, actions in self.markov_matrix.items():
            markov_str += f"State: {state}\n"
            for action, data in actions.items():
                markov_str += f"    Action: {action}, Prob: {data['prob']}, N_obs: {data['n_obs']}\n"

        return markov_str