import pygame
import pygame.mixer

class brickbreaker:
    #This class manages overall game state and acts as the main loop for the game
    def __init__(self):
     self._init_pygame()
     self.screen = pygame.display.set_mode((1440, 990), pygame.FULLSCREEN)
     self.clock = pygame.time.Clock()
     
    def main_loop(self):
        """This function is the main game loop that handles user input, 
        game logic processing, and rendering"""
        while globals.game:
            self._handle_input()
            self._process_game_logic()
            self._draw()
            if self.restart_game:
                self.reset_game()
                self.restart_game = False
                
                
    def _init_pygame(self):
        """This function initializes the pygame library and sets the game window caption"""
        pygame.init()
        pygame.display.set_caption("Brick Breaker")