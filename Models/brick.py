from pygame.math import Vector2
from pygame.transform import rotozoom
from GameObject import GameObject

from utils import load_sound, load_sprite
import globals

UP = Vector2(0, -1)

class Brick(GameObject):
    def __init__(self, position, sprite, health=1):
        # Convert grid coordinates to pixel coordinates
        self.position = Vector2(position) * globals.BRICK_SIZE 
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(0, 0)  # Bricks don't move
        self.health = health
        self.destroyed = False

    def update(self):
        if self.health <= 0:
            self.destroyed = True

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            # Play a sound effect for breaking the brick
            break_sound = load_sound("brick_break.wav")
            break_sound.play()

# Function to create a brick formation
def create_brick_formation(rows, cols):
    bricks = []
    for row in range(rows):
        for col in range(cols):
            position = (col, row)  # Grid coordinates
            bricks.append(Brick(position, load_sprite("brick_sprite.png")))
    return bricks