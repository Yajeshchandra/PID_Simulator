# PID Motor Rod Simulation

Educational PID control system for learning PID tuning with a motor and rod plant.

## Overview

This simulation demonstrates PID control of a motor with an attached rod that needs to be kept horizontal against gravity. It's designed for educational purposes to help understand:

- How PID controllers work
- The effect of each PID term (P, I, D)
- Real-time system response
- PID tuning strategies

## Files

- `main.py` - Main application entry point
- `plant.py` - Second-order motor-rod plant model
- `pid_controller.py` - **PID controller template for students to complete**
- `gui.py` - Real-time visualization GUI
- `requirements.txt` - Required Python packages

## System Description

### Plant Model
The system represents a motor trying to keep a rod at a setpoint against gravity. It's modeled as a second-order system:

```
G(s) = K / (s² + 2ζωₙs + ωₙ²)
```

Where:
- K = System gain (1.0)
- ωₙ = Natural frequency (2.0 rad/s)
- ζ = Damping ratio (0.1, underdamped)

### Control Objective
Keep the rod at setpoint despite:
- Gravity disturbance
- System noise
- Changing setpoints

## Quick Start

1. Clone Repo
   ```bash
   git clone https://github.com/your-username/pid-motor-rod-simulation.git
   cd PID_Simulator
   ```

2. Install requirements (Python 3.12.6 or compatible will work for simulation):
   ```
   pip install -r requirements.txt
   ```

3. Run the simulation:
   ```
   python main.py
   ```

## Implementing Your PID Controller

### Step 1: Open the Template
The main PID controller file (`pid_controller.py`) is now a template with TODOs that you need to complete.

### Step 2: Complete the Implementation
Edit `pid_controller.py` and fill in the TODOs in the `PIDController` class:
- Add necessary state variables in `__init__()` (like previous_error, integral)
- Implement the PID algorithm in `compute()` method
- Complete the `reset()` method to clear accumulated state
- The other methods are already implemented for GUI integration

### Step 3: Test Your Implementation
Run `python main.py` and use the GUI to test and tune your PID controller.

## Demo Video

🎥 **Watch the PID Tuning Demo: `demo.mp4`**

The demo video showcases two scenarios to help you understand the impact of PID tuning:

### **Well-Tuned System Example**
- Smooth response to setpoint changes
- Quick settling time with minimal overshoot
- Effective disturbance rejection

### **Poorly-Tuned System Example**
- Excessive oscillations
- Large overshoot and long settling times

## GUI Features

### Visualization
- **Motor & Rod Display**: Real-time visual representation of the motor and rod position
- **Response Plot**: Time history of position, setpoint, and control output

### Controls
- **PID Gains**: Real-time tuning of Kp, Ki, and Kd
- **Setpoint**: Change desired rod position
- **Disturbance**: Adjust gravity effect
- **Start/Stop**: Control simulation
- **Reset**: Return to initial conditions

## PID Tuning Guide

### Step 1: Proportional (Kp)
1. Set Ki = 0, Kd = 0
2. Increase Kp until system oscillates
3. Reduce Kp to 60-70% of oscillation point

### Step 2: Integral (Ki)
1. Slowly increase Ki to eliminate steady-state error
2. Stop when system becomes unstable
3. Reduce Ki if overshoot is too large

### Step 3: Derivative (Kd)
1. Add small amount of Kd to reduce overshoot
2. Increase until settling time improves
3. Avoid excessive Kd (amplifies noise)

## Learning Objectives

After using this simulation, students should understand:
1. How each PID term affects system response
2. Trade-offs between performance metrics
3. Practical tuning procedures
4. Real-world control challenges
5. Importance of system modeling

## Troubleshooting

**Common Issues:**
- Import errors: Install required packages
- Slow performance: Reduce animation interval in `gui.py`
- Instability: Reduce PID gains, especially Ki and Kd

---

**Note**: This is an educational tool. Real-world PID tuning may require additional considerations like sensor noise, actuator limits, and safety constraints.
