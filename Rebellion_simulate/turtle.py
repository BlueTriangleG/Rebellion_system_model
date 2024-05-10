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
        radius = st.vision
        board_size = st.board_size
        patches = []
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx*dx + dy*dy <= radius*radius:  
                    x = (self.x + dx) % board_size
                    y = (self.y + dy) % board_size
                    patches.append((x, y))
        return patches
    
    def move(self, map):
        radius = st.vision
        board_size = st.board_size
        available_patches = []
        
        # Combine loops to find available spots
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx*dx + dy*dy <= radius*radius:
                    px = (self.x + dx) % board_size
                    py = (self.y + dy) % board_size
                    if map[px, py] == 0:
                        available_patches.append((px, py))

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