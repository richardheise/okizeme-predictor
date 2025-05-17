import rvr
import json
import os
import datetime
import csv

class OkizemeAI:

    AI_DEFENDING = 1
    PLAYER_DEFENDING = 0

    def __init__(self, rvr_path:str="./weights/rvr.json", markov_order=5, 
                 markov_path="") -> None:
       
        self.save_results = True

        if not os.path.exists(rvr_path):
            raise ValueError(f"RVR path {rvr_path} does not exist") 
        
        # Load RVR dictionary
        rvr_dict = None
        with open(rvr_path, "r") as f:
            rvr_dict = json.load(f)

        # Index dictionaries for attack and defense with the RVR values
        offense_moves = rvr_dict["offense_moves"]
        defense_moves = rvr_dict["defense_moves"]
        rvr_values = rvr_dict["rvr_values"]

        self.offensive_actions = offense_moves
        self.defensive_actions = defense_moves

        defense_dict = {}
        for i, offense_move in enumerate(offense_moves):
            defense_dict[offense_move] = {}
            for j, defense_move in enumerate(defense_moves):
                defense_dict[offense_move][defense_move] = rvr_values[i][j]

        offense_dict = {}
        for i, defense_move in enumerate(defense_moves):
            offense_dict[defense_move] = {}
            for j, offense_move in enumerate(offense_moves):
                offense_dict[defense_move][offense_move] = -rvr_values[j][i]

        print("Loaded RVR values:")
        print("Offense RVR:")
        print(defense_dict)

        print("Defense RVR:")
        print(offense_dict)
        
        # Initialize AI with the RVR values
        self.offense_predictor = rvr.AI(offense_dict)
        self.defense_predictor = rvr.AI(defense_dict)

        # Load Markov chains
        offense_markov_weights = os.path.join(markov_path, "offense")
        defense_markov_weights = os.path.join(markov_path, "defense")
        multi_markov_dicts = [[], []]
        for weights_path, markov_dicts in zip([offense_markov_weights, defense_markov_weights], multi_markov_dicts):
            for i in range(markov_order):
                try:
                    with open(f"{weights_path}/markov_{i + 1}.json", "r") as f:
                        markov_dict = json.load(f)
                        markov_dicts.append(markov_dict)
                except FileNotFoundError:
                    print(f"Markov file {weights_path}/markov_{i + 1}.json not found. Loading Markov without weights.")
                    markov_dicts.clear()
                    break
        
        self.offense_predictor.load_multi_markov(markov_order, multi_markov_dicts[0])
        self.defense_predictor.load_multi_markov(markov_order, multi_markov_dicts[1])

        print("Loaded Markov chains:")
        print(f"Offense Markov: {len(self.offense_predictor.multi_markov.get_markov_chains())}")
        print(f"Defense Markov: {len(self.defense_predictor.multi_markov.get_markov_chains())}")

        self.curr_defender = None


    def set_defender(self, defender:int):
        if defender not in [self.AI_DEFENDING, self.PLAYER_DEFENDING]:
            raise ValueError("Defender must be either AI_DEFENDING or PLAYER_DEFENDING")
        
        self.curr_defender = defender

    def predict_offense(self):
        self.set_defender(self.PLAYER_DEFENDING)
        return self.predict()
    
    def predict_defense(self):
        self.set_defender(self.AI_DEFENDING)
        return self.predict()

    def predict(self):

        if self.curr_defender is None:
            return None
        
        if self.curr_defender == self.AI_DEFENDING:
            pred_offense, ai_defense = self.offense_predictor.predict_action()
            print(f"AI predicted possible offense actions: {pred_offense}")

            if self.save_results:
                chains_state = self.offense_predictor.get_chain_state()
                self.offense_predictor_results.append(
                    {"pred_offense": pred_offense, "ai_defense": ai_defense, "chains_state": chains_state})
            
            ai_defense = sorted(ai_defense, key=lambda action: action[1], reverse=True)
            return self.defensive_actions.index(ai_defense[0][0])
        
        elif self.curr_defender == self.PLAYER_DEFENDING:
            pred_defense, ai_offense = self.defense_predictor.predict_action()
            print(f"AI predicted possible defense actions: {pred_defense}")

            if self.save_results:
                chains_state = self.defense_predictor.get_chain_state()
                self.defense_predictor_results.append(
                    {"pred_defense": pred_defense, "ai_offense": ai_offense, "chains_state": chains_state})

            ai_offense = sorted(ai_offense, key=lambda action: action[1], reverse=True)
            return self.offensive_actions.index(ai_offense[0][0])
        
    def get_damage(self, offense_action, defense_action) -> tuple[float, float]:
        """
        Returns:
            Tuple[AI damage, Player damage]
        """

        offense_action_str = self.offensive_actions[offense_action]
        defense_action_str = self.defensive_actions[defense_action]
        if self.curr_defender == self.AI_DEFENDING:
            player_reward = self.offense_predictor.calculate_player_reward(offense_action_str, defense_action_str)
        elif self.curr_defender == self.PLAYER_DEFENDING:
            player_reward = self.defense_predictor.calculate_player_reward(defense_action_str, offense_action_str)
        else:
            raise ValueError("Defender must be set before calculating damage")
        
        if player_reward < 0:
            return 0.0, -player_reward
        else:
            return player_reward, 0.0
        
    def get_player_actions(self):
        if self.curr_defender == self.AI_DEFENDING:
            return self.offense_predictor.get_player_actions()
        elif self.curr_defender == self.PLAYER_DEFENDING:
            return self.defense_predictor.get_player_actions()
        else:
            raise ValueError("Defender must be set before getting player actions")

    def update(self, action_taken:int):
        if self.curr_defender == self.AI_DEFENDING:
            action_taken_str = self.offensive_actions[action_taken]

            self.offense_predictor.update(action_taken_str)

            if self.save_results:
                self.offense_predictor_results[-1]["player_action"] = action_taken_str

        elif self.curr_defender == self.PLAYER_DEFENDING:
            action_taken_str = self.defensive_actions[action_taken]

            self.defense_predictor.update(action_taken_str)

            if self.save_results:
                self.defense_predictor_results[-1]["player_action"] = action_taken_str

    def save_weights(self, path:str):
        offense_path = os.path.join(path, "offense")
        defense_path = os.path.join(path, "defense")
        
        if not os.path.exists(offense_path):
            os.makedirs(offense_path)
        if not os.path.exists(defense_path):
            os.makedirs(defense_path)

        markov_dicts = self.offense_predictor.get_markov_chains()
        for i, markov_dict in enumerate(markov_dicts):
            with open(f"{offense_path}/markov_{i + 1}.json", "w") as f:
                json.dump(markov_dict, f, indent=4)

        markov_dicts = self.defense_predictor.get_markov_chains()
        for i, markov_dict in enumerate(markov_dicts):
            with open(f"{defense_path}/markov_{i + 1}.json", "w") as f:
                json.dump(markov_dict, f, indent=4)
            
    def init_results(self, player_level, player_knowledge, results_path) -> None:
        if not self.save_results:
            return

        if self.save_results:
            self.offense_predictor_results = []
            self.defense_predictor_results = []
            
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.path = os.path.join(results_path, f"results_{timestamp}_{player_level}_{player_knowledge}")
            os.makedirs(self.path, exist_ok=True)

    def export_results(self) -> None:

        if len(self.defense_predictor_results) <= 0 or len(self.offense_predictor_results) <= 0:
            return

        # Save results to CSV
        with open(os.path.join(self.path, "defense_results.csv"), "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.defense_predictor_results[0].keys())
            writer.writeheader()
            writer.writerows(self.defense_predictor_results)

        with open(os.path.join(self.path, "offense_results.csv"), "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.offense_predictor_results[0].keys())
            writer.writeheader()
            writer.writerows(self.offense_predictor_results)  
