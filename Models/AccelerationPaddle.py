from .GameObject import gameobject
from pygame.math import Vector2
from utils import load_sprite

class acceleration_paddle(gameobject):
    ACCELERATION = 0.2  # Increased for more responsive acceleration
    FRICTION = 0.05     # Friction coefficient for deceleration
    MAX_SPEED = 10      # Maximum speed limit
    
    def __init__(self, position, create_ball_callback):
        self.create_bullet_callback = create_ball_callback
        self.direction = "none"  # Store current direction
        
        super().__init__(position, load_sprite("paddle"), Vector2(0))
        
    def move(self, direction="none", surface=None):
        # Apply acceleration based on direction
        if direction == "left":
            self.velocity.x -= self.ACCELERATION
            # Cap maximum speed
            if self.velocity.x < -self.MAX_SPEED:
                self.velocity.x = -self.MAX_SPEED
        elif direction == "right":
            self.velocity.x += self.ACCELERATION
            # Cap maximum speed
            if self.velocity.x > self.MAX_SPEED:
                self.velocity.x = self.MAX_SPEED
        else:  # "none" - gradually slow down with friction
            if abs(self.velocity.x) > 0:
                # Apply friction in the opposite direction of movement
                if self.velocity.x > 0:
                    self.velocity.x -= self.FRICTION
                    # Prevent overshooting zero
                    if self.velocity.x < 0:
                        self.velocity.x = 0
                else:
                    self.velocity.x += self.FRICTION
                    # Prevent overshooting zero
                    if self.velocity.x > 0:
                        self.velocity.x = 0
        
        # Update position if surface is provided
        if surface:
            self.position += self.velocity
            
            # Wrap around screen edges
            paddle_width = self.sprite.get_width()
            paddle_half_width = paddle_width / 2
            
            # Wrap around screen edges
            if self.position.x < -paddle_half_width:
                self.position.x = surface.get_width() + paddle_half_width
            elif self.position.x > surface.get_width() + paddle_half_width:
                self.position.x = -paddle_half_width
                
    def draw(self, screen):
        """Draw the paddle on the screen."""
        if hasattr(self, 'sprite') and self.sprite:
            screen.blit(self.sprite, (self.position.x - self.radius, self.position.y - self.radius))