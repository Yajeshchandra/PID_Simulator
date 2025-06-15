"""
Main PID Simulation Application
Run this file to start the PID motor rod simulation.
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from plant import MotorRodPlant

# CONTROLLER SELECTION:
# The PID controller is now a template that students need to complete.
# Students should implement their PID algorithm in pid_controller.py

from pid_controller import PIDController          # Student template to complete

# NOTE: Both pid_controller.py and student_pid_template.py are now templates.
# Students should complete the PIDController class in pid_controller.py
from gui import PIDSimulationGUI

def main():
    """Main function to run the PID simulation."""
    
    print("Starting PID Motor Rod Simulation...")
    print("=" * 50)
    print("Educational PID Control System")
    print("Motor with Rod Stabilization")
    print("=" * 50)
    
    # Create plant model (second-order underdamped system)
    # These parameters create a challenging but tunable system
    plant = MotorRodPlant(
        K=1.0,          # System gain
        wn=2.0,         # Natural frequency (rad/s)
        zeta=0.1,       # Damping ratio (underdamped for oscillation)
        dt=0.01         # Time step (100 Hz simulation)
    )
      # Create PID controller with initial gains
    # Students can tune these through the GUI
    pid_controller = PIDController(
        Kp=1.0,         # Start with proportional only
        Ki=0.0,         # Add integral to eliminate steady-state error
        Kd=0.0,         # Add derivative to reduce overshoot
        dt=0.01         # Same as plant time step
    )
    
    print(f"Plant initialized: K={plant.K}, wn={plant.wn}, zeta={plant.zeta}")
    print(f"PID template loaded: Kp={pid_controller.Kp}, Ki={pid_controller.Ki}, Kd={pid_controller.Kd}")
    print()
    print("🎓 STUDENT TASK:")
    print("=" * 20)
    print("1. Open pid_controller.py")
    print("2. Complete the TODOs in the PIDController class")
    print("3. Implement the PID algorithm in compute() method")
    print("4. Add necessary state variables in __init__()")
    print("5. Run this simulation to test your implementation")
    print()
    print("📊 SIMULATION INSTRUCTIONS:")
    print("=" * 30)
    print("1. Click 'Start' to begin simulation")
    print("2. Adjust PID gains using sliders")
    print("3. Change setpoint to see tracking performance")
    print("4. Modify disturbance to test robustness")
    print("5. Watch the rod try to stay horizontal!")
    print()
    print("💡 PID TUNING TIPS:")
    print("=" * 20)
    print("- Start with Kp only, increase until oscillation")
    print("- Add Ki to eliminate steady-state error")
    print("- Add Kd to reduce overshoot and settling time")
    print("- Too much Ki causes instability")
    print("- Too much Kd amplifies noise")
    print()
    print("⚠️  NOTE: The simulation may not work properly until")
    print("   you complete the PID implementation!")
    print()
    
    try:
        # Create and run GUI
        gui = PIDSimulationGUI(plant, pid_controller)
        gui.run()
        
    except Exception as e:
        print(f"Error running simulation: {e}")
        print("Make sure you have the required packages installed:")
        print("pip install tkinter matplotlib numpy")
        return 1
    
    print("Simulation ended. Thank you!")
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
