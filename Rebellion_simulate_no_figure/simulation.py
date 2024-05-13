# This file contains the simulation class, which is the main class of the simulation.
import random
from agent import Agent
from cop import Cop
from setting import Setting as st
import csv

class Simulation:

    def __init__(self):
        self.agents = []
        self.cops = []
        self.board_size = st.board_size
        self.map = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.statuses = ['Active', 'Jailed', 'Quiet']
        self.data = {status: [] for status in self.statuses}
        self.csv_file = open('frame_data.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Frame', 'Active', 'Jailed', 'Quiet'])


    def update_map(self):
        # update agent and cop in one time step
        # update ruleM
        if st.movement == True:
            for agent in self.agents:
                agent.move(self.map)
        for cop in self.cops:
                cop.move(self.map)
        # update rule A
        for agent in self.agents:
            agent.determine_behavior(self.map)
        # update rule C
        for cop in self.cops:
            cop.enforce(self.map, self.agents)
        
        # update jail term
        for agent in self.agents:
            if agent.state == st.jail:
                agent.reduce_jail_term(self.map)
    
    def place_object(self, obj_type):
        # randomly place agent or cop on the map
        while True:
            x = random.randint(0, self.board_size - 1)
            y = random.randint(0, self.board_size - 1)
            if self.map[x][y] == st.empty: 
                if obj_type == "agent":
                    agent = Agent(x, y)
                    self.agents.append(agent)
                    self.map[x][y] = st.quit  
                elif obj_type == "cop":
                    cop = Cop(id, x, y)
                    self.cops.append(cop)
                    self.map[x][y] = st.cops 
                break
    
    def update_status_counts(self, frame):
        # update the number of agents in each status in current time step
        active_count = len([agent for agent in self.agents if agent.state == st.active])
        jailed_count = len([agent for agent in self.agents if agent.state == st.jail])
        quiet_count = len([agent for agent in self.agents if agent.state == st.quit])
        self.data['Active'].append(active_count)
        self.data['Jailed'].append(jailed_count)
        self.data['Quiet'].append(quiet_count)
        self.csv_writer.writerow([frame, active_count, jailed_count, quiet_count])

        print(f"Frame {frame}: Active agents: {active_count}, Jailed agents: {jailed_count}, Quiet agents: {quiet_count}")

    def close_csv(self):
        self.csv_file.close()


    def run(self, round):
        # initialise agent and cop
        # Calculate the number of initial agents and cop
        quit_agent_num = int(st.board_size ** 2 * st.initial_agent_density)
        cop_num = int(st.board_size ** 2 * st.initial_cop_density)
        # Initialising agent and cop
        for _ in range(quit_agent_num):
            self.place_object("agent")
        for _ in range(cop_num):
            self.place_object("cop")
        frame = 0
        for _ in range(round):
            self.update_map()
            self.update_status_counts(frame)
            frame += 1
        self.close_csv()
