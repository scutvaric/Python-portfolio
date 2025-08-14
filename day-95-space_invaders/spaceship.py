from turtle import Turtle, register_shape

# Register both frames
register_shape("img/spaceship_a.gif")
register_shape("img/spaceship_b.gif")

EXPLOSION_FRAMES = [f"img/explosion{i}.gif" for i in range(1, 4)]
for path in EXPLOSION_FRAMES:
    register_shape(path)

class Spaceship(Turtle):
    def __init__(self, position, get_active, anim_rate_ms=120):
        super().__init__()
        self.get_active = get_active
        self.penup()
        self.color("white")
        self.frames = ["img/spaceship_a.gif", "img/spaceship_b.gif"]
        self.frame_idx = 0
        self.shape(self.frames[self.frame_idx])
        self.goto(position)

        # animation
        self.anim_rate_ms = anim_rate_ms
        self._anim_running = False

    # --- movement ---
    def move_right(self):
        if not self.get_active():
            return
        if self.xcor() < 380:
            self.goto(self.xcor() + 20, self.ycor())

    def move_left(self):
        if not self.get_active():
            return
        if self.xcor() > -380:
            self.goto(self.xcor() - 20, self.ycor())

    # --- animation ---
    def _animate(self):
        if not self._anim_running:
            return
        if self.get_active():
            self.frame_idx = 1 - self.frame_idx
            self.shape(self.frames[self.frame_idx])
        self.screen.ontimer(self._animate, self.anim_rate_ms)

    def start_animation(self):
        if not self._anim_running:
            self._anim_running = True
            self._animate()

    def stop_animation(self):
        self._anim_running = False

    # --- explosion ---
    def explode(self, frame_idx=0):
        self.stop_animation()  # stop flicker while exploding
        self.shape(EXPLOSION_FRAMES[frame_idx])
        next_idx = frame_idx + 1
        if next_idx < len(EXPLOSION_FRAMES):
            self.screen.ontimer(lambda: self.explode(next_idx), 60)
        else:
            self.hideturtle()
            self.shape(self.frames[0]); self.start_animation()