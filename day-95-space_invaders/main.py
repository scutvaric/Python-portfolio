from turtle import Screen
from spaceship import Spaceship
from rocket import Rocket
from scoreboard import Scoreboard
from enemy_rocket import EnemyRocket
from aliens import AlienManager
from shields import ShieldManager
import random

# === Constants === #
COLORS = ["red", "orange", "yellow"]

# === Screen Setup=== #
screen = Screen()
screen.bgcolor("black")
screen.setup(800, 600)
screen.title("Space invaders")
screen.tracer(0)

# === Game settings === #
game_is_on = True
game_active = True

# === Control Functions === #
def continue_game():
    """Restart a fresh round."""
    global game_active, stop_fire, rockets_pool
    game_active = True

    # Reset world
    alien_manager.clear_aliens()
    alien_manager.create_aliens()
    alien_manager.start_animation()
    spaceship.showturtle()
    scoreboard.score = 0
    scoreboard.update_score()
    rocket.reset_after_hit()
    shields.clear()
    shields.create_shields(count=3, y=-160)

    # Reset all enemy rockets
    for r in rockets_pool:
        r.reset_after_hit()

    # (Re)start enemy fire waves
    stop_fire = start_enemy_fire(screen, is_game_active, rockets_pool)

    # Resume alien movement and ticking
    alien_manager.move_aliens()

def quit_game():
    global game_is_on
    game_is_on = False
    try:
        stop_fire()  # stop timers cleanly if possible
    except:
        pass
    screen.bye()

def end_game(message):
    """Pause gameplay, show message, and allow restart/quit."""
    global game_active
    game_active = False
    scoreboard.game_over(message)

    # stop new enemy waves; current in-flight rockets will be reset on restart
    try:
        stop_fire()
    except:
        pass

    screen.onkey(continue_game, "y")
    screen.onkey(quit_game, "q")

def is_game_active():
    return game_active

def game_tick():
    screen.update()

    if game_active:
        # Player rocket vs aliens
        # Player rocket vs shields
        shields.check_player_rocket_hit(rocket)

        # Enemy rockets vs shields
        shields.check_enemy_rockets_hit(rockets_pool)

        for alien in alien_manager.AliensManager[:]:
            if alien.distance(rocket) < 30:
                scoreboard.increase_score(alien.score)
                rocket.reset_after_hit()
                alien_manager.explode_alien(alien)

        # Enemy rockets vs spaceship (any active rocket)
        for er in rockets_pool:
            if er.is_active and spaceship.distance(er) < 20:
                spaceship.explode()
                er.reset_after_hit()
                end_game("YOU HAVE LOST!")
                break

        # Win condition
        if not alien_manager.AliensManager:
            end_game("CONGRATS, YOU WON")

    # schedule next frame only if the app is still open
    if game_is_on:
        screen.ontimer(game_tick, 16)  # ~60 FPS

def create_enemy_rocket_pool(screen, aliens_manager, get_active, pool_size=8):
    return [EnemyRocket(screen, aliens_manager, get_active) for _ in range(pool_size)]

# Start random waves of 1..4 rockets. Returns a stop() function.
def start_enemy_fire(screen, get_active, rockets,
                     min_delay=600, max_delay=1600):
    state = {"running": True}

    def wave():
        if not state["running"]:
            return
        if not get_active():
            # game paused: try again soon
            screen.ontimer(wave, 300)
            return

        idle = [r for r in rockets if not r.is_active]
        if idle:
            k = random.randint(1, min(4, len(idle)))
            shooters = random.sample(idle, k)
            for r in shooters:
                r.fire()

        # schedule next wave at a random time
        delay = random.randint(min_delay, max_delay)
        screen.ontimer(wave, delay)

    wave()  # kick off immediately

    def stop():
        state["running"] = False
        for r in rockets:
            r.reset_after_hit()

    return stop

# === Game objects === #
spaceship = Spaceship((0, -250), is_game_active)
rocket = Rocket(screen, is_game_active)
scoreboard = Scoreboard()
alien_manager = AlienManager(screen, is_game_active)
rockets_pool = create_enemy_rocket_pool(screen,
                                   alien_manager.AliensManager,  # the list of aliens
                                   is_game_active)
stop_fire = start_enemy_fire(screen, is_game_active, rockets_pool)
shields = ShieldManager(screen)
shields.create_shields(count=3, y=-160)

# === Event listeners === #
screen.listen()
screen.onkey(spaceship.move_left, "Left")
screen.onkey(spaceship.move_right, "Right")
screen.onkey(lambda: rocket.fire(spaceship.xcor(), spaceship.ycor()), "space")

# === Start Game === #
alien_manager.create_aliens()
alien_manager.start_animation()
alien_manager.move_aliens()
spaceship.start_animation()
screen.update()
game_tick()
screen.mainloop()