"""
Real-time GUI for PID Motor Rod Simulation
Displays the motor and rod position in real-time with tuning controls.
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np
import math

class PIDSimulationGUI:
    """
    GUI for PID simulation with real-time motor and rod visualization.
    """
    
    def __init__(self, plant, pid_controller):
        """
        Initialize the GUI.
        
        Args:
            plant: Motor rod plant object
            pid_controller: PID controller object
        """
        self.plant = plant
        self.pid = pid_controller
        
        # Simulation parameters
        self.setpoint = 0.0  # Desired horizontal position
        self.is_running = False
        self.time = 0.0
        
        # Data for plotting
        self.time_history = []
        self.position_history = []
        self.setpoint_history = []
        self.control_history = []
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("PID Motor Rod Simulation")
        self.root.geometry("1200x800")
        
        self.setup_gui()
        self.setup_animation()
        
    def setup_gui(self):
        """Setup the GUI layout."""
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for visualization
        viz_frame = ttk.LabelFrame(main_frame, text="Motor & Rod Visualization", padding=10)
        viz_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Motor visualization
        self.setup_motor_visualization(viz_frame)
        
        # Response plot
        self.setup_response_plot(viz_frame)
        
        # Right panel for controls
        control_frame = ttk.LabelFrame(main_frame, text="PID Control Panel", padding=10)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.setup_controls(control_frame)
        
    def setup_motor_visualization(self, parent):
        """Setup the motor and rod visualization."""
        
        # Create matplotlib figure for motor visualization
        self.motor_fig, self.motor_ax = plt.subplots(figsize=(6, 4))
        self.motor_fig.patch.set_facecolor('white')
        
        # Setup motor visualization
        self.motor_ax.set_xlim(-3, 3)
        self.motor_ax.set_ylim(-2, 2)
        self.motor_ax.set_aspect('equal')
        self.motor_ax.grid(True, alpha=0.3)
        self.motor_ax.set_title('Motor with Rod (Real-time)')
        
        # Motor base (circle)
        motor_circle = plt.Circle((0, 0), 0.3, color='gray', zorder=1)
        self.motor_ax.add_patch(motor_circle)
        
        # Rod (line that will rotate)
        self.rod_line, = self.motor_ax.plot([0, 2], [0, 0], 'r-', linewidth=4, zorder=2)
        
        # Rod end point
        self.rod_end, = self.motor_ax.plot([2], [0], 'ro', markersize=8, zorder=3)
        
        # Setpoint indicator (horizontal line)
        self.setpoint_line, = self.motor_ax.plot([-3, 3], [0, 0], 'g--', alpha=0.7, linewidth=2)
        
        # Add canvas to tkinter
        self.motor_canvas = FigureCanvasTkAgg(self.motor_fig, parent)
        self.motor_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def setup_response_plot(self, parent):
        """Setup the response time plot."""
        
        # Create matplotlib figure for response plot
        self.response_fig, self.response_ax = plt.subplots(figsize=(6, 3))
        self.response_fig.patch.set_facecolor('white')
        
        self.response_ax.set_xlabel('Time (s)')
        self.response_ax.set_ylabel('Angle (rad)')
        self.response_ax.grid(True, alpha=0.3)
        self.response_ax.set_title('System Response')
        
        # Initialize empty plots
        self.position_line, = self.response_ax.plot([], [], 'b-', label='Position')
        self.setpoint_line_plot, = self.response_ax.plot([], [], 'g--', label='Setpoint')
        self.control_line, = self.response_ax.plot([], [], 'r-', alpha=0.7, label='Control Output')
        
        self.response_ax.legend()
        
        # Add canvas to tkinter
        self.response_canvas = FigureCanvasTkAgg(self.response_fig, parent)
        self.response_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def setup_controls(self, parent):
        """Setup control panel."""
        
        # PID Gains
        gains_frame = ttk.LabelFrame(parent, text="PID Gains", padding=10)
        gains_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Kp
        ttk.Label(gains_frame, text="Kp:").grid(row=0, column=0, sticky=tk.W)
        self.kp_var = tk.DoubleVar(value=self.pid.Kp)
        self.kp_scale = ttk.Scale(gains_frame, from_=0.0, to=10.0, variable=self.kp_var, 
                                 orient=tk.HORIZONTAL, length=200)
        self.kp_scale.grid(row=0, column=1, padx=5)
        self.kp_label = ttk.Label(gains_frame, text=f"{self.kp_var.get():.2f}")
        self.kp_label.grid(row=0, column=2)
        
        # Ki
        ttk.Label(gains_frame, text="Ki:").grid(row=1, column=0, sticky=tk.W)
        self.ki_var = tk.DoubleVar(value=self.pid.Ki)
        self.ki_scale = ttk.Scale(gains_frame, from_=0.0, to=5.0, variable=self.ki_var,
                                 orient=tk.HORIZONTAL, length=200)
        self.ki_scale.grid(row=1, column=1, padx=5)
        self.ki_label = ttk.Label(gains_frame, text=f"{self.ki_var.get():.2f}")
        self.ki_label.grid(row=1, column=2)
        
        # Kd
        ttk.Label(gains_frame, text="Kd:").grid(row=2, column=0, sticky=tk.W)
        self.kd_var = tk.DoubleVar(value=self.pid.Kd)
        self.kd_scale = ttk.Scale(gains_frame, from_=0.0, to=2.0, variable=self.kd_var,
                                 orient=tk.HORIZONTAL, length=200)
        self.kd_scale.grid(row=2, column=1, padx=5)
        self.kd_label = ttk.Label(gains_frame, text=f"{self.kd_var.get():.2f}")
        self.kd_label.grid(row=2, column=2)
        
        # Bind scale events
        self.kp_scale.bind("<Motion>", self.update_gain_labels)
        self.ki_scale.bind("<Motion>", self.update_gain_labels)
        self.kd_scale.bind("<Motion>", self.update_gain_labels)
        
        # Simulation Controls
        sim_frame = ttk.LabelFrame(parent, text="Simulation Controls", padding=10)
        sim_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_button = ttk.Button(sim_frame, text="Start", command=self.toggle_simulation)
        self.start_button.pack(fill=tk.X, pady=2)
        
        ttk.Button(sim_frame, text="Reset", command=self.reset_simulation).pack(fill=tk.X, pady=2)
        
        # Setpoint control
        setpoint_frame = ttk.LabelFrame(parent, text="Setpoint", padding=10)
        setpoint_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(setpoint_frame, text="Setpoint (rad):").pack()
        self.setpoint_var = tk.DoubleVar(value=0.0)
        setpoint_scale = ttk.Scale(setpoint_frame, from_=-1.0, to=1.0, variable=self.setpoint_var,
                                  orient=tk.HORIZONTAL, length=200)
        setpoint_scale.pack()
        
        # Disturbance control
        dist_frame = ttk.LabelFrame(parent, text="Disturbance", padding=10)
        dist_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(dist_frame, text="Gravity Effect:").pack()
        self.disturbance_var = tk.DoubleVar(value=0.5)
        dist_scale = ttk.Scale(dist_frame, from_=0.0, to=2.0, variable=self.disturbance_var,
                              orient=tk.HORIZONTAL, length=200)
        dist_scale.pack()
        
        # System info
        info_frame = ttk.LabelFrame(parent, text="System Info", padding=10)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.info_text = tk.Text(info_frame, height=8, width=30)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
    def update_gain_labels(self, event=None):
        """Update gain labels when sliders move."""
        self.kp_label.config(text=f"{self.kp_var.get():.2f}")
        self.ki_label.config(text=f"{self.ki_var.get():.2f}")
        self.kd_label.config(text=f"{self.kd_var.get():.2f}")
        
    def setup_animation(self):
        """Setup animation for real-time updates."""
        self.animation = FuncAnimation(self.motor_fig, self.update_animation, 
                                     interval=50, blit=False, cache_frame_data=False)
        
    def update_animation(self, frame):
        """Update animation frame."""
        if self.is_running:
            self.simulation_step()
            
        self.update_visualization()
        return []
        
    def simulation_step(self):
        """Perform one simulation step."""
        
        # Update PID gains
        self.pid.set_gains(self.kp_var.get(), self.ki_var.get(), self.kd_var.get())
        
        # Update setpoint and disturbance
        self.setpoint = self.setpoint_var.get()
        self.plant.set_disturbance(self.disturbance_var.get())
        
        # Get current position
        current_position = self.plant.get_position()
        
        # Compute PID output
        control_output = self.pid.compute(self.setpoint, current_position)
        
        # Update plant
        new_position = self.plant.update(control_output)
        
        # Store data
        self.time += self.plant.dt
        self.time_history.append(self.time)
        self.position_history.append(new_position)
        self.setpoint_history.append(self.setpoint)
        self.control_history.append(control_output)
        
        # Keep reasonable history length
        if len(self.time_history) > 500:
            self.time_history = self.time_history[-500:]
            self.position_history = self.position_history[-500:]
            self.setpoint_history = self.setpoint_history[-500:]
            self.control_history = self.control_history[-500:]
            
    def update_visualization(self):
        """Update the visual elements."""
        
        # Update motor and rod
        current_angle = self.plant.get_position()
        rod_length = 2.0
        
        # Rod end position
        end_x = rod_length * math.cos(current_angle)
        end_y = rod_length * math.sin(current_angle)
        
        # Update rod line
        self.rod_line.set_data([0, end_x], [0, end_y])
        self.rod_end.set_data([end_x], [end_y])
        
        # Update response plot
        if len(self.time_history) > 1:
            self.position_line.set_data(self.time_history, self.position_history)
            self.setpoint_line_plot.set_data(self.time_history, self.setpoint_history)
            
            # Scale control output for visibility
            scaled_control = [c * 0.1 for c in self.control_history]
            self.control_line.set_data(self.time_history, scaled_control)
            
            # Auto-scale axes
            self.response_ax.relim()
            self.response_ax.autoscale_view()
            
        # Update info display
        self.update_info_display()
        
        # Redraw
        self.motor_canvas.draw_idle()
        self.response_canvas.draw_idle()
        
    def update_info_display(self):
        """Update the information display."""
        
        pid_terms = self.pid.get_pid_terms()
        plant_info = self.plant.get_info()
        
        info_text = f"""Time: {self.time:.2f}s

Position: {plant_info['position']:.3f} rad
Velocity: {plant_info['velocity']:.3f} rad/s
Setpoint: {self.setpoint:.3f} rad

PID Terms:
P: {pid_terms['proportional']:.3f}
I: {pid_terms['integral']:.3f}
D: {pid_terms['derivative']:.3f}
Output: {pid_terms['total_output']:.3f}

Plant Parameters:
K: {plant_info['K']:.2f}
ωn: {plant_info['wn']:.2f}
ζ: {plant_info['zeta']:.2f}
"""
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, info_text)
        
    def toggle_simulation(self):
        """Start/stop simulation."""
        self.is_running = not self.is_running
        if self.is_running:
            self.start_button.config(text="Stop")
        else:
            self.start_button.config(text="Start")
            
    def reset_simulation(self):
        """Reset simulation to initial conditions."""
        self.is_running = False
        self.start_button.config(text="Start")
        
        # Reset plant and controller
        self.plant.reset()
        self.pid.reset()
        
        # Clear history
        self.time = 0.0
        self.time_history = []
        self.position_history = []
        self.setpoint_history = []
        self.control_history = []
        
        # Clear plots
        self.position_line.set_data([], [])
        self.setpoint_line_plot.set_data([], [])
        self.control_line.set_data([], [])
        
        # Reset visualization
        self.rod_line.set_data([0, 2], [0, 0])
        self.rod_end.set_data([2], [0])
        
        self.motor_canvas.draw_idle()
        self.response_canvas.draw_idle()
        
    def run(self):
        """Start the GUI main loop."""
        self.root.mainloop()
