# GlydCar Simulation

## Overview
This Python application simulates the operation of GlydCar, a fictional ride-sharing service. It calculates the shortest path between two points using a breadth-first search (BFS) algorithm and simulates ride-sharing operations, including assigning rides to cars and calculating ride times and distances.

## Asuumptions
- Glydcar will idle for 3 minutes when picking up a rider to allow for rider to get situated before proceeding.  
- Glydcar will idle for 3 minutes when dropping off a rider to allow for rider to exit the car
- These idle times will not count towards the ride or wait time, but will count when determining when the Glydcar is next available to pick up another rider

## Features
- **Shortest Path Calculation**: Utilizes BFS to find the shortest path between two stations.
- **Ride Simulation**: Simulates rides based on provided start and end times, rider requests, and glydcar availability.
- **Distance Calculation**: Computes the distance between two geographical points.

## Requirements
- Python 3.x
- Additional Python libraries: `collections`, `datetime`

## Setup
1. Ensure Python 3.x is installed on your system.
2. Clone this repository to your local machine.
3. No external dependencies are required beyond the standard Python libraries.

## Usage
To run the simulation, execute the `app.py` script from the command line:

```bash
python app.py