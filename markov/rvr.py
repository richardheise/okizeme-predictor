import markov

class AI:

    def __init__(self, rvr: dict) -> None:

        if not rvr:
            return

        self.rewards = rvr

        self.ai_actions = list(rvr.keys())
        self.player_actions = list(rvr[self.ai_actions[0]].keys())

    def load_multi_markov(self, markov_order=5, markov_dicts=[]) -> None:
        if len(markov_dicts) > 0:
            markov_weights = []
            correct_predictions = []
            for markov_dict in markov_dicts:
                markov_weights.append(markov_dict["weights"])
                correct_predictions.append(markov_dict["correct_predictions"])
            self.multi_markov = markov.MultiMarkovChain(markov_order, self.player_actions, markov_weights, correct_predictions)
        else:
            self.multi_markov = markov.MultiMarkovChain(markov_order, self.player_actions)

    def get_markov_chains(self):
        markov_dicts = []
        markov_weights = self.multi_markov.get_markov_chains()
        for markov_chain in markov_weights:
            markov_dicts.append({"weights": markov_chain[0], "correct_predictions": markov_chain[1]})

        return markov_dicts

    def get_player_actions(self):
        return self.player_actions

    def predict_action(self):
        possible_player_actions = self.multi_markov.predict()
        
        possible_ai_actions = {}
        for ai_action in self.ai_actions:
            weight = 0.0

            # Weight the reward of the AI action with the probability of the possible player action
            for player_action in possible_player_actions:
                weight += self.rewards[ai_action][player_action[0]] * player_action[1]
            possible_ai_actions[ai_action] = weight

        # Sort the AI actions according to their reward
        possible_ai_actions = sorted(possible_ai_actions.items(), key=lambda action: action[1], reverse=True)

        # print(f"\n    [DEBUG] Finished prediction")
        # print(f"    [DEBUG] Possible offensive actions: {possible_player_actions}")
        # print(f"    [DEBUG] Possible defensive actions: {possible_ai_actions}\n")

        return [a for a in possible_player_actions], possible_ai_actions
    
    def update(self, action):
        self.multi_markov.update_matrix(action)

    def calculate_player_reward(self, player_action, ai_action):
        return -self.rewards[ai_action][player_action]
    
    def get_chain_state(self):
        return self.multi_markov.get_chains_state()