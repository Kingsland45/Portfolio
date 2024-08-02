import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
data = pd.read_csv('damped_oscillator_solution.csv')

# Plot y (position) vs t (time)
plt.figure(figsize=(10, 6))
plt.plot(data['t'], data['y'], label='Position (y)')
plt.plot(data['t'], data['v'], label='Velocity (v)')
plt.xlabel('Time (t)')
plt.ylabel('Position (y) / Velocity (v)')
plt.title('Damped Harmonic Oscillator')
plt.legend()
plt.grid(True)
plt.show()