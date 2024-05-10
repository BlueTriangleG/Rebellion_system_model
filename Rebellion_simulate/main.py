from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from simulation import Simulation
from setting import Setting

def run_simulation():
    sim = Simulation()
    sim.run()

class SimulationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Simulation Parameters")
        layout = QVBoxLayout()

        # Create input fields for each parameter while displaying the current value in the setup as the default
        self.cop_density = self.create_input_field("Initial Cop Density (0-1):", str(Setting.initial_cop_density), layout)
        self.agent_density = self.create_input_field("Initial Agent Density (0-1):", str(Setting.initial_agent_density), layout)
        self.vision = self.create_input_field("Vision (integer):", str(Setting.vision), layout)
        self.legitimacy = self.create_input_field("Government Legitimacy (0-1):", str(Setting.government_legitimacy), layout)
        self.jail_term = self.create_input_field("Max Jail Term (days):", str(Setting.max_jail_term), layout)

        # Create a button to run the simulation
        btn = QPushButton('Run Simulation', self)
        btn.clicked.connect(self.update_settings)
        layout.addWidget(btn)
        self.setLayout(layout)

    def create_input_field(self, label_text, default_value, layout):
        hbox = QHBoxLayout()
        label = QLabel(label_text)
        edit = QLineEdit()
        edit.setText(default_value)  # Set the default value of the input box
        hbox.addWidget(label)
        hbox.addWidget(edit)
        layout.addLayout(hbox)
        return edit

    def update_settings(self):
        # Get data from the input box and update the properties of the Setting class
        Setting.initial_cop_density = float(self.cop_density.text())
        Setting.initial_agent_density = float(self.agent_density.text())
        Setting.vision = int(self.vision.text())
        Setting.government_legitimacy = float(self.legitimacy.text())
        Setting.max_jail_term = int(self.jail_term.text())
        run_simulation()

def main():
    app = QApplication([])
    ex = SimulationWindow()
    ex.show()
    app.exec_()

if __name__ == "__main__":
    main()
