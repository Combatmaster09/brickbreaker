from GameObject import gameobject
from pygame.math import Vector2
from utils import load_sprite

class velocity_paddle(gameobject):
    VELOCITY = 1
    def __init__(self, position, create_ball_callback):
        self.create_bullet_callback = create_ball_callback
        
        super().__init__(position, load_sprite("paddle"), Vector2(0))
        
    def move_right(self):
        self.velocity = self.VELOCITY
    def move_left(self):
        self.velocity = self.VELOCITY * -1