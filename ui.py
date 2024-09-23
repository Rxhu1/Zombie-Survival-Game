import pygame
from settings import *
#from tile import Tile
#from level import *

class UI:
    def __init__(self):
        '''
        These are the attributes that will be used in the ui class. This mainly includes
        font styles, rectangle sizes, as well as dictionaries for both weapons and magic.
        '''
        #general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

        #minimap setup
        self.minimap_rect = pygame.Rect(1070,10,MINIMAP_WIDTH,MINIMAP_HEIGHT)

        #bar setup
        self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT)

        #convert weapon dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphics']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon) #this put all of the weapons in a list

        #convert magic dictionary
        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphics']
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic) #this put all of the magic abilities in a list

    def show_bar(self,current,max_amount,bg_rect,color): #draws health and energy bars
        '''
        This is the show bar method which is used to draw the bars for the both the health
        bar and the energy bar.
        '''
        #draw bg
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)

        #converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        #drawing the bar
        pygame.draw.rect(self.display_surface,color,current_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)

    def draw_minimap(self, minimap):
        '''
        In this draw minimap method, I ended up using the draw class in the pygame library
        to display the minimap rectangle that will go behind the actual minimap. This is 
        designed to be slightly larger than the minimap so I can can easily be seen and contrasts
        to the game background.
        '''
        #draw bg
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,self.minimap_rect)

        #self.screen.blit(minimap, (1075,15))
        #Tile((1075,15),[self.visible_sprites],'minimap', minimap)

    def show_exp(self,exp): #displys exp on screen.
        '''
        Similarly, this show exp method is used to draw the rectangle for the score text to be in.
        The width of this is dependent on the size of the number, and thus changes and the exp gets
        larger.
        '''
        text_surf = self.font.render(str(int(exp)),False,TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20 #finds the vector bottom right to place the exp
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x,y))

        pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(20,20)) #score bg
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(20,20),3) #frame

    def inventory_box(self,left,top, has_switched):
        '''
        This method is used to create the rectangles for the inventory in the bottom left
        of the screen. This includes two overlapping squares.
        '''
        bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR_ACTIVE,bg_rect,3)
        else:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
        return bg_rect

    def weapon_overlay(self,weapon_index,has_switched):
        '''
        This method is used to overlay the weapon that is currently in use on top
        of the box made for the weapon inventory. This changes as the user changes
        the weapon in use.
        '''
        bg_rect = self.inventory_box(10,590,has_switched)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(weapon_surf,weapon_rect)

    def magic_overlay(self,magic_index,has_switched):
        '''
        This method is used to overlay the magic spell that is currently in use on top
        of the box made for the magic inventory. This changes as the user changes
        the magic spell in use.
        '''
        bg_rect = self.inventory_box(70,635,has_switched)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(magic_surf,magic_rect)

    def display(self,player):
        '''
        This is an important method as it calls all of the other methods created in this class
        to draw the UI onto the screen. This will be constantly called in the run method in the
        level class.
        '''
        self.show_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR)
        self.show_bar(player.energy,player.stats['energy'],self.energy_bar_rect,ENERGY_COLOR)

        self.show_exp(player.exp)
        self.draw_minimap(MINIMAP)

        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon) #weapon
        self.magic_overlay(player.magic_index, not player.can_switch_magic) #magic