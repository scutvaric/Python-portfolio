from turtle import Turtle
import random

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.color("white")
        self.speed("fastest")
        self.move_x = 10
        self.move_y = 10
        self.reset_position()
        self.move_speed = 0.1

    def move(self):
        new_xcor = self.xcor() + self.move_x
        new_ycor = self.ycor() + self.move_y
        self.goto(new_xcor, new_ycor)

    def increase_speed(self):
        self.move_speed *= 0.9

    def bounce_y(self):
        self.move_y *= -1

    def bounce_x(self):
        self.move_x *= -1

    def reset_position(self):
        self.goto(random.randint(-300,300),0)
        self.bounce_x()
        self.move_speed = 0.1
