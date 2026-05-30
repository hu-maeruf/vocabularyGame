from game import play_game_session, choose_category

# Restarts the game
while True:
    previous_score = 0
    user_input = choose_category()
    session = 1

    # Plays 3 sessions
    while session < 4:
        previous_score = play_game_session(previous_score, user_input)
        session += 1

    play_again = input("Play again? (y/n): ").strip().lower()
    if play_again != "y":
        break