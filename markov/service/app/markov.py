import itertools
import random

class MarkovChain():

    DECAY = 0.9

    def __init__(self, order, actions, markov_matrix=None) -> None:

        self.order = order
        self.markov_matrix = {}

        # Create a state for each combination of 'order' number of previous observations
        states = actions.copy()
        for _ in range(order - 1):
            for state in itertools.product(actions, states):
                states.append(''.join(state))

        if markov_matrix is None:
            for state in states:
                # Chance for each action to happen in given state
                self.markov_matrix[state] = {}
                for action in actions:
                    self.markov_matrix[state][action] = {'prob' : 1 / len(actions), 'n_obs' : 1.0 }
        else:
            self.markov_matrix = markov_matrix

        self.curr_state = None

    def get_markov_matrix(self):
        return self.markov_matrix

    def update_matrix(self, action_taken):

        if self.curr_state is None:
            self.curr_state = [action_taken]
            return

        curr_state_str = ''.join(self.curr_state)

        # Apply decay to state
        total_obs = 1
        for action in self.markov_matrix[curr_state_str].keys():
            self.markov_matrix[curr_state_str][action]['n_obs'] = self.DECAY * self.markov_matrix[curr_state_str][action]['n_obs']
            total_obs += self.markov_matrix[curr_state_str][action]['n_obs']

        self.markov_matrix[curr_state_str][action_taken]['n_obs'] += 1
        
        # Re estimate probabiblities
        for action in self.markov_matrix[curr_state_str].keys():
            self.markov_matrix[curr_state_str][action]['prob'] = self.markov_matrix[curr_state_str][action]['n_obs'] / total_obs

        self.curr_state.append(action_taken)
        if len(self.curr_state) > self.order:
            self.curr_state.pop(0)

    def predict(self):

        if self.curr_state is None:
            state = random.choice(list(self.markov_matrix.keys()))
            return random.choice(list(self.markov_matrix[state].items()))

        state_str = ''.join(self.curr_state)

        # Find max probabily 
        state_actions = list(self.markov_matrix[state_str].items())
        max_prob = max([action[1]['prob'] for action in state_actions])

        return random.choice([action for action in state_actions if action[1]['prob'] == max_prob])
    
    def __str__(self) -> str:
        markov_str = f"Markov Chain - Order: {self.order}\n"
        for state, actions in self.markov_matrix.items():
            markov_str += f"State: {state}\n"
            for action, data in actions.items():
                markov_str += f"    Action: {action}, Prob: {data['prob']}, N_obs: {data['n_obs']}\n"

        return markov_str

class MultiMarkovChain():

    def __init__(self, order, actions, markov_weights=None, correct_predictions=None) -> None:
        self.order = order
        self.markov_chains = []
        self.curr_round = 0
        self.last_predictions = [None] * self.order
        
        if correct_predictions is None:
            self.correct_predictions = [[] for _ in range(self.order)]
        else:
            self.correct_predictions = correct_predictions

        for i in range(order):
            if markov_weights is None:
                self.markov_chains.append(MarkovChain(i + 1, actions))
            else:
                self.markov_chains.append(MarkovChain(i + 1, actions, markov_weights[i]))

    def get_markov_chains(self):
        return [(markov_chain.get_markov_matrix(), self.correct_predictions[i]) for i, markov_chain in enumerate(self.markov_chains)]

    def predict(self):
        for i, markov_chain in enumerate(self.markov_chains):
            self.last_predictions[i] = markov_chain.predict()[0]
        
        self.curr_round += 1

        # Weight the predictions based on the number of correct predictions from the chain
        num_correct_preds = [sum(correct_preds) for correct_preds in self.correct_predictions]
        total_correct_preds = sum(num_correct_preds)
        weighted_preds = []
        for i in range(len(self.correct_predictions[0])):
            weight = (num_correct_preds[i] / total_correct_preds) if total_correct_preds > 0 else 0.1
            weighted_preds.append((self.last_predictions[i], weight))

        # Return the best (order / 2 rounded up) predictions
        return weighted_preds

    def update_matrix(self, action_taken):
        for markov_chain in self.markov_chains:
            markov_chain.update_matrix(action_taken)

        for i in range(self.order):
            self.correct_predictions[i].append(1 if self.last_predictions[i] == action_taken else 0)

            if len(self.correct_predictions[i]) > self.order:
                self.correct_predictions[i].pop(0)

    def get_chains_state(self):
        return [('-'.join(markov_chain.curr_state) if markov_chain.curr_state is not None else "None", 
             self.correct_predictions[i]) for i, markov_chain in enumerate(self.markov_chains)]
