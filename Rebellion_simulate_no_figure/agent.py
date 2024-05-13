# This is agent model. It contains the agent class that will be used to create agents in the model.
# Using int to represent the state of the agent.
from turtle import Turtle
from setting import Setting as st
import random
import math

class Agent(Turtle):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.state = st.quit  # Initial state
        self.risk_aversion = random.uniform(0, 1)  #  risk aversion from [0, 1]
        self.perceived_hardship = random.uniform(0, 1)  # Perceived Difficulty from [0, 1]
        self.jail_term = 0  # prison term
        self.grievance = self.perceived_hardship * (1 - st.government_legitimacy)
        self.threshold = st.threshold  # threshold of rebellion
       
    def count_cops(self, nearby_patches, map):
        # count the number of cops in the nearby patches
        count = 0
        for patch in nearby_patches:
            x, y = patch
            if map[x][y] == st.cops:
                count += 1
        return count 
    
    def count_active_agents(self, nearby_patches, map):
        # count the number of active agents in the nearby patches
        count = 0
        for patch in nearby_patches:
            x, y = patch
            if map[x][y] == st.active:
                count += 1
        return count
    
    def estimated_arrest_probability(self, map):
        # Record the patches you can see
        nearby_patches = self.get_patches_in_radius(map, [st.cops, st.active, st.empty])
        c = self.count_cops(nearby_patches, map)
        a = 1 + self.count_active_agents(nearby_patches, map)
        k = st.k
        result = 1 - math.exp(-k * math.floor(c / a))
        return result
    
    def determine_behavior(self, map):
        # Calculating the probability of arrest
        if self.state == st.jail:
            return
        arrest_prob = self.estimated_arrest_probability(map)
        # Calculating activation conditions
        if self.grievance - self.risk_aversion * arrest_prob > self.threshold:
            self.state = st.active 
        else:
            self.state = st.quit 
        map[self.x][self.y] = self.state
        
    def move(self, map):
        if self.state == st.jail:
            return  
        available_patches = self.get_patches_in_radius(map, [st.empty])
        # If there's an available point, randomly select one to move to
        if available_patches:
            new_x, new_y = random.choice(available_patches)
            self.move_to(new_x, new_y, map)


    def reduce_jail_term(self, map):
        # Reduce the jail term by 1 each time step
        self.jail_term -= 1
        if self.jail_term <= 0:
            self.state = st.quit
        map[self.x][self.y] = self.state
