from .GameObject import gameobject
from pygame.math import Vector2
from utils import load_sprite, load_sound
import globals
import random
from .Brick import Brick  # Import the Brick classq

class Ball(gameobject):
    VELOCITY = 5  # Constant velocity

    def __init__(self, position, create_ball_callback, paddle):
        self.create_bullet_callback = create_ball_callback
        self.paddle = paddle
        self.attached_to_paddle = True  # Start attached to paddle
        #self.bounce_sound = load_sound("bounce")
        
        super().__init__(position, load_sprite("ball"), Vector2(0))

    # In Ball.py, update the move method to avoid the AttributeError
    def move(self, surface=None, **kwargs):
        if self.attached_to_paddle and self.paddle:
            # If attached to paddle, move with the paddle
            self.position.x = self.paddle.position.x
            self.position.y = self.paddle.position.y - self.paddle.radius - self.radius
        else:
            # Normal movement
            previous_position = Vector2(self.position)
            self.position += self.velocity
            
            # Make sure surface is provided
            if surface is not None:
                # Bounce off walls
                if self.position.x <= self.radius:
                    self.position.x = self.radius  # Prevent sticking in the wall
                    self.velocity.x = abs(self.velocity.x)  # Always move right after hitting left wall
                    if hasattr(self, 'bounce_sound'):
                        self.bounce_sound.play()
                
                if self.position.x >= surface.get_width() - self.radius:
                    self.position.x = surface.get_width() - self.radius  # Prevent sticking in the wall
                    self.velocity.x = -abs(self.velocity.x)  # Always move left after hitting right wall
                    if hasattr(self, 'bounce_sound'):
                        self.bounce_sound.play()
                
                # Bounce off ceiling
                if self.position.y <= self.radius:
                    self.position.y = self.radius  # Prevent sticking in the ceiling
                    self.velocity.y = abs(self.velocity.y)  # Always move down after hitting ceiling
                    if hasattr(self, 'bounce_sound'):
                        self.bounce_sound.play()

                # Check if ball is below the screen (game over condition)
                if self.position.y > surface.get_height() + self.radius:
                    # Call the ball lost handler in the game instance
                    try:
                        from game import brickbreaker
                        game_instance = brickbreaker.get_instance()
                        if game_instance and hasattr(game_instance, 'handle_ball_lost'):
                            # Don't reset position here - let the handler do it
                            game_instance.handle_ball_lost()
                    except (ImportError, AttributeError):
                        # Fallback if handler not available
                        self.attached_to_paddle = True
                        self.velocity = Vector2(0, 0)
                        if self.paddle:
                            self.position.x = self.paddle.position.x
                            self.position.y = self.paddle.position.y - self.paddle.radius - self.radius
                
                # Check for paddle collision if paddle exists
                if self.paddle and self.collides_with(self.paddle):
                    # Bounce off paddle
                    self.handle_paddle_collision()
            
            # Get bricks directly from the game instance
            try:
                from game import brickbreaker
                game_instance = brickbreaker.get_instance()
                if game_instance:
                    # Use a safer method to get bricks
                    bricks = [obj for obj in game_instance._get_game_objects() 
                            if isinstance(obj, Brick) and not obj.destroyed]
                    self.check_brick_collisions(bricks, previous_position)
            except (ImportError, AttributeError) as e:
                # Print the error for debugging
                print(f"Error checking brick collisions: {e}")
                pass
            
    def launch(self):
        if self.attached_to_paddle:
            # Launch at an angle with constant vertical velocity
            self.velocity = Vector2(random.uniform(-1, 1), -1)  # Random horizontal component
            
            # Normalize and scale to maintain constant velocity
            self.velocity = self.velocity.normalize() * self.VELOCITY
            
            self.attached_to_paddle = False
            
    # In Ball.py, update the handle_paddle_collision method:
    def handle_paddle_collision(self):
        # Make sure the paddle exists
        if not self.paddle:
            return
            
        # Calculate bounce angle based on where ball hits the paddle
        hit_position = (self.position.x - self.paddle.position.x) / self.paddle.radius
        
        # Limit the hit_position between -1 and 1
        hit_position = max(-1, min(1, hit_position))
        
        # Calculate new velocity based on hit position
        # Middle of paddle: straight up (-90°)
        # Edge of paddle: angled bounce (±45°)
        angle = hit_position * 0.8  # 0.8 controls how extreme the angle can be
        
        # Set direction with constant speed
        self.velocity.x = self.VELOCITY * angle
        self.velocity.y = -self.VELOCITY * (1 - abs(angle) * 0.5)
        
        # Normalize to maintain constant speed
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * self.VELOCITY
        
        # Add a small amount of paddle's velocity to the ball for more intuitive control
        paddle_influence = 0.3  # How much the paddle's motion affects ball direction
        if hasattr(self.paddle, 'velocity'):
            self.velocity.x += self.paddle.velocity.x * paddle_influence
        
        # Ensure ball isn't inside paddle - move it above the paddle
        self.position.y = self.paddle.position.y - self.paddle.radius - self.radius - 1
        
        # Play bounce sound if available
        if hasattr(self, 'bounce_sound'):
            self.bounce_sound.play()
    
    def check_brick_collisions(self, bricks, previous_position):
        # Import here to avoid circular imports
        from Models.Brick import Brick
        
        collided_bricks = []
        
        for brick in bricks:
            if self.precise_collides_with(brick) and not brick.destroyed:
                collided_bricks.append(brick)
                
        if collided_bricks:
            # Find the closest brick - this should be the one that was actually hit
            closest_brick = min(collided_bricks, key=lambda b: self.position.distance_to(b.position))
            
            # Hit only the closest brick
            closest_brick.hit()
            globals.score += 10 * (globals.level + globals.score_multiplier)
            
            # Calculate collision direction more precisely
            relative_x = self.position.x - closest_brick.position.x
            relative_y = self.position.y - closest_brick.position.y
            
            # Get brick dimensions
            brick_width = closest_brick.sprite.get_width()
            brick_height = closest_brick.sprite.get_height()
            
            # Calculate normalized distances to each edge
            h_distance = abs(relative_x) / (brick_width/2 + self.radius)
            v_distance = abs(relative_y) / (brick_height/2 + self.radius)
            
            # Bounce in appropriate direction based on collision angle
            if h_distance > v_distance:
                # Horizontal collision (left/right sides)
                self.velocity.x = -self.velocity.x
                
                # Horizontal collision correction
                if relative_x > 0:
                    self.position.x = closest_brick.position.x + brick_width/2 + self.radius + 1
                else:
                    self.position.x = closest_brick.position.x - brick_width/2 - self.radius - 1
            else:
                # Vertical collision (top/bottom sides)
                self.velocity.y = -self.velocity.y
                
                # Vertical collision correction
                if relative_y > 0:
                    self.position.y = closest_brick.position.y + brick_height/2 + self.radius + 1
                else:
                    self.position.y = closest_brick.position.y - brick_height/2 - self.radius - 1
                    
    def precise_collides_with(self, other_obj):
        """A more precise rectangle-based collision detection"""
        # Get ball bounds
        ball_left = self.position.x - self.radius
        ball_right = self.position.x + self.radius
        ball_top = self.position.y - self.radius
        ball_bottom = self.position.y + self.radius
        
        # Get brick bounds (assuming the sprite's position is at its center)
        brick_width = other_obj.sprite.get_width()
        brick_height = other_obj.sprite.get_height()
        brick_left = other_obj.position.x - brick_width / 2
        brick_right = other_obj.position.x + brick_width / 2
        brick_top = other_obj.position.y - brick_height / 2
        brick_bottom = other_obj.position.y + brick_height / 2
        
        # Check for overlap
        return (ball_right >= brick_left and
                ball_left <= brick_right and
                ball_bottom >= brick_top and
                ball_top <= brick_bottom)