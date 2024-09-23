'''
These are the variables for common numbers, values, letters, or
directories that could be used in other files within game setup.
This is done to aid with the readability of my program
'''
#game setup
WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64
HITBOX_OFFSET = {
    'player': -26,
    'object': -40,
    'grass': -10,
    'invisible': 0}

'''
These are the variables for common numbers, values, letters, or
directories that could be used in other files within the ui.
This is done to aid with the readability of my program
'''
#ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = '../NEA/sprites2/5 - level graphics/graphics/font/joystix.ttf'
UI_FONT_SIZE = 18
MINIMAP = 'sprites2/5 - level graphics/graphics/tilemap/ground3.png'
MINIMAP_WIDTH = 199
MINIMAP_HEIGHT = 175

'''
These are the variables for common numbers, values, letters, or
directories that could be used in other files within the ui for
general colours. This is done to aid with the readability of my
program
'''
#general colours
LAVA_COLOR = '#c32329'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

'''
These are the variables for common numbers, values, letters, or
directories that could be used in other files within the ui for
the health and energy colours. This is done to aid with the readability
of my program
'''
#ui colours
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'GOLD'

# WORLD_MAP = [
#     ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
#     ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
#     ['x', ' ', 'p', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
#     ['x', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', 'x', 'x', 'x', 'x', 'x', ' ', ' ', ' ', ' ', ' ', 'x'],
#     ['x', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', 'x'],
#     ['x', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', 'x'],
#     ['x', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', 'x'],
#     ['x', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', 'x'],
#     ['x', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', 'x'],
#     ['x', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', 'x'],
#     ['x', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', 'x'],
#     ['x', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', 'x', 'x', ' ', ' ', ' ', 'x'],
#     ['x', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
#     ['x', ' ', ' ', ' ', ' ', ' ', 'x', 'x', 'x', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
#     ['x', ' ', ' ', ' ', ' ', ' ', ' ', 'x', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
#     ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
#     ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
#     ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
#     ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
#     ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
# ]
# 'x'=collsion, ' '=no collision, 'p'=player

'''
This is the dictionaries of dictionaries containing weapon data
used within the player class.
'''
# weapons
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15,'graphics':'sprites2/5 - level graphics/graphics/weapons/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 30,'graphics':'sprites2/5 - level graphics/graphics/weapons/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20,'graphics':'sprites2/5 - level graphics/graphics/weapons/axe/full.png'},
    'rapier': {'cooldown': 50, 'damage': 8,'graphics':'sprites2/5 - level graphics/graphics/weapons/rapier/full.png'},
    'sai': {'cooldown': 80, 'damage': 10,'graphics':'sprites2/5 - level graphics/graphics/weapons/sai/full.png'}}

'''
This is the dictionaries of dictionaries containing magic data
used within the player class.
'''
#magic
magic_data = {
    'flame' : {'strength': 5,'cost': 20,'graphics':'sprites2/5 - level graphics/graphics/particles/flame/fire.png'},
    'heal' : {'strength': 20,'cost': 10,'graphics':'sprites2/5 - level graphics/graphics/particles/heal/heal.png'}}

'''
This is the dictionaries of dictionaries containing monster data
used within the enemy class.
'''
#enemy
monster_data = {
    'zombie': {'health':100,'exp':100,'energy':5,'damage':20,'attack_type':'slash','attack_sound':'sprites2/5 - level graphics/audio/attack/slash.wav','speed':1,'resistance':3,'attack_radius':80,'notice_radius':225},
    'gorilla': {'health':300,'exp':250,'energy':20,'damage':40,'attack_type':'claw','attack_sound':'sprites2/5 - level graphics/audio/attack/claw.wav','speed':2,'resistance':3,'attack_radius':120,'notice_radius':500},
    'tear': {'health':100,'exp':110,'energy':10,'damage':8,'attack_type':'thunder','attack_sound':'sprites2/5 - level graphics/audio/attack/fireball.wav','speed':1,'resistance':3,'attack_radius':60,'notice_radius':219},
    'grassrot': {'health':70,'exp':120,'energy':5,'damage':6,'attack_type':'leaf_attack','attack_sound':'sprites2/5 - level graphics/audio/attack/slash.wav','speed':1,'resistance':3,'attack_radius':50,'notice_radius':188},
}
