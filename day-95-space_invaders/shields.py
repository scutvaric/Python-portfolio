from turtle import Turtle

BRICK_SIZE = 8      # px square
BRICK_SPACING = 2   # gap between bricks
BRICK_HITS = 3      # how many hits a brick takes

# A tiny square brick with HP that changes color and disappears when destroyed
class Brick(Turtle):
    def __init__(self, x, y, hp=BRICK_HITS):
        super().__init__(shape="square", visible=False)
        self.penup()
        self.color("lime")
        self.speed("fastest")
        self.shapesize(stretch_wid=BRICK_SIZE/20, stretch_len=BRICK_SIZE/20)
        self.hp = hp
        self.goto(x, y)
        self._update_color()
        self.showturtle()

    def _update_color(self):
        # simple damage tint
        if self.hp >= 3: self.color("lime")
        elif self.hp == 2: self.color("yellow")
        else: self.color("orange")

    def hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.hideturtle()
            self.clear()
            return True  # destroyed
        else:
            self._update_color()
            return False  # still alive

class ShieldManager:
    """
    Builds 2–4 shields between ship and aliens.
    - call create_shields() once at start (or on restart)
    - call check_player_rocket_hit(rocket)
    - call check_enemy_rockets_hit(rockets_pool)
    """
    def __init__(self, screen):
        self.screen = screen
        self.bricks = []

        # 1/0 mask; 1 = place a brick
        # This draws a classic arch with a notch so shots can pass
        self.MASK = [
            [0,1,1,1,1,1,1,1,0],
            [1,1,1,1,1,1,1,1,1],
            [1,1,1,1,0,1,1,1,1],
            [1,1,1,0,0,0,1,1,1],
        ]

    def clear(self):
        for b in self.bricks:
            b.hideturtle()
            b.clear()
        self.bricks.clear()

    def create_shields(self, count=3, y=-160, left_x=-260, gap=260):
        """
        Make `count` shields placed horizontally.
        y: vertical position (between ship ~-250 and aliens ~100)
        """
        self.clear()
        for i in range(count):
            origin_x = left_x + i * gap
            self._build_mask_at(origin_x, y)

    def _build_mask_at(self, origin_x, origin_y):
        rows = len(self.MASK)
        cols = len(self.MASK[0])
        cell = BRICK_SIZE + BRICK_SPACING
        for r in range(rows):
            for c in range(cols):
                if self.MASK[r][c]:
                    x = origin_x + (c - cols//2) * cell
                    y = origin_y + (rows//2 - r) * cell
                    self.bricks.append(Brick(x, y))

    # ---- collision helpers ----
    def _hit_test(self, sprite, radius=10):
        """
        Returns a brick that collides with `sprite` (Turtle) or None.
        radius is a simple distance threshold.
        """
        sx, sy = sprite.xcor(), sprite.ycor()
        for b in self.bricks:
            if b.isvisible() and b.distance(sx, sy) < radius:
                return b
        return None

    def check_player_rocket_hit(self, rocket, destroy_rocket=True):
        """Call this every frame: rocket vs shields."""
        if not rocket.isvisible():
            return False
        b = self._hit_test(rocket, radius=BRICK_SIZE)
        if b:
            destroyed = b.hit()
            if destroyed:
                self.bricks.remove(b)
            if destroy_rocket:
                rocket.reset_after_hit()
            return True
        return False

    def check_enemy_rockets_hit(self, rockets_pool, destroy_rocket=True):
        """Call this every frame for each active enemy rocket."""
        hit_any = False
        for r in rockets_pool:
            if not getattr(r, "is_active", False) or not r.isvisible():
                continue
            b = self._hit_test(r, radius=BRICK_SIZE)
            if b:
                destroyed = b.hit()
                if destroyed:
                    self.bricks.remove(b)
                if destroy_rocket:
                    r.reset_after_hit()
                hit_any = True
        return hit_any