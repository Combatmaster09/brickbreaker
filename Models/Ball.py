from GameObject import gameobject
from pygame.math import Vector2
from utils import load_sprite

class ball(gameobject):
    VELOCITY = 3
    def __init__(self, position, create_ball_callback):
        self.create_bullet_callback = create_ball_callback
        
        super().__init__(position, load_sprite("ball"), Vector2(0))
        
