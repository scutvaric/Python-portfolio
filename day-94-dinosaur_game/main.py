import pyautogui
import time

screen_w, screen_h = pyautogui.size()
shot_w, shot_h = pyautogui.screenshot().size
scale = shot_w / screen_w
# 1. Let the user switch to the game window
print("Starting in 3 seconds... Switch to Chrome Dinosaur Game.")
time.sleep(3)

dino_box = pyautogui.locateOnScreen("dino.png", confidence=0.8)
if not dino_box:
    print("Could not find the dino on screen!")
    exit()

print("Dino found at:", dino_box)
dino_left = int(dino_box.left / scale)
dino_top = int(dino_box.top / scale)
dino_width = int(dino_box.width / scale)
dino_height = int(dino_box.height / scale)

# Set scan position slightly in front of dino
scan_x = dino_left + dino_width + 90      # small gap in front
scan_y = dino_top + int(dino_height * 0.1)

pyautogui.press('space')  # Start the game

def is_night_mode():
    # Sample a pixel in the scan area
    px = pyautogui.screenshot(region=(scan_x, scan_y, 1, 1)).getpixel((0, 0))
    r, g, b = px[:3]
    # Night mode: background is dark, so r/g/b are small
    return r < 128 and g < 128 and b < 128

while True:
    night = is_night_mode()
    screenshot = pyautogui.screenshot(region=(scan_x, scan_y, 30, 30))
    pixels = screenshot.load()

    obstacle_found = False
    for x in range(screenshot.width):
        for y in range(screenshot.height):
            r, g, b, a = pixels[x, y]

            if night:
                # Night mode: obstacles are light, background is dark
                if (r, g, b) != (0, 0, 0):
                    pyautogui.press('space')
                    obstacle_found = True
                    break
            else:
                if (r, g, b) != (255, 255, 255):
                    pyautogui.press('space') # Cooldown
                    obstacle_found = True
                    break
        if obstacle_found:
            break
    time.sleep(0.01)