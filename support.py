from csv import reader #lets me read the csv file
from os import walk #lets you walk through the file system
import pygame

def import_csv_layout(path):
    '''
    This function is used to import the csv layout, by using a comma
    to separate each entry to the file to create the map layout.
    '''
    terrain_map = []
    with open(path) as level_map: #opens file
        layout = reader(level_map,delimiter = ',') #this will use a comma to seperate each entry in the file.
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map
    
def import_folder(path):
    '''
    This function is very important is used throughout the entire implementation of the program.
    This is responsible for walking through a file path and removing the forward slash to get the
    image that needs to be loaded. These are added to a list which is returned.
    '''
    surface_list = []
    
    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list