# This is class of cop.
from turtle import Turtle
from setting import Setting as st
import random

class Cop(Turtle):
    def __init__(self, id,x,y):
        super().__init__(x,y)
        self.id = id
        self.state = st.cops
    
    def enforce(self, map, agents):
        # cops try to arrest the active agents in the nearby patches
        nearby_patches = self.get_patches_in_radius(map, [st.active])
        agent_dict = {(agent.x, agent.y): agent for agent in agents if agent.state == st.active}
        if nearby_patches:
            x, y = nearby_patches[random.randint(0, len(nearby_patches) - 1)]
            agent = agent_dict[(x, y)]
            agent.state = st.jail
            agent.jail_term = random.randint(0, st.max_jail_term) 
            map[x][y] = agent.state
            self.move_to(x, y, map)
