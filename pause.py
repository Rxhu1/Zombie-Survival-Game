import pygame
from settings import WIDTH, HEIGHT

class Pause:
    '''
    This is the pause class, containing the related implementation that can be called
    in the level class to run the pause related methods once the user has chosen to
    enter the pause gamestate. It also has implementation used during the death gamestate.
    As the implementation within both of these gamestates are relatively short, both of these
    are used within the same class.
    '''
    def __init__(self):
        '''
        These are the following attributes used within the pause class. This includes the display
        surface, which is used to blur and drawn on the screen, and all of the directories of the
        different assets that I wanted to try and use within this function. Ultimately, the attributes
        for the death gamestate are also found here for the simplicity of the code rather than creating
        another class for death.
        '''
        #general setup
        self.display_surface = pygame.display.get_surface()
        self.pause = pygame.image.load('sprites2/5 - level graphics/graphics/gamestates/pause.png').convert_alpha()
        self.pause2 = pygame.image.load('sprites2/5 - level graphics/graphics/gamestates/pause2.png').convert_alpha()
        self.death = pygame.image.load('sprites2/5 - level graphics/graphics/gamestates/death.png').convert_alpha()
        self.death2 = pygame.image.load('sprites2/5 - level graphics/graphics/gamestates/death2.png').convert_alpha()
        self.restart = pygame.image.load('sprites2/5 - level graphics/graphics/gamestates/restart2.png').convert_alpha()

    def blur_surf(self):
        '''
        The blur surf method acts to blur the most current display surface since the method
        has been called when the user enters the pause gamestate. This will blur the screen
        by changing the scale of the image to be smaller and then will re size the image back
        to normal which will make the quality worse due to lossy compression.
        '''
        #blurs screen by scaling the screen so its smaller and then back to normal.
        scale = 1 / 5
        surf_size = self.display_surface.get_size()
        scale_size = (surf_size[0]*scale),(surf_size[1]*scale)
        surf = pygame.transform.smoothscale(self.display_surface, scale_size)
        surf = pygame.transform.smoothscale(surf,surf_size)
        return surf
    
    def draw_pause(self):
        '''
        The draw_pause method simply draws the pause image on screen at certain coordinates
        '''
        self.display_surface.blit(self.pause2,((WIDTH/2) - 360,(HEIGHT/2) - 360))
    
    def draw_death(self):
        '''
        The draw_death method simply draws the 'you died' image on screen at certain coordinates
        as well as the 'press r to restart' image.
        '''
        self.display_surface.blit(self.death2,((WIDTH/2) - 640,(HEIGHT/2) - 90))
        self.display_surface.blit(self.restart,((WIDTH/2) + 380,(HEIGHT/2)- 65))