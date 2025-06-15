"""
Motor with Rod Plant Model
Second-order system representing a motor with an attached rod that needs to be kept horizontal.
"""

import numpy as np

class MotorRodPlant:
    """
    Second-order plant model for motor with rod system.
    The system represents a motor trying to keep a rod horizontal against gravity.
    
    Transfer function: G(s) = K / (s^2 + 2*zeta*wn*s + wn^2)
    Where:
    - K: System gain
    - wn: Natural frequency (rad/s)
    - zeta: Damping ratio
    """
    
    def __init__(self, K=1.0, wn=2.0, zeta=0.1, dt=0.01):
        """
        Initialize the plant model.
        
        Args:
            K (float): System gain
            wn (float): Natural frequency (rad/s)
            zeta (float): Damping ratio (underdamped for oscillatory behavior)
            dt (float): Time step for simulation
        """
        self.K = K
        self.wn = wn
        self.zeta = zeta
        self.dt = dt
        
        # State variables [position, velocity]
        self.state = np.array([0.0, 0.0])  # [angle, angular_velocity]
        
        # Disturbance (gravity effect)
        self.gravity_disturbance = 0.5  # Constant disturbance representing gravity
        
        # System matrices for state-space representation
        # x_dot = A*x + B*u + D*disturbance
        self.A = np.array([[0, 1],
                          [-self.wn**2, -2*self.zeta*self.wn]])
        
        self.B = np.array([[0],
                          [self.K * self.wn**2]])
        
        self.D = np.array([[0],
                          [1]])  # Disturbance input matrix
        
    def update(self, control_input):
        """
        Update the plant state given a control input.
        
        Args:
            control_input (float): Control signal from PID controller
            
        Returns:
            float: Current position (angle) of the rod
        """
        # Add some noise to make it more realistic
        noise = np.random.normal(0, 0.01)
        
        # State derivative
        state_dot = (self.A @ self.state.reshape(-1, 1) + 
                    self.B * control_input + 
                    self.D * (self.gravity_disturbance + noise)).flatten()
        
        # Euler integration
        self.state += state_dot * self.dt
        
        # Return position (angle)
        return self.state[0]
    
    def get_position(self):
        """Get current rod position (angle in radians)."""
        return self.state[0]
    
    def get_velocity(self):
        """Get current rod angular velocity."""
        return self.state[1]
    
    def reset(self):
        """Reset the plant to initial conditions."""
        self.state = np.array([0.0, 0.0])
    
    def set_disturbance(self, disturbance):
        """Set the gravity disturbance level."""
        self.gravity_disturbance = disturbance
    
    def get_info(self):
        """Get plant parameters for display."""
        return {
            'K': self.K,
            'wn': self.wn,
            'zeta': self.zeta,
            'dt': self.dt,
            'position': self.state[0],
            'velocity': self.state[1]
        }
