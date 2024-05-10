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
        nearby_patches = self.get_patches_in_radius()
        agent_dict = {(agent.x, agent.y): agent for agent in agents if agent.state == st.active}

        for x, y in nearby_patches:
            if (x, y) in agent_dict:
                agent = agent_dict[(x, y)]
                agent.state = st.jail
                agent.jail_term = random.randint(0, st.max_jail_term)  # 设置监禁期为0到max_jail_term的随机值
                map[x, y] = agent.state
                self.move_to(x, y, map)
                break
