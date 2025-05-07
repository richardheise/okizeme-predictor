import okizeme_ai

LOAD_WEIGHTS = True
SAVE_RESULTS = True

NUM_ROUNDS = 1
MARKOV_ORDER = 5

RVR_PATH = "weights/rvr.json"
MARKOV_PATH = "weights"

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

    if LOAD_WEIGHTS:
        ai = okizeme_ai.OkizemeAI(RVR_PATH, MARKOV_ORDER, MARKOV_PATH, SAVE_RESULTS)
    else:
        ai = okizeme_ai.OkizemeAI(RVR_PATH, MARKOV_ORDER, save_results=SAVE_RESULTS)

    for i in range(NUM_ROUNDS):
        print(f"\n=====================\nRound {i + 1} of {NUM_ROUNDS}")
        player_hp, ai_hp = 8.0, 8.0
        while player_hp > 0 and ai_hp > 0:
            # os.system("cls" if os.name == "nt" else "clear")

            ai.set_defender(ai.AI_DEFENDING)
            print("\n=====================")
            print(f"Player HP: {player_hp} - AI HP: {ai_hp}")
            print("You're attacking...")
            
            # Call AI to predict player action and a response
            player_offense = get_player_action("Choose your action: ", ai.get_player_actions())
            print(f"Your offensive action: {player_offense}\n")
            ai_defense = ai.predict()
            print(f"AI defensive action: {ai_defense}\n")

            # Calculate rewards
            ai_damage, player_damage = ai.get_damage(player_offense, ai_defense)
            print(f"Your damage: {player_damage}")
            print(f"AI damage: {ai_damage}\n")
            # Update HP
            player_hp -= player_damage
            ai_hp -= ai_damage
            ai.update(player_offense)

            ai.change_sides()
            print("\n=====\n")
            print("You're defending...")

            # Call AI to predict player action and a response
            player_defense = get_player_action("Choose your action: ", ai.get_player_actions())
            print(f"Your defensive action: {player_defense}\n")
            ai_offense = ai.predict()
            print(f"AI offensive action: {ai_offense}\n")
            
            # Calculate rewards
            ai_damage, player_damage = ai.get_damage(ai_offense, player_defense)
            print(f"Your damage: {player_damage}")
            print(f"AI damage: {ai_damage}\n")
            ai.update(player_defense)

            input("\n=====================\n")

    if LOAD_WEIGHTS:
        ai.save_weights(MARKOV_PATH)

    ai.export_results("./results", 0, 0)
