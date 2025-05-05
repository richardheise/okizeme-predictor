import rvr
import os

LOAD_WEIGHTS = True

NUM_ROUNDS = 5
MARKOV_ORDER = 5

DEFENSE_RVR_PATH = "weights/rvr_defense.json"
OFFENSE_RVR_PATH = "weights/rvr_offense.json"

OFFENSE_MARKOV_PATH = "weights/offense"
DEFENSE_MARKOV_PATH = "weights/defense"

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
    else:
        print("Invalid input. Please enter a valid action number.")
        return get_player_action(prompt, possible_actions)

if __name__ == "__main__":

    defensive_ai = rvr.AI({})
    offensive_ai = rvr.AI({})

    if LOAD_WEIGHTS:
        defensive_ai.from_files(DEFENSE_RVR_PATH, DEFENSE_MARKOV_PATH, MARKOV_ORDER)
        offensive_ai.from_files(OFFENSE_RVR_PATH, OFFENSE_MARKOV_PATH, MARKOV_ORDER)
    else:
        defensive_ai.from_files(DEFENSE_RVR_PATH, markov_order=MARKOV_ORDER)
        offensive_ai.from_files(OFFENSE_RVR_PATH, markov_order=MARKOV_ORDER)

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

    if LOAD_WEIGHTS:
        defensive_ai.save_weights(DEFENSE_MARKOV_PATH)
        offensive_ai.save_weights(OFFENSE_MARKOV_PATH)
