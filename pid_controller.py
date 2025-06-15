"""
PID Implementation Template
Complete the missing parts to make the PID controller work!

INSTRUCTIONS:
1. Fill in the TODOs in the StudentPIDController class
2. Run the simulation and test your controller!
"""

import numpy as np

class PIDController:
    """
    YOUR MISSION: Make this PID controller work!
    
    Goal: Keep the rod horizontal (angle = 0) using PID control.
    Formula: output = Kp*error + Ki*integral + Kd*derivative
    """
    
    def __init__(self, Kp=1.0, Ki=0.0, Kd=0.0, dt=0.01):
        """Initialize your controller."""
        self.Kp = Kp
        self.Ki = Ki  
        self.Kd = Kd
        self.dt = dt
        
        # TODO: Add variables you need to remember between calls
        # Hint: What do you need for integral and derivative terms?
        
        self.error_history = []
        self.output_history = []
        
    def compute(self, setpoint, measured_value):
        """
        Calculate control output to move the rod.
        
        Args:
            setpoint: Where you want the rod (usually 0 = horizontal)
            measured_value: Where the rod actually is (in radians)
            
        Returns:
            Control signal to send to the motor
        """
        
        # TODO: Implement PID algorithm
        # Step 1: Calculate error
        # Step 2: Calculate proportional term
        # Step 3: Calculate integral term
        # Step 4: Calculate derivative term
        # Step 5: Return P + I + D
        # Step 6: Store error and output for tracking
        
        return 0.0  # REPLACE THIS with your PID calculation!
    
    def reset(self):
        """Reset controller when user clicks Reset button."""
        # TODO: Reset any variables that accumulate over time
        # eg - self.kp = 1.0 or self.error_history = [] etc.
        pass
    
    def set_gains(self, Kp, Ki, Kd):
        """Update gains when user moves sliders."""
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
    
    # Required methods for GUI integration (you can leave these as-is)
    def get_pid_terms(self):
        """Return P, I, D values for display."""
        # TODO: Calculate and return the current PID terms
        # e.g. {'proportional': P, 'integral': I, 'derivative': D, 'total_output': P + I + D}
        return {'proportional': 0, 'integral': 0, 'derivative': 0, 'total_output': 0}
    
    def get_gains(self):
        """Return current gains."""
        return {'Kp': self.Kp, 'Ki': self.Ki, 'Kd': self.Kd}
    
#Bonus :
# If you want to add bonus features, you can implement them here.
# For example, windup filters, anti-windup mechanisms, or advanced PID algorithms.
