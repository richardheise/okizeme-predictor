import markov

MARKOV_ORDER = 5

class AI():

    def __init__(self, rvr) -> None:

        self.rewards = rvr

        self.ai_actions = list(rvr.keys())
        self.player_actions = list(rvr[self.ai_actions[0]].keys())
        self.multi_markov = markov.MultiMarkovChain(MARKOV_ORDER, self.player_actions)

    def get_player_actions(self):
        return self.player_actions

    def predict_action(self):
        possible_player_actions = self.multi_markov.predict()
        
        # For each AI action, weight the reward with the probability of the respective possible player action
        possible_ai_actions = {}
        for ai_action in self.ai_actions:
            weight = 0.0
            for player_action in possible_player_actions:
                weight += self.rewards[ai_action][player_action[0]] * player_action[1]
            possible_ai_actions[ai_action] = weight

        # Sort the AI actions according to their reward
        possible_ai_actions = sorted(possible_ai_actions.items(), key=lambda action: action[1], reverse=True)

        # print(f"\n    [DEBUG] Finished prediction")
        # print(f"    [DEBUG] Possible offensive actions: {possible_player_actions}")
        # print(f"    [DEBUG] Possible defensive actions: {possible_ai_actions}\n")

        return [a[0] for a in possible_player_actions], possible_ai_actions[0][0]
    
    def update(self, action):
        self.multi_markov.update_matrix(action)

    def calculate_rewards(self, player_action, ai_action):
        ai_reward = self.rewards[ai_action][player_action]

        return -ai_reward, ai_reward
        
