import pygame
from settings import *
from random import randint

class MagicPlayer:
    '''
    This class is designed to play the animations of the different magic spells. In addition, it
    has the logic behind both spells which either increase the players heal or damages the enemy.
    It also determines where it should spawn the animations with a given offset aswell as playing 
    the sound effect corresponding to the appropriate spell.
    '''
    def __init__(self,animation_player):
        '''
        These are the attributes for the magic player class. This included initialising the animation
        player to an attribute so it can be called and used in this class. This also contains attributes
        which hold the file location of the different audios played for each spell, held in a dictionary.
        '''
        self.animation_player = animation_player
        self.sounds = {
            'heal': pygame.mixer.Sound('sprites2/5 - level graphics/audio/heal.wav'),
            'flame': pygame.mixer.Sound('sprites2/5 - level graphics/audio/Fire.wav')
            }

    def heal(self,player,strength,cost,groups):
        '''
        The heal method is called elsewhere and contains the logic of the heal spell, including
        playing the sound effect, minusing the energy, increasing the health of the player, and 
        playing the particle effects on top of the player with some slight offset.
        '''
        if player.energy >= cost:
            self.sounds['heal'].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
                self.animation_player.create_particles('aura',player.rect.center,groups)
                self.animation_player.create_particles('heal',player.rect.center + pygame.math.Vector2(0,-60),groups)
        if player.health >= player.stats['health'] and player.energy >= cost:
                self.animation_player.create_particles('aura',player.rect.center,groups)
                self.animation_player.create_particles('heal',player.rect.center + pygame.math.Vector2(0,-60),groups)

    def flame(self,player,cost,groups):
        '''
        This flame method is responsible for providing the logic of the flame spell.
        This method reduces the energy level by the cost, plays the sound effect and
        draws the assets on screen. Drawing the assets however included looking at the
        position of the player using their status and thus responding on where the fire
        should be drawn. This also includes the manipulation of the tile size to spawn
        identicle sprites for the flame 5 tiles away from the player, each with their
        own damage via collision and their own slight offset, letting them be placed
        randomly within a tile.
        '''
        if player.energy >= cost:
            player.energy -= cost
            self.sounds['flame'].play()
            self.sounds['flame'].set_volume(0.1)

            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1,0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1,0)
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0,-1)
            else:
                direction = pygame.math.Vector2(0,1)

            for i in range(1,6):
                if direction.x: #horizontal
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame',(x,y),groups)
                else: #vertical
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame',(x,y),groups)