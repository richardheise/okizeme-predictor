import rvr
import os

NUM_ROUNDS = 140

DEFFENSIVE_REWARDS = {
    "Block": {"Throw": -1.7, "Delayed_tc": -0.7, "Meaty_high": -0.7, "Meaty_low": -0.5, "Shimmy_lp": -0.5},
    "Guard_jump": {"Throw": 0.5, "Delayed_tc": -4.2, "Meaty_high": -0.7, "Meaty_low": -0.5, "Shimmy_lp": 0.5},
    "Button": {"Throw": -1.7, "Delayed_tc": 4.2, "Meaty_high": -4.2, "Meaty_low": -3.2, "Shimmy_lp": 3.7},
    "Throw": {"Throw": -0.5, "Delayed_tc": 1.7, "Meaty_high": -4.2, "Meaty_low": -3.2, "Shimmy_lp": -4.2},
    "Reversal": {"Throw": 2.1, "Delayed_tc": -3.7, "Meaty_high": 2.1, "Meaty_low": 2.1, "Shimmy_lp": -4.2},
    "Parry_high": {"Throw": -1.7, "Delayed_tc": 4.2, "Meaty_high": 4.2, "Meaty_low": -3.2, "Shimmy_lp": -0.5},
    "Parry_low": {"Throw": -1.7, "Delayed_tc": -4.2, "Meaty_high": -4.2, "Meaty_low": 4.2, "Shimmy_lp": 0.5},
}

OFFENSIVE_REWARDS = {
    "Throw": {"Block": 1.7, "Guard_jump": -0.5, "Button": 1.7, "Throw": 0.7, "Reversal": -2.1, "Parry_high": 1.7, "Parry_low": 1.7},
    "Delayed_tc": {"Block": 0.7, "Guard_jump": 4.2, "Button": -4.2, "Throw": -1.7, "Reversal": 3.7, "Parry_high": -4.2, "Parry_low": 4.2},
    "Meaty_high": {"Block": 0.7, "Guard_jump": 0.7, "Button": 4.2, "Throw": 4.2, "Reversal": -2.2, "Parry_high": -4.2, "Parry_low": 4.2},
    "Meaty_low": {"Block": 0.5, "Guard_jump": 0.5, "Button": 3.2, "Throw": 3.2, "Reversal": -2.2, "Parry_high": 3.2, "Parry_low": -4.2},
    "Shimmy_lp": {"Block": 0.5, "Guard_jump": -0.5, "Button": -3.7, "Throw": 3.7, "Reversal": 4.2, "Parry_high": 0.5, "Parry_low": 0.5},
}

def get_player_action(prompt, possible_actions):
    print("Actions:")
    for i, action in enumerate(possible_actions):
        print(f"{i}: {action}", end="   ")
    print()

    input_str = input(prompt)

    # Check if input is a number in range
    if input_str.isdigit():
        try:
            action_index = int(input_str)
            if 0 <= action_index < len(possible_actions):
                return possible_actions[action_index]
            else:
                print("Invalid input. Please enter a valid action number.")
                return get_player_action(prompt, possible_actions)
        except ValueError:
            print("Invalid input. Please enter a valid action number.")
            return get_player_action(prompt, possible_actions)

if __name__ == "__main__":

    defensive_ai = rvr.AI(DEFFENSIVE_REWARDS)
    offensive_ai = rvr.AI(OFFENSIVE_REWARDS)

    ai_wins, player_wins = 0, 0

    for r in range(NUM_ROUNDS):
        os.system("cls" if os.name == "nt" else "clear")

        print("\n=====================")
        print(f"Round {r + 1}/{NUM_ROUNDS} - AI wins: {ai_wins}, Your wins: {player_wins}\n")
        print("You're attacking...")
        
        # Call AI to predict player action and a response
        pred_offense, ai_defense = defensive_ai.predict_action()
        player_offense = get_player_action("Choose your action: ", defensive_ai.get_player_actions())
        
        print(f"Your offensive action: {player_offense}\n")
        print(f"AI predicted possible offensive actions: {pred_offense}")
        print(f"AI defensive action: {ai_defense}\n")

        # Calculate rewards
        player_reward, ai_reward = defensive_ai.calculate_rewards(player_offense, ai_defense)
        print(f"Your reward: {player_reward}")
        print(f"AI reward: {ai_reward}\n")
        
        print("Winner: ", end="")
        if player_reward > ai_reward:
            print("You")
            player_wins += 1
        elif player_reward < ai_reward:
            print("AI")
            ai_wins += 1

        defensive_ai.update(player_offense)

        print("\n=====\n")
        print("You're defending...")

        # Call AI to predict player action and a response
        pred_defense, ai_offense = offensive_ai.predict_action()
        player_defense = get_player_action("Choose your action: ", offensive_ai.get_player_actions())
        
        print(f"Your defensive action: {player_defense}\n")
        print(f"AI predicted possible defensive actions: {pred_defense}")
        print(f"AI offensive action: {ai_offense}\n")
        
        # Calculate rewards
        player_reward, ai_reward = offensive_ai.calculate_rewards(player_defense, ai_offense)
        print(f"Your reward: {player_reward}")
        print(f"AI reward: {ai_reward}\n")

        print("Winner: ", end="")
        if player_reward > ai_reward:
            print("You")
            player_wins += 1
        elif player_reward < ai_reward:
            print("AI")
            ai_wins += 1
        
        offensive_ai.update(player_defense)

        input("\n=====================\n")