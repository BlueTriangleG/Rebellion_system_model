

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation
from agent import Agent
from cop import Cop
from setting import Setting as st

class Simulation:

    def __init__(self):
        self.agents = []
        self.cops = []
        self.map = np.zeros((st.board_size, st.board_size), dtype=int)
        # create two subplots
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Submap 1: Show map
        self.cmap = ListedColormap(['white', 'green', 'black', 'red', 'grey'])
        self.mat = self.ax1.matshow(self.map, cmap=self.cmap, vmin=0, vmax=5)
        self.ax1.set_title('Simulation Map')
        
        # Subfigure 2: Line chart showing status counts
        # Text labels for showing real-time counts in the second subplot
        self.text_active_ax2 = self.ax2.text(0.02, 0.95, '', transform=self.ax2.transAxes, color='red')
        self.text_jailed_ax2 = self.ax2.text(0.02, 0.90, '', transform=self.ax2.transAxes, color='grey')
        self.text_quiet_ax2 = self.ax2.text(0.02, 0.85, '', transform=self.ax2.transAxes, color='green')

        self.statuses = ['Active', 'Jailed', 'Quiet']
        self.data = {status: [] for status in self.statuses}
        self.lines = {status: self.ax2.plot([], [], label=status)[0] for status in self.statuses}
        self.ax2.set_title('Agent Status Over Time')
        self.ax2.set_ylim(0, 1300)
        self.ax2.set_xlim(0, 200)  # Assuming an animation length of 200 frames
        self.ax2.legend()


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
            x, y = np.random.randint(0, st.board_size, 2)
            if self.map[x, y] == st.empty: 
                if obj_type == "agent":
                    agent = Agent(x, y)
                    self.agents.append(agent)
                    self.map[x, y] = st.quit  
                elif obj_type == "cop":
                    id = len(self.cops) + 1
                    cop = Cop(id, x, y)
                    self.cops.append(cop)
                    self.map[x, y] = st.cops 
                break

    def run(self):
        # initialise agent and cop
        # Calculate the number of initial agents and cop
        quit_agent_num = int(st.board_size ** 2 * st.initial_agent_density)
        cop_num = int(st.board_size ** 2 * st.initial_cop_density)
        # Initialising the map
        self.map = np.zeros((st.board_size, st.board_size), dtype=int)
        # Initialising agent and cop
        for _ in range(quit_agent_num):
            self.place_object("agent")
        for _ in range(cop_num):
            self.place_object("cop")
        self.ani = FuncAnimation(self.fig, self.update, frames=2000, interval=5, blit=False)
        plt.show()
        
    def update(self, frame):
        self.update_map()
        self.update_status_counts(frame)

        # Updated map display
        self.mat.set_data(self.map)

        # Update text labels for real-time counts in the second subplot
        self.text_active_ax2.set_text(f"Active: {self.data['Active'][-1]}")
        self.text_jailed_ax2.set_text(f"Jailed: {self.data['Jailed'][-1]}")
        self.text_quiet_ax2.set_text(f"Quiet: {self.data['Quiet'][-1]}")

        # Dynamically update the x-axis range for the line chart
        if frame > 200:
            self.ax2.set_xlim(frame - 200, frame)
        else:
            self.ax2.set_xlim(0, max(200, frame))

        # Update line chart
        for status in self.statuses:
            line = self.lines[status]
            data = self.data[status]
            line.set_data(range(len(data)), data)

        # Return all updated artists including new text objects
        return [self.mat, self.text_active_ax2, self.text_jailed_ax2, self.text_quiet_ax2] + list(self.lines.values())

    
    def update_status_counts(self, frame):
        # Update status counting logic
        active_count = sum(1 for agent in self.agents if agent.state == st.active)
        jailed_count = sum(1 for agent in self.agents if agent.state == st.jail)
        quiet_count = sum(1 for agent in self.agents if agent.state == st.quit)
        self.data['Active'].append(active_count)
        self.data['Jailed'].append(jailed_count)
        self.data['Quiet'].append(quiet_count)
