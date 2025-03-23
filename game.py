import pygame
import pygame.mixer
import globals

class brickbreaker:
    #This class manages overall game state and acts as the main loop for the game
    def __init__(self):
     self._init_pygame()
     self.screen = pygame.display.set_mode((800, 600))
     self.clock = pygame.time.Clock()
     self.restart_game = False 
     
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
        
    def _handle_input(self):
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            globals.game = False
            pygame.quit()
            
    
    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)
    
    def _draw(self):
        pygame.draw.rect(self.screen, globals.colour, pygame.Rect(30, 30, 60, 60))
        pygame.display.flip()
    
    def reset_game(self):
        pass