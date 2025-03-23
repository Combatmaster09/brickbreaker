from GameObject import gameobject
from pygame.math import Vector2
from utils import load_sprite
from AccelerationPaddle import acceleration_paddle
from VelocityPaddle import velocity_paddle

class Ball(gameobject):
    VELOCITY = 3

    def __init__(self, position, create_ball_callback, acceleration_paddle):
        self.create_bullet_callback = create_ball_callback
        self.acceleration_paddle = self.acceleration_paddle  # Store the acceleration paddle

        super().__init__(position, load_sprite("ball"), Vector2(0))

    def collides_with_paddle(self, paddle):
        if globals.paddle_type == "AccelerationPaddle":
            if self.collides_with(self.acceleration_paddle):  # Use self.acceleration_paddle
                self.velocity.x = -self.velocity.x
        elif globals.paddle_type == "VelocityPaddle":
            if self.collides_with(paddle):
                self.velocity.x = -self.velocity.x
