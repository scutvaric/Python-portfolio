from turtle import Turtle, register_shape

# --- Register alien animation frames (two per row) ---
ALIEN_FRAMES = {
    1: [ "img/alien1a.gif", "img/alien1b.gif" ],
    2: [ "img/alien2a.gif", "img/alien2b.gif" ],
    3: [ "img/alien3a.gif", "img/alien3b.gif" ],
}
for row_frames in ALIEN_FRAMES.values():
    for path in row_frames:
        register_shape(path)

# --- Explosion frames (already in your code) ---
EXPLOSION_FRAMES = [f"img/explosion{i}.gif" for i in range(1, 4)]
for path in EXPLOSION_FRAMES:
    register_shape(path)

class AlienManager:
    def __init__(self, screen, get_active):
        self.get_active = get_active
        self.screen = screen
        self.AliensManager = []
        self.move_x = 10
        self.move_y = 5
        self.move_speed = 0.7

        # animation settings
        self.anim_rate_ms = 120
        self.animating = False

    def create_aliens(self):
        y_cor = 100
        for row in range(3):
            x_cor = -300
            alien_score = row + 1
            row_frames = ALIEN_FRAMES[alien_score]
            for _ in range(10):
                new_alien = Turtle(row_frames[0])  # start on first frame
                new_alien.penup()
                new_alien.goto(x_cor, y_cor)
                new_alien.score = alien_score
                new_alien.frames = row_frames[:]   # attach its 2-frame set
                new_alien.frame_idx = 0
                new_alien.exploding = False        # animator should skip when True
                self.AliensManager.append(new_alien)
                x_cor += 60
            y_cor += 50

    def clear_aliens(self):
        for alien in self.AliensManager:
            alien.hideturtle()
            alien.clear()
        self.AliensManager.clear()

    # ---------- Movement ----------
    def move_aliens(self):
        if not self.get_active():
            return
        hit_edge = any(
            alien.xcor() + self.move_x > 360 or alien.xcor() + self.move_x < -360
            for alien in self.AliensManager
        )
        if hit_edge:
            self.go_row_down()
            self.change_direction()
            self.increase_speed()
        else:
            for alien in self.AliensManager:
                new_xcor = alien.xcor() + self.move_x
                alien.goto(new_xcor, alien.ycor())

        self.screen.ontimer(self.move_aliens, int(self.move_speed * 1000))

    def change_direction(self):
        self.move_x *= -1

    def go_row_down(self):
        for alien in self.AliensManager:
            alien.goto(alien.xcor(), alien.ycor() - self.move_y)

    def increase_speed(self):
        self.move_speed *= 0.9

    # ---------- Animation ----------
    def animate_aliens(self):
        """Flip visible, non-exploding aliens between their two frames."""
        if not self.get_active():
            # Try again soon while paused (keeps timer chain alive)
            self.screen.ontimer(self.animate_aliens, self.anim_rate_ms)
            return

        for alien in self.AliensManager:
            if alien.isvisible() and not alien.exploding and hasattr(alien, "frames"):
                alien.frame_idx = 1 - getattr(alien, "frame_idx", 0)
                alien.shape(alien.frames[alien.frame_idx])

        self.screen.ontimer(self.animate_aliens, self.anim_rate_ms)

    def start_animation(self):
        if not self.animating:
            self.animating = True
            self.animate_aliens()

    # ---------- Explosion ----------
    def explode_alien(self, alien, frame_idx=0):
        """Swap alien sprite through explosion frames, then remove it."""
        alien.exploding = True  # prevent animator from flipping its sprite
        alien.shape(EXPLOSION_FRAMES[frame_idx])

        next_idx = frame_idx + 1
        if next_idx < len(EXPLOSION_FRAMES):
            self.screen.ontimer(lambda: self.explode_alien(alien, next_idx), 60)
        else:
            alien.hideturtle()
            if alien in self.AliensManager:
                self.AliensManager.remove(alien)

