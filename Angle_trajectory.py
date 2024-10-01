import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# Number of time steps and servos
time_steps = 11
num_servos = 12

# Example dummy data for the 12 servos over 11 time steps (40° to 90°)
angle_table = [
    [50, 74, 67, 83, 48, 77, 66, 89, 70, 58, 60, 73],
    [84, 59, 67, 48, 64, 85, 50, 53, 69, 76, 75, 45],
    [67, 53, 43, 57, 65, 85, 79, 54, 90, 44, 74, 64],
    [66, 88, 47, 60, 54, 59, 72, 60, 80, 63, 75, 90],
    [82, 45, 40, 51, 47, 78, 79, 52, 85, 48, 59, 66],
    [71, 58, 65, 88, 49, 45, 66, 81, 63, 77, 60, 40],
    [89, 49, 64, 66, 53, 41, 56, 67, 66, 52, 68, 43],
    [46, 72, 77, 45, 74, 67, 88, 42, 59, 61, 51, 83],
    [70, 60, 73, 59, 57, 45, 60, 75, 88, 74, 61, 63],
    [61, 90, 58, 67, 44, 66, 45, 71, 52, 55, 42, 76],
    [44, 86, 54, 49, 77, 82, 73, 89, 58, 72, 43, 69],
]

# Time steps (t = 0 to t = 10)
time = np.arange(time_steps)

# Generate a finer time scale for smooth plotting
time_smooth = np.linspace(time.min(), time.max(), 300)

# Create the plot
plt.figure(figsize=(10, 6))

# Plot each servo's data with interpolation
for servo in range(num_servos):
    # Get the angles for the current servo
    angles = np.array([row[servo] for row in angle_table])

    # Use cubic spline interpolation to smooth the curve
    spline = make_interp_spline(time, angles, k=3)  # k=3 gives a cubic spline
    angles_smooth = spline(time_smooth)

    # Plot the smoothed curve
    plt.plot(time_smooth, angles_smooth, label=f'Servo {servo+1}')

# Add labels and title
plt.title('Servo Angle Movement Over Time')
plt.xlabel('Time')
plt.ylabel('Angle (Degrees)')
plt.legend(title="Servos", loc="upper right")
plt.grid(True)

# Show the plot
plt.show()
