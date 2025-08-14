from turtle import Turtle
import random

class EnemyRocket(Turtle):
    def __init__(self, screen, aliens_manager, get_active):
        super().__init__()
        self.get_active = get_active
        self.aliens_manager = aliens_manager
        self.screen = screen
        self.shape("square")
        self.shapesize(stretch_wid=0.8, stretch_len=0.1)
        self.penup()
        self.hideturtle()
        self.color("white")
        self.speed("fastest")
        self.move_y = -10
        self.firing = False
        self.is_active = False

    def fire(self):
        if self.is_active:
            return
            # only pick alive/visible aliens
        candidates = [a for a in self.aliens_manager if a.isvisible()]
        if not candidates:
            return
        alien = random.choice(candidates)

        self.is_active = True
        self.goto(alien.xcor(), alien.ycor())
        self.showturtle()
        self.move_down()

    def reset_after_hit(self):
        self.hideturtle()
        self.is_active = False
        self.clear()
        self.goto(0, 340)

    def move_down(self):
        if not self.is_active or not self.get_active():
            return
        if self.ycor() > -300:
            self.sety(self.ycor() + self.move_y)
            self.screen.ontimer(self.move_down, 20)  # move again in 20ms
        else:
            self.hideturtle()
            self.is_active = False