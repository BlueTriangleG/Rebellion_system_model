# It is the class represent all the moving objectss.
from setting import Setting as st
import numpy as np
import random
class Turtle:
    id = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = Turtle.id
        Turtle.id += 1
        self.previeous_state = st.empty
    # Get the patches in the radius，filter is the type of patch you want to get.
    def get_patches_in_radius(self,map, filter = [st.empty]):
        radius = st.vision
        board_size = st.board_size
        patches = []
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx*dx + dy*dy <= radius*radius:  
                    x = (self.x + dx) % board_size
                    y = (self.y + dy) % board_size
                    # If the patch is in the radius and the type of patch is in the filter, add it to the patches.
                    if map[x, y] in filter:
                        patches.append((x, y))
        return patches
    
    def move(self, map):
        # Get the available patches in the radius
        available_patches = self.get_patches_in_radius(map, [st.empty])

        # If there's an available point, randomly select one to move to
        if available_patches:
            new_x, new_y = available_patches[np.random.randint(len(available_patches))]
            self.move_to(new_x, new_y, map)
                
    def move_to(self, x, y, map):
        map[self.x, self.y] = self.previeous_state
        self.previeous_state = map[x, y]
        self.x = x
        self.y = y
        map[x, y] = self.state