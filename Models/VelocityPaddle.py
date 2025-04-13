from .GameObject import gameobject
from pygame.math import Vector2
from utils import load_sprite

class velocity_paddle(gameobject):
    VELOCITY = 5
    def __init__(self, position, create_ball_callback):
        self.create_bullet_callback = create_ball_callback
        
        super().__init__(position, load_sprite("paddle"), Vector2(0))
    
    def move(self, direction="none", surface=None):
        # Handle movement based on direction
        if direction == "left":
            self.velocity = Vector2(-self.VELOCITY, 0)
        elif direction == "right":
            self.velocity = Vector2(self.VELOCITY, 0)
        else:  # "none" or any other value
            self.velocity = Vector2(0, 0)
        
        # Update position if surface is provided
        if surface:
            self.position += self.velocity
            
            # Keep paddle within screen boundaries - no wrapping
            paddle_width = self.sprite.get_width()
            if self.position.x < paddle_width / 2:
                self.position.x = paddle_width / 2
            elif self.position.x > surface.get_width() - paddle_width / 2:
                self.position.x = surface.get_width() - paddle_width / 2