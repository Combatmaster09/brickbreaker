import pygame
from pygame.math import Vector2
from pygame.transform import rotozoom
from .GameObject import gameobject

from utils import load_sound, load_sprite
import globals

UP = Vector2(0, -1)

class Brick(gameobject):
    def __init__(self, position, sprite, health=1):
        # Convert grid coordinates to pixel coordinates
        self.position = Vector2(position)
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
            self.destroyed = True
            # Play a sound effect for breaking the brick
            try:
                break_sound = load_sound("brick_break")
                break_sound.play()
            except:
                # If sound fails, just mark as destroyed
                pass
    # In Brick.py, update the draw method:
    def draw(self, surface):
        # Draw the brick with color based on health
        if self.health == 1:
            color = (255, 0, 0)  # Red for 1 health
        elif self.health == 2:
            color = (255, 165, 0)  # Orange for 2 health
        elif self.health == 3:
            color = (255, 255, 0)  # Yellow for 3 health
        else:
            color = (0, 255, 0)  # Green for 4+ health
        
        # Create a rect for the brick
        brick_width = self.sprite.get_width()
        brick_height = self.sprite.get_height()
        rect = pygame.Rect(
            self.position.x - brick_width / 2,
            self.position.y - brick_height / 2,
            brick_width,
            brick_height
        )
        
        # Draw the brick
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, (255, 255, 255), rect, 1)  # White border
        
        # Optionally show health number for higher health bricks
        if self.health > 1:
            font = pygame.font.Font(None, 24)
            text_surf = font.render(str(self.health), True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.position)
            surface.blit(text_surf, text_rect)