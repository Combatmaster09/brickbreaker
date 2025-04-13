import globals
from Models.Brick import Brick
from pygame.math import Vector2
from utils import load_sprite
import random

class LevelManager:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.current_level = 1
        self.levels_data = self._generate_levels_data(10)  # Pre-generate 10 levels
        
    def _generate_levels_data(self, num_levels):
        """Generate data for multiple levels with increasing difficulty"""
        levels = []
        
        for level in range(1, num_levels + 1):
            level_data = {
                "rows": min(3 + level // 2, 10),  # Increase rows as level increases (max 10)
                "cols": min(5 + level // 3, 15),  # Increase columns as level increases (max 15)
                "brick_health": 1 + level // 3,  # Increase brick health every 3 levels
                "ball_speed": 5 + level * 0.5,  # Gradually increase ball speed
                "special_bricks": level // 2,  # Add special bricks in higher levels
            }
            levels.append(level_data)
        
        return levels
    
    def load_level(self, level_number):
        """Load a specific level"""
        if level_number > len(self.levels_data):
            # If we've gone beyond pre-generated levels, create a harder one
            level_data = self._generate_level_data(level_number)
        else:
            level_data = self.levels_data[level_number - 1]
        
        # Update global level
        globals.level = level_number
        self.current_level = level_number
        
        # Clear existing bricks
        self.game_instance.game_objects = [obj for obj in self.game_instance.game_objects if not isinstance(obj, Brick)]
        
        # Create new bricks based on level data
        bricks = self._create_level_bricks(level_data)
        
        # Add bricks to game objects
        for brick in bricks:
            self.game_instance.game_objects.append(brick)
        
        # Update ball speed
        for ball in [obj for obj in self.game_instance.game_objects if hasattr(obj, "VELOCITY")]:
            ball.VELOCITY = level_data["ball_speed"]
            
        return True
    
    def _create_level_bricks(self, level_data):
        """Create brick formation based on level data"""
        bricks = []
        rows = level_data["rows"]
        cols = level_data["cols"]
        
        # Calculate available space
        screen_width = self.game_instance.screen.get_width()
        
        # Set up brick dimensions
        if isinstance(globals.BRICK_SIZE, tuple):
            brick_width, brick_height = globals.BRICK_SIZE
        else:
            brick_width, brick_height = 50, 20
        
        # Add padding between bricks
        padding = 5
        
        # Calculate total width needed for bricks
        total_width = cols * (brick_width + padding) - padding
        
        # Calculate starting x position to center the brick formation
        start_x = (screen_width - total_width) // 2
        start_y = 50  # Start from the top with some margin
        
        # Create the grid of bricks
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (brick_width + padding)
                y = start_y + row * (brick_height + padding)
                
                # Determine brick health
                if random.random() < 0.2:  # 20% chance for a stronger brick
                    health = level_data["brick_health"] + 1
                else:
                    health = level_data["brick_health"]
                
                # Create the brick
                brick = Brick(Vector2(x, y), load_sprite("brick"), health)
                bricks.append(brick)
                
        return bricks
        
    def check_level_complete(self):
        """Check if all bricks are destroyed"""
        bricks = [obj for obj in self.game_instance.game_objects if isinstance(obj, Brick) and not obj.destroyed]
        
        if not bricks:
            # Level complete, load next level
            self.load_level(self.current_level + 1)
            return True
        
        return False