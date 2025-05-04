import markov
import json
import os

class AI:

    def __init__(self, rvr: dict, markov_order=5) -> None:

        if not rvr:
            return

        self.rewards = rvr

        self.ai_actions = list(rvr.keys())
        self.player_actions = list(rvr[self.ai_actions[0]].keys())
        self.multi_markov = markov.MultiMarkovChain(markov_order, self.player_actions)

    def from_files(self, rvr_path: str, markov_path: str = "", markov_order=5):

        # Load RVR dictionary
        if rvr_path == "":
            raise ValueError("RVR path is required")
        
        with open(rvr_path, "r") as f:
            self.rewards = json.load(f)

        self.ai_actions = list(self.rewards.keys())
        self.player_actions = list(self.rewards[self.ai_actions[0]].keys())

        # Load Markov chains
        if markov_path != "":
            markov_weights = []
            for i in range(markov_order):
                try:
                    with open(f"{markov_path}/markov_{i + 1}.json", "r") as f:
                        markov_weights.append(json.load(f))
                except FileNotFoundError:
                    raise ValueError(f"Markov file {markov_path}/markov_{i + 1}.json not found")
            self.multi_markov = markov.MultiMarkovChain(markov_order, self.player_actions, markov_weights)
        else:
            self.multi_markov = markov.MultiMarkovChain(markov_order, self.player_actions)

    def save_weights(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

        markov_weights = self.multi_markov.get_markov_chains()
        for i, markov_chain in enumerate(markov_weights):
            with open(f"{path}/markov_{i + 1}.json", "w") as f:
                json.dump(markov_chain, f, indent=4)

    def save_rvr(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

        with open(f"{path}/rvr.json", "w") as f:
            json.dump(self.rewards, f, indent=4)

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

        return [a[0] for a in possible_player_actions], possible_ai_actions[0][0]
    
    def update(self, action):
        self.multi_markov.update_matrix(action)

    def calculate_rewards(self, player_action, ai_action):
        ai_reward = self.rewards[ai_action][player_action]

        return -ai_reward, ai_reward
        
