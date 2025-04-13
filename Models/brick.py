import pygame
import random
from pygame.math import Vector2
from pygame.transform import rotozoom
from .GameObject import gameobject
from .Powerup import Powerup  # Import the Powerup class

from utils import load_sound, load_sprite
import globals

UP = Vector2(0, -1)

class Brick(gameobject):
    # In Models/Brick.py
    def __init__(self, position, sprite, health=1, powerup_chance=0.2, powerup_type=None):
        # Convert grid coordinates to pixel coordinates
        self.position = Vector2(position)
        self.powerup_type = powerup_type
        
        # Load appropriate sprite based on powerup type
        if powerup_type:
            color_map = {
                "fastball": "red_brick",
                "slowball": "blue_brick",
                "expand": "yellow_brick",
                "shrink": "orange_brick",
                "multiball": "pink_brick",
                "extralife": "green_brick"
            }
            sprite_name = color_map.get(powerup_type, "brick")
            self.sprite = load_sprite(sprite_name)
        else:
            self.sprite = sprite
        
        self.radius = self.sprite.get_width() / 2
        self.velocity = Vector2(0, 0)  # Bricks don't move
        self.health = health
        self.destroyed = False
        self.powerup_chance = powerup_chance  # Chance to spawn a powerup

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
                
            # Try to spawn a powerup
            self._try_spawn_powerup()
    
    def _try_spawn_powerup(self):
        # Spawn a powerup with the defined chance
        if random.random() < self.powerup_chance:
            try:
                from game import brickbreaker
                game_instance = brickbreaker.get_instance()
                if game_instance:
                    powerup = Powerup(self.position, self.powerup_type)
                    game_instance.game_objects.append(powerup)
            except (ImportError, AttributeError) as e:
                print(f"Error spawning powerup: {e}")

    def draw(self, surface):
        if not self.destroyed:
            blit_position = self.position - Vector2(self.radius)
            surface.blit(self.sprite, blit_position)
            
            # Optionally show health number for higher health bricks
            if self.health > 1:
                font = pygame.font.Font(None, 24)
                text_surf = font.render(str(self.health), True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=self.position)
                surface.blit(text_surf, text_rect)