from simulation import Simulation
from setting import Setting
import sys

def main():
    try:
        rounds = int(input("Enter the number of rounds you want to simulate: "))
        if rounds < 1:
            raise ValueError("Number of rounds must be at least 1.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        sys.exit(1)
    sim = Simulation()
    sim.run(rounds)

if __name__ == "__main__":
    main()
