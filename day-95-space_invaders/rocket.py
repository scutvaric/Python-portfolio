from turtle import Turtle


class Rocket(Turtle):
    def __init__(self, screen, get_active):
        super().__init__()
        self.get_active = get_active
        self.screen = screen
        self.shape("square")
        self.shapesize(stretch_wid=0.8, stretch_len=0.1)
        self.penup()
        self.hideturtle()
        self.color("white")
        self.speed("fastest")
        self.move_y = 5
        self.firing = False
        self.is_active = False

    def fire(self, spaceship_xcor, spaceship_ycor):
        if self.is_active or not self.get_active():
            return
        self.is_active = True
        self.goto(spaceship_xcor, spaceship_ycor)
        self.showturtle()
        self.move_up()

    def reset_after_hit(self):
        self.hideturtle()
        self.is_active = False
        self.clear()
        self.goto(0, 340)

    def move_up(self):
        if not self.is_active or not self.get_active():
            return
        if self.ycor() < 300:
            self.sety(self.ycor() + self.move_y)
            self.screen.ontimer(self.move_up, 20)  # move again in 20ms
        else:
            self.hideturtle()
            self.is_active = False