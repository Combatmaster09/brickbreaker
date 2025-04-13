from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import load_sound, load_sprite, wrap_position
import globals

UP = Vector2(0, -1)

class gameobject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)
        
    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def collides_with(self, other_obj):
        # Check if other_obj is None before trying to access its attributes
        if other_obj is None:
            return False
            
        # Make sure both objects have position and radius attributes
        if not hasattr(other_obj, 'position') or not hasattr(other_obj, 'radius'):
            return False
            
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius
    def move(x, y):
        pass