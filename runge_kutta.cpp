/*
Name: Austin Kingsland
Project: Solving Differential Equations using Runge-Kutta Method (RK4)

Description:
This project demonstrates C++ programming and mathematical skills by 
implementing the fourth-order Runge-Kutta (RK4) method to solve the ordinary differential equation (ODE) 
of a damped harmonic oscillator. The ODE is given by:
    d²y/dt² + 2ζω₀dy/dt + ω₀²y = 0
where ζ (zeta) is the damping ratio and ω₀ (omega0) is the natural frequency. 
The RK4 method provides an efficient and accurate way to approximate the solution of this second-order ODE by 
converting it into a system of first-order ODEs. The results are saved to a CSV file for further analysis and visualization.

*/

#include <iostream>
#include <vector>
#include <fstream>
#include <cmath>

// Define constants for the damped harmonic oscillator
const double omega0 = 1.0;   // Natural frequency
const double zeta = 0.1;     // Damping ratio

// Function prototypes
void rungeKutta(double t0, double y0, double v0, double t_end, double h);
std::vector<double> derivatives(double t, double y, double v);

int main() {
    // Initial conditions
    double t0 = 0.0;
    double y0 = 1.0;     // Initial position
    double v0 = 0.0;     // Initial velocity
    double t_end = 10.0; // End time
    double h = 0.01;     // Time step

    rungeKutta(t0, y0, v0, t_end, h);

    return 0;
}

// Function to compute derivatives
std::vector<double> derivatives(double t, double y, double v) {
    std::vector<double> dydt(2);
    dydt[0] = v;
    dydt[1] = -2 * zeta * omega0 * v - omega0 * omega0 * y;
    return dydt;
}

// Function implementing the fourth-order Runge-Kutta method
void rungeKutta(double t0, double y0, double v0, double t_end, double h) {
    double t = t0;
    double y = y0;
    double v = v0;

    // Output file to store results
    std::ofstream outputFile("damped_oscillator_solution.csv");
    outputFile << "t,y,v\n";

    while (t <= t_end) {
        outputFile << t << "," << y << "," << v << "\n";

        // Compute k1
        std::vector<double> k1 = derivatives(t, y, v);
        // Compute k2
        std::vector<double> k2 = derivatives(t + h / 2.0, y + h * k1[0] / 2.0, v + h * k1[1] / 2.0);
        // Compute k3
        std::vector<double> k3 = derivatives(t + h / 2.0, y + h * k2[0] / 2.0, v + h * k2[1] / 2.0);
        // Compute k4
        std::vector<double> k4 = derivatives(t + h, y + h * k3[0], v + h * k3[1]);

        // Update the next values
        y += (h / 6.0) * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]);
        v += (h / 6.0) * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]);
        t += h;
    }

    outputFile.close();
    std::cout << "Results have been written to damped_oscillator_solution.csv\n";
}
