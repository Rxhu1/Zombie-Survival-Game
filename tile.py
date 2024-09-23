import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    '''
    This is the tile class. The main use of this class is just to instantiate individual
    tiles. These have their own rects and offsets to their positions.
    '''
    def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        y_offset = HITBOX_OFFSET[sprite_type]
        self.image = surface
        if sprite_type == 'object':
            #offset required
            self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,y_offset)