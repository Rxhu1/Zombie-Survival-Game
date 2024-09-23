import pygame


class Weapon(pygame.sprite.Sprite):
    '''
    This is the weapon class, which gets the direction of the player, and uses it to
    get the right asset of the the weapon in use. In addition, it determines the rect
    of the weapon asset depending on the direction of the player. It will place this
    to the side of the player.
    '''
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        direction = player.status.split('_')[0]

        #graphic
        full_path = f'../NEA/sprites2/5 - level graphics/graphics/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        #placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-13,0))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-13,0))