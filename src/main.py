import rvr

NUM_ROUNDS = 50

if __name__ == "__main__":

    ai = rvr.AI()

    ai_wins, player_wins = 0, 0

    for r in range(NUM_ROUNDS):
        print("\n=====================")
        print(f"Round {r + 1}/{NUM_ROUNDS} - AI wins: {ai_wins}, Your wins: {player_wins}\n")
        print("You're attacking...")
        print("Actions:")
        ai.list_offense_actions()
        
        pred_offense, ai_defense = ai.predict_offense_action()
        player_offense = ai.get_offense_action(int(input("")))
        
        print(f"Your offensive action: {player_offense}\n")
        print(f"AI predicted possible offensive actions: {pred_offense}")
        print(f"AI defensive action: {ai_defense}\n")

        player_reward, ai_reward = ai.calculate_rewards(player_offense, ai_defense)
        print(f"Your reward: {player_reward}")
        print(f"AI reward: {ai_reward}\n")
        
        print("Winner: ", end="")
        if player_reward > ai_reward:
            print("You")
            player_wins += 1
        elif player_reward < ai_reward:
            print("AI")
            ai_wins += 1

        ai.update_offense(player_offense)

        # print("You're defending...")
        # pred_defense, ai_offense = ai.predict_defense_action()
        # player_defense = ai.get_defense_action(input())

        # print(f"Your defensive action: {player_defense}\n")
        # print(f"AI predicted defensive action: {pred_defense}")
        # print(f"AI offensive action: {ai_offense}\n")

        # ai_reward, player_reward = ai.calculate_rewards(ai_offense, player_defense)
        # print(f"Your reward: {player_reward}")
        # print(f"AI reward: {ai_reward}\n")
        # print(f"Winner: {'You' if player_reward > ai_reward else 'AI'}\n\n")
        # ai.update_defense(player_defense)