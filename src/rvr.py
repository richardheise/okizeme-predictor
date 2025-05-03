import markov

DEFFENSIVE_REWARDS = {
    "Block": {"Throw": -1.7, "Delayed_tc": -0.7, "Meaty_high": -0.7, "Meaty_low": -0.5, "Shimmy_lp": -0.5},
    "Guard_jump": {"Throw": 0.5, "Delayed_tc": -4.2, "Meaty_high": -0.7, "Meaty_low": -0.5, "Shimmy_lp": 0.5},
    "Delayed_tech": {"Throw": -0.5, "Delayed_tc": -4.2, "Meaty_high": -0.7, "Meaty_low": -0.5, "Shimmy_lp": -3.7},
    "Button": {"Throw": -1.7, "Delayed_tc": 4.2, "Meaty_high": -4.2, "Meaty_low": -3.2, "Shimmy_lp": 3.7},
    "Throw": {"Throw": -0.5, "Delayed_tc": 1.7, "Meaty_high": -4.2, "Meaty_low": -3.2, "Shimmy_lp": -4.2},
    "Reversal": {"Throw": 2.1, "Delayed_tc": -3.7, "Meaty_high": 2.1, "Meaty_low": 2.1, "Shimmy_lp": -4.2},
    "Parry_high": {"Throw": -1.7, "Delayed_tc": 4.2, "Meaty_high": 4.2, "Meaty_low": -3.2, "Shimmy_lp": -0.5},
    "Parry_low": {"Throw": -1.7, "Delayed_tc": -4.2, "Meaty_high": -4.2, "Meaty_low": 4.2, "Shimmy_lp": 0.5},
}

OFFENSIVE_REWARDS = {
    "Throw": {"Block": 1.7, "Guard_jump": -0.5, "Delayed_tech": 0.5, "Button": 1.7, "Throw": 0.7, "Reversal": -2.1, "Parry_high": 1.7, "Parry_low": 1.7},
    "Delayed_tc": {"Block": 0.7, "Guard_jump": 4.2, "Delayed_tech": 4.2, "Button": -4.2, "Throw": -1.7, "Reversal": 3.7, "Parry_high": -4.2, "Parry_low": 4.2},
    "Meaty_high": {"Block": 0.7, "Guard_jump": 0.7, "Delayed_tech": 0.7, "Button": 4.2, "Throw": 4.2, "Reversal": -2.2, "Parry_high": -4.2, "Parry_low": 4.2},
    "Meaty_low": {"Block": 0.5, "Guard_jump": 0.5, "Delayed_tech": 0.5, "Button": 3.2, "Throw": 3.2, "Reversal": -2.2, "Parry_high": 3.2, "Parry_low": -4.2},
    "Shimmy_lp": {"Block": 0.5, "Guard_jump": -0.5, "Delayed_tech": 3.7, "Button": -3.7, "Throw": 3.7, "Reversal": 4.2, "Parry_high": 0.5, "Parry_low": 0.5},
}

MARKOV_ORDER = 5

class AI():

    def __init__(self) -> None:

        self.offensive_actions = list(OFFENSIVE_REWARDS.keys())
        self.offsentive_pred_chain = markov.MarkovChain(MARKOV_ORDER, self.offensive_actions)

        self.deffensive_actions = list(DEFFENSIVE_REWARDS.keys())
        self.deffensive_pred_chain = markov.MarkovChain(MARKOV_ORDER, self.deffensive_actions)

    def list_defense_actions(self):
        for i, action in enumerate(self.deffensive_actions):
            print(f"{i}: {action}", end=", ")
        print("")

    def list_offense_actions(self):
        for i, action in enumerate(self.offensive_actions):
            print(f"{i}: {action}", end=", ")
        print(" ")

    def predict_offense_action(self):
        possible_off_actions = self.offsentive_pred_chain.predict()
        
        # For each def action, weight the reward with the probability of the off action
        defensive_actions = {}
        for def_action in self.deffensive_actions:
            weight = 0.0
            for off_action in possible_off_actions:
                weight += DEFFENSIVE_REWARDS[def_action][off_action[0]] * off_action[1]["prob"]
            defensive_actions[def_action] = weight

        # Sort the defensive actions by their reward
        defensive_actions = sorted(defensive_actions.items(), key=lambda action: action[1], reverse=True)

        print(f"\n  [DEBUG] Finished prediction")
        print(f"    [DEBUG] Possible offensive actions: {possible_off_actions}")
        print(f"    [DEBUG] Possible defensive actions: {defensive_actions}\n")

        return [a[0] for a in possible_off_actions], defensive_actions[0][0]
    
    def get_offense_action(self, idx):
        return self.offensive_actions[idx]
    
    def update_offense(self, action):
        self.offsentive_pred_chain.update_matrix(action)

    def calculate_rewards(self, offense, defense):
        offensive = OFFENSIVE_REWARDS[offense][defense] 
        defensive = DEFFENSIVE_REWARDS[defense][offense]

        return offensive, defensive
        