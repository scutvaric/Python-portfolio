from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time
from bricks import BricksManager

# === Constants === #
COLORS = ["red", "orange", "yellow"]

# === Screen Setup=== #
screen = Screen()
screen.bgcolor("black")
screen.setup(800, 600)
screen.title("Pong Game")
screen.tracer(0)

# === Game objects === #
paddle = Paddle((0, -250))
ball = Ball()
scoreboard = Scoreboard()
bricks_manager = BricksManager()

# === Control Functions === #
def continue_game():
    bricks_manager.clear_bricks()
    bricks_manager.create_bricks()
    scoreboard.score = 0
    scoreboard.update_score()
    ball.reset_position()

def quit_game():
    global game_is_on
    game_is_on = False
    screen.bye()

def end_game(message):
    scoreboard.game_over(message)
    screen.onkey(continue_game, "y")
    screen.onkey(quit_game, "q")

# === Event listeners === #
screen.listen()
screen.onkey(paddle.move_left, "Left")
screen.onkey(paddle.move_right, "Right")

# === Start Game === #
bricks_manager.create_bricks()
screen.update()
game_is_on = True

# === Game Loop === #
while game_is_on:
    screen.update()
    time.sleep(ball.move_speed)

    ball.move()
    if ball.xcor() > 370 or ball.xcor() < -380:
        ball.bounce_x()

    if ball.distance(paddle) < 80 and ball.ycor() < -230:
        ball.bounce_y()
        ball.increase_speed()

    if ball.ycor() > 280:
        ball.bounce_y()

    for brick in bricks_manager.BricksManager[:]:
        if brick.distance(ball) < 30:
            for n in range(len(COLORS)):
                if brick.color()[0] == COLORS[n]:
                    scoreboard.increase_score(n+1)
            ball.bounce_y()
            brick.hideturtle()
            bricks_manager.BricksManager.remove(brick)

    if ball.ycor() < -280:
        end_game("GAME OVER")

    if not bricks_manager.BricksManager:
        end_game("CONGRATS, YOU WON")

screen.exitonclick()