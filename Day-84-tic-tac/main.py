
def choose_field(player_symbol):
    is_empty = False
    while not is_empty:
        player_row = int(input("Choose row you'd like to put your symbol (1-3): "))
        player_column = int(input("Choose column you'd like to put your symbol (1-3): "))
        if board[player_row - 1][player_column - 1] == " ":
            board[player_row - 1][player_column - 1] = player_symbol
            is_empty = True
        else:
            print("That field is already occupied, please try again")

    for row in board:
        print(row)

def check_winner(player_board):
    for row in player_board:
        if row[0] == row[1] == row[2] and row[0] != " ":
            winner = row[0]
            print(f"Player with symbol: {winner} wins!")
            return winner

    for col in range(3):
        if (
                player_board[0][col] == player_board[1][col] == player_board[2][col]
                and player_board[0][col] != " "
        ):
            winner = player_board[0][col]
            print(f"Player with symbol: {winner} wins!")
            return winner

    if (player_board[0][0] == player_board[1][1] == player_board[2][2]
            and player_board[0][0] != " "
    ):
        winner = player_board[0][0]
        print(f"Player with symbol: {winner} wins!")
        return winner

    if (player_board[0][2] == player_board[1][1] == player_board[2][0]
            and player_board[0][2] != " "
    ):
        winner = player_board[0][2]
        print(f"Player with symbol: {winner} wins!")
        return winner

    return None

def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    print("It's a draw!")
    return True

def wants_to_continue():
    while True:
        play_again = input("Would you like to play again? Type 'y' for yes or 'n' for no: ").lower()
        if play_again == 'y':
            return True
        elif play_again == 'n':
            return False
        else:
            print("Wrong input, please type 'y' for yes or 'n' for no.")

is_on = True
player1_symbol = "X"
player2_symbol = "O"

while is_on:
    board = [[' ' for _ in range(3)] for _ in range(3)]
    game_not_over = True
    while game_not_over:
        for symbol in [player1_symbol, player2_symbol]:
            choose_field(symbol)
            winning_player = check_winner(board)

            if winning_player or is_board_full(board):
                game_not_over = False

                is_on = wants_to_continue()
                break
