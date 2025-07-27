from turtle import Turtle

COLORS = ["red", "orange", "yellow"]


class BricksManager:
    def __init__(self):
        self.BricksManager = []

    def create_bricks(self):
        y_cor = 100
        for i in range(3):
            x_cor = -350
            for j in range(14):
                new_brick = Turtle("square")
                new_brick.penup()
                new_brick.shapesize(stretch_wid=1, stretch_len=2)
                new_brick.color(COLORS[i])
                new_brick.goto(x_cor, y_cor)
                self.BricksManager.append(new_brick)
                x_cor +=50
            y_cor += 30

    def clear_bricks(self):
        for brick in self.BricksManager:
            brick.hideturtle()
            brick.clear()
        self.BricksManager.clear()