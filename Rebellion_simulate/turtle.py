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
    def get_patches_in_radius(self):
        patches = []
        radius = st.vision
        board_size = st.board_size 
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                # Using modulo arithmetic to deal with cyclic world boundaries
                x = (self.x + dx) % board_size
                y = (self.y + dy) % board_size
                if np.sqrt(dx**2 + dy**2) <= radius:  # Using Euclidean distances to determine points within a radius
                    patches.append((x, y))
        return patches
    
    def move(self, map):
            # Get all coordinate points within the radius of the field of view
            nearby_patches = self.get_patches_in_radius()
            available_patches = []

            # Filter out the points on the map with a value of 0 (i.e., idle points) from these coordinate points
            for patch in nearby_patches:
                px, py = patch
                if map[px, py] == 0:  # Check if the corresponding position on the map is free
                    available_patches.append((px, py))

            # If there's a point available, randomly select one to be moved
            if available_patches:
                new_x, new_y = random.choice(available_patches)  # Randomly select an available location
                self.move_to(new_x, new_y, map)
                
    def move_to(self, x, y, map):
        map[self.x, self.y] = self.previeous_state
        self.previeous_state = map[x, y]
        self.x = x
        self.y = y
        map[x, y] = self.state