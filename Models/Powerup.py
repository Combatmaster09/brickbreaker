import pygame
import random
from pygame.math import Vector2
from .GameObject import gameobject
from utils import load_sprite

class Powerup(gameobject):
    FALL_SPEED = 3  # Speed at which powerups fall
    TYPES = ["multiball", "slowball", "fastball", "extralife"]
    
    def __init__(self, position, powerup_type=None):
        # If no type specified, choose a random one
        if powerup_type is None:
            powerup_type = random.choice(self.TYPES)
        
        self.powerup_type = powerup_type
        # Load appropriate sprite based on powerup type
        sprite = load_sprite("powerup_" + powerup_type, True)
        
        # Fallback if sprite doesn't exist
        if sprite is None:
            # Create a colored circle as fallback
            color = self._get_color_for_type(powerup_type)
            surface = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(surface, color, (10, 10), 10)
            sprite = surface
            
        super().__init__(position, sprite, Vector2(0, self.FALL_SPEED))
        self.active = True
    
    def _get_color_for_type(self, powerup_type):
        """Return color based on powerup type"""
        colors = {
            "shrink": (0, 0, 255),      # Blue for paddle shrinking
            "multiball": (255, 255, 0),  # Yellow for multiball
            "slowball": (0, 255, 0),    # Green for slow ball
            "fastball": (255, 0, 255),  # Magenta for fast ball
            "extralife": (255, 255, 255) # White for extra life
        }
        return colors.get(powerup_type, (150, 150, 150))
    
    def move(self, surface=None):
        """Move the powerup down the screen"""
        self.position += self.velocity
        
        # Check if powerup is below the screen
        if surface and self.position.y > surface.get_height() + self.radius:
            self.active = False
    
    def apply_effect(self, game_instance):
        """Apply the powerup effect"""
        # Increased duration from 10000ms to 20000ms (20 seconds)
        powerup_duration = 20000
        
        '''if self.powerup_type == "expand":
            # Expand paddle
            for obj in game_instance.game_objects:
                if hasattr(obj, 'sprite') and (isinstance(obj, game_instance.paddle.__class__)):
                    # Increase paddle size by 50%
                    current_width = obj.sprite.get_width()
                    current_height = obj.sprite.get_height()
                    new_width = int(current_width * 1.5)
                    new_sprite = pygame.transform.scale(obj.sprite, (new_width, current_height))
                    obj.sprite = new_sprite
                    # Update radius to match the new width
                    obj.radius = new_width / 2
                    # Set a timer to revert after 20 seconds
                    pygame.time.set_timer(pygame.USEREVENT + 1, powerup_duration)'''
        
        '''if self.powerup_type == "shrink":
            # Shrink paddle
            for obj in game_instance.game_objects:
                if hasattr(obj, 'sprite') and (isinstance(obj, game_instance.paddle.__class__)):
                    # Decrease paddle size by 25%
                    current_width = obj.sprite.get_width()
                    current_height = obj.sprite.get_height()
                    new_width = max(int(current_width * 0.75), 30)  # Minimum width of 30
                    new_sprite = pygame.transform.scale(obj.sprite, (new_width, current_height))
                    obj.sprite = new_sprite
                    # Update radius to match the new width
                    obj.radius = new_width / 2
                    # Set a timer to revert after 20 seconds
                    pygame.time.set_timer(pygame.USEREVENT + 2, powerup_duration)'''
        
        # Similar modifications for slowball and fastball
        if self.powerup_type == "slowball":
            # Slow down all balls
            for obj in game_instance.game_objects:
                if hasattr(obj, 'VELOCITY') and hasattr(obj, 'velocity'):
                    # Slow ball by 30%
                    obj.VELOCITY = max(obj.VELOCITY * 0.7, 2)  # Minimum velocity of 2
                    # Preserve direction but adjust speed
                    if obj.velocity.length() > 0:
                        obj.velocity = obj.velocity.normalize() * obj.VELOCITY
                    # Set a timer to revert after 20 seconds
                    pygame.time.set_timer(pygame.USEREVENT + 3, powerup_duration)
        
        elif self.powerup_type == "fastball":
            # Speed up all balls
            for obj in game_instance.game_objects:
                if hasattr(obj, 'VELOCITY') and hasattr(obj, 'velocity'):
                    # Speed up ball by 30%
                    obj.VELOCITY = obj.VELOCITY * 1.3
                    # Preserve direction but adjust speed
                    if obj.velocity.length() > 0:
                        obj.velocity = obj.velocity.normalize() * obj.VELOCITY
                    # Set a timer to revert after 20 seconds
                    pygame.time.set_timer(pygame.USEREVENT + 4, powerup_duration)
        
        # No timer for multiball and extralife as they're one-time effects
        elif self.powerup_type == "multiball":
            # Create two additional balls and immediately launch them
            from Models.Ball import Ball
            
            # Get the current paddle
            paddle = game_instance.paddle if hasattr(game_instance, 'paddle') else None
            
            # Create and launch two new balls
            for i in range(2):
                # Create a new ball
                new_ball = game_instance._create_ball_callback()
                
                # Check if ball was created successfully
                if new_ball and isinstance(new_ball, Ball):
                    # Launch the ball immediately
                    new_ball.launch()
        
        elif self.powerup_type == "extralife":
            # Add an extra life
            if hasattr(game_instance, 'score_manager'):
                game_instance.score_manager.lives += 1