from .GameObject import gameobject
from pygame.math import Vector2
from utils import load_sprite, load_sound
from Models.AccelerationPaddle import acceleration_paddle
from Models.VelocityPaddle import velocity_paddle
from Models.Brick import Brick
import globals
import random

class Ball(gameobject):
    VELOCITY = 5  # Constant velocity

    def __init__(self, position, create_ball_callback, paddle):
        self.create_bullet_callback = create_ball_callback
        self.paddle = paddle
        self.attached_to_paddle = True  # Start attached to paddle
        #self.bounce_sound = load_sound("bounce")
        
        super().__init__(position, load_sprite("ball"), Vector2(0))

    def move(self, surface=None, **kwargs):
        if self.attached_to_paddle and self.paddle:
            # If attached to paddle, move with the paddle
            self.position.x = self.paddle.position.x
            self.position.y = self.paddle.position.y - self.paddle.radius - self.radius
        else:
            # Normal movement
            previous_position = Vector2(self.position)
            self.position += self.velocity
            
            # Bounce off walls
            if self.position.x <= self.radius or self.position.x >= surface.get_width() - self.radius:
                self.velocity.x = -self.velocity.x
                #self.bounce_sound.play()
            
            # Bounce off ceiling
            if self.position.y <= self.radius:
                self.velocity.y = -self.velocity.y
                #self.bounce_sound.play()
                
            # Check if ball is below the screen (game over condition)
            if self.position.y > surface.get_height() + self.radius:
                # Reset ball to paddle
                self.attached_to_paddle = True
                self.velocity = Vector2(0, 0)
            
            # Check for paddle collision
            if self.collides_with(self.paddle):
                # Bounce off paddle with angle based on where it hit
                self.handle_paddle_collision()
            
            # Get game objects from the game instance
            from game import brickbreaker
            game_objects = [obj for obj in brickbreaker.get_instance().game_objects 
                            if isinstance(obj, Brick) and not obj.destroyed]
            
            # Check for brick collisions
            self.check_brick_collisions(game_objects, previous_position)
    
    def launch(self):
        if self.attached_to_paddle:
            # Launch at an angle with constant vertical velocity
            self.velocity = Vector2(random.uniform(-1, 1), -1)  # Random horizontal component
            
            # Normalize and scale to maintain constant velocity
            self.velocity = self.velocity.normalize() * self.VELOCITY
            
            self.attached_to_paddle = False

    def handle_paddle_collision(self):
        # Calculate bounce angle based on where ball hits the paddle
        hit_position = (self.position.x - self.paddle.position.x) / self.paddle.radius
        
        # Limit the hit_position between -1 and 1
        hit_position = max(-1, min(1, hit_position))
        
        # Adjust angle based on hit position
        angle_factor = hit_position * 0.5  # Controls maximum angle
        
        # Always bounce upward with adjusted angle
        self.velocity.y = -abs(self.velocity.y)
        self.velocity.x = self.VELOCITY * angle_factor
        
        # Normalize to maintain constant speed
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * self.VELOCITY
            
        # Add some of the paddle's velocity to the ball
        self.velocity.x += self.paddle.velocity.x * 0.2
        
        # Move ball above paddle to prevent multiple collisions
        self.position.y = self.paddle.position.y - self.paddle.radius - self.radius - 1
        
        #self.bounce_sound.play()

    def check_brick_collisions(self, bricks, previous_position):
        for brick in bricks:
            if self.collides_with(brick):
                # Determine collision side and bounce accordingly
                brick.hit()
                globals.score += 10 * (globals.level + globals.score_multiplier)
                
                # Calculate collision direction
                dx = self.position.x - brick.position.x
                dy = self.position.y - brick.position.y
                
                # Simplified collision response - just bounce based on dominant axis
                if abs(dx) > abs(dy):
                    self.velocity.x = -self.velocity.x
                else:
                    self.velocity.y = -self.velocity.y
                
                # Only handle one brick collision per frame
                break