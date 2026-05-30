from game import play_game_session, choose_category

previous_score = 0
user_input = choose_category()

while True:
    previous_score = play_game_session(previous_score, user_input)