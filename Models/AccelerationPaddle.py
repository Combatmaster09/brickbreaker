from .GameObject import gameobject
from pygame.math import Vector2
from utils import load_sprite, wrap_position

class acceleration_paddle(gameobject):
    ACCELERATION = 0.1
    FRICTION = 0.02  # Friction coefficient for deceleration
    
    def __init__(self, position, create_ball_callback):
        self.create_bullet_callback = create_ball_callback
        
        super().__init__(position, load_sprite("paddle"), Vector2(0))
        
    def move(self, direction="none", surface=None):
        # Apply acceleration based on direction
        if direction == "left":
            self.velocity.x -= self.ACCELERATION
        elif direction == "right":
            self.velocity.x += self.ACCELERATION
        else:  # "none" - gradually slow down with friction
            if abs(self.velocity.x) > 0:
                friction_force = -self.FRICTION * (self.velocity.x / abs(self.velocity.x))
                self.velocity.x += friction_force
                # Stop completely if velocity is very small
                if abs(self.velocity.x) < self.FRICTION:
                    self.velocity.x = 0
        
        # Update position if surface is provided
        if surface:
            self.position += self.velocity
            
            # Wrap around screen edges
            paddle_width = self.sprite.get_width()
            if self.position.x < 0:
                self.position.x = surface.get_width()
            elif self.position.x > surface.get_width():
                self.position.x = 0