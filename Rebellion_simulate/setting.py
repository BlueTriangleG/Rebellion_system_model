# This is the class using to set the parameters of the simulation. Change the parameters here to change the simulation environment.

# Setting parameters of the simulation.
# board parameters

class Setting:
    # agent parameters
    initial_cop_density = 0.04
    initial_agent_density = 0.7
    vision = 7
    threshold = 0.1
    k = 2.3
    # turtle states
    quit = 1
    cops = 2
    active = 3
    jail = 4
    empty = 0
    # environment parameters
    government_legitimacy = 0.82
    max_jail_term = 30
    board_size = 40
    movement = True