from turtle import Turtle

FONT = ("Courier", 30, "normal")

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.color("white")
        self.penup()
        self.score = 0
        self.update_score()

    def increase_score(self, score_value):
        self.score += score_value
        self.update_score()

    def update_score(self):
        self.clear()
        self.goto(320, 250)
        self.write(f"{self.score}", align="center", font=FONT)

    def game_over(self, game_status):
        self.goto(0,30)
        self.write(game_status,
                   align="center", font=FONT)
        self.goto(0, 0)
        self.write("Would you like to play again?",
                   align="center", font=FONT)
        self.goto(0, -30)
        self.write("Press 'y' for yes or 'q' to quit the game!",
                   align="center", font=FONT)