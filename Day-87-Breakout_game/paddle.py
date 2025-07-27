from turtle import Turtle

class Paddle(Turtle):
    def __init__(self, position):
        super().__init__()
        self.color("White")
        self.penup()
        self.shape("square")
        self.shapesize(stretch_wid=1, stretch_len=10)
        self.goto(position)

    def move_right(self):
        if self.xcor() < 300:
            new_x_cor = self.xcor() + 20
            self.goto(new_x_cor, self.ycor())

    def move_left(self):
        if self.xcor() > -300:
            new_x_cor = self.xcor() - 20
            self.goto(new_x_cor, self.ycor())