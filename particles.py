import pygame
from support import import_folder
from random import choice
        
class AnimationPlayer:
    '''
    This is the animation player class which includes attributes and methods
    responsible for playing particle effects and animations. It does this by
    using the particle effect class.
    '''
    def __init__(self):
        '''
        This is the constructor for the animation player class, containing the attributes
        related to the class. In this case, it includes an attribute called frames which is
        a dictionary containing the directories for all the particle effects, by making
        use of the import folder method from the support file.
        '''
        self.frames = {
            #magic
            'flame': import_folder('sprites2/5 - level graphics/graphics/particles/flame/frames'),
            'aura': import_folder('sprites2/5 - level graphics/graphics/particles/aura'),
            'heal': import_folder('sprites2/5 - level graphics/graphics/particles/heal/frames'),

            #attacks
            'claw': import_folder('sprites2/5 - level graphics/graphics/particles/claw'),
            'slash': import_folder('sprites2/5 - level graphics/graphics/particles/slash'),
            'sparkle': import_folder('sprites2/5 - level graphics/graphics/particles/sparkle'),
            'leaf_attack': import_folder('sprites2/5 - level graphics/graphics/particles/leaf_attack'),
            'thunder': import_folder('sprites2/5 - level graphics/graphics/particles/thunder'),

            #monster deaths
            'zombie': import_folder('sprites2/5 - level graphics/graphics/particles/smoke_orange'),
            'gorilla': import_folder('sprites2/5 - level graphics/graphics/particles/gorilla'),
            'tear': import_folder('sprites2/5 - level graphics/graphics/particles/nova'),
            'grassrot': import_folder('sprites2/5 - level graphics/graphics/particles/grassrot'),

            #leafs
            'leaf': (
                import_folder('sprites2/5 - level graphics/graphics/particles/leaf1'),
                import_folder('sprites2/5 - level graphics/graphics/particles/leaf2'),
                import_folder('sprites2/5 - level graphics/graphics/particles/leaf3'),
                import_folder('sprites2/5 - level graphics/graphics/particles/leaf4'),
                import_folder('sprites2/5 - level graphics/graphics/particles/leaf5'),
                import_folder('sprites2/5 - level graphics/graphics/particles/leaf6'),
                self.reflect_images(import_folder('sprites2/5 - level graphics/graphics/particles/leaf1')),
                self.reflect_images(import_folder('sprites2/5 - level graphics/graphics/particles/leaf2')),
                self.reflect_images(import_folder('sprites2/5 - level graphics/graphics/particles/leaf3')),
                self.reflect_images(import_folder('sprites2/5 - level graphics/graphics/particles/leaf4')),
                self.reflect_images(import_folder('sprites2/5 - level graphics/graphics/particles/leaf5')),
                self.reflect_images(import_folder('sprites2/5 - level graphics/graphics/particles/leaf6'))
            )
        }

    def reflect_images(self,frames):
        '''
        This method is used to reflect the set of frames being played so that
        it plays back to front. This can allow for animations to loop like the
        grass animations. This method is used in the dictionary found in the frames
        dictionary in the constructor.
        '''
        new_frames = []

        for frame in frames:
            flipped_frame = pygame.transform.flip(frame,True,False)
            new_frames.append(flipped_frame)
        return new_frames
    
    def create_grass_particles(self,pos,groups):
        '''
        This method is used to create the grass particles when a tile of grass
        is destroyed. This will be called in another file once this occurs. This
        method is responsible for playing the leaf animations.
        '''
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos,animation_frames,groups)

    def create_particles(self,animation_type,pos,groups):
        '''
        This method creates the rest of the particles as an animation, making
        use of the particle effect class. It gets these animation frames from
        the frames dictionary.
        '''
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos,animation_frames,groups)

class ParticleEffect(pygame.sprite.Sprite):
    '''
    This is the particle effect class, responsible for animating
    the frames together. This will be called throughout the animation
    player class. It also contains an update method which will be called
    from another file.
    '''
    def __init__(self,pos,animation_frames,groups):
        '''
        These are the attributes for the particle effects class. This
        mainly includes attributes used to animate frames together.
        '''
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self): #only plays animation once
        '''
        This is the animate method which uses the frame index and animation
        speed to play a sequence of frames in succession to create an animation.
        It plays the animation once then kills the last frame stopping it from continuing.
        '''
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        '''
        This is the update method for the particle effect class. This will
        be called in another file. It includes methods that need to be called
        such as the animate method.
        '''
        self.animate()