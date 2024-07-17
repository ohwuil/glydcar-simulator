from flask import Flask, request, jsonify
import pandas as pd
import datetime
from math import radians, sin, cos, sqrt, atan2
from collections import deque
import heapq

app = Flask(__name__)

# Define stations and connections
stations = [
    {"name": "A", "lat": 38.01699345044407, "lon": -121.94638573082345},
    {"name": "B", "lat": 38.01837994162642, "lon": -121.95760346848552},
    {"name": "C", "lat": 38.01973230013453, "lon": -121.96459866921425},
    {"name": "D", "lat": 38.026595134855945, "lon": -121.95498563262994},
    {"name": "E", "lat": 38.02673035666877, "lon": -121.94545842672945},
    {"name": "F", "lat": 38.02666274580736, "lon": -121.93923570170942},
    {"name": "G", "lat": 38.02689549995812, "lon": -121.9321178052867},
    {"name": "H", "lat": 38.02689938359431, "lon": -121.92610360658814},
    {"name": "I", "lat": 38.02967136956211, "lon": -121.91104032020498},
    {"name": "J", "lat": 38.03149676632553, "lon": -121.90674878601556},
    {"name": "K", "lat": 38.03197000991321, "lon": -121.90069772280849},
    {"name": "L", "lat": 38.03261226412525, "lon": -121.8833170083404},
    {"name": "M", "lat": 38.02635849624187, "lon": -121.88610650556352},
    {"name": "N", "lat": 38.02108463378863, "lon": -121.88778020400991},
    {"name": "O", "lat": 38.01695993843636, "lon": -121.8895826483695},
    {"name": "P", "lat": 38.01259832763476, "lon": -121.89099885474108},
    {"name": "Q", "lat": 38.0113134625897, "lon": -121.88597775973945},
    {"name": "R", "lat": 38.01107677446706, "lon": -121.88580609837187},
    {"name": "S", "lat": 38.01002857493957, "lon": -121.88155747896411},
    {"name": "T", "lat": 38.00921705539965, "lon": -121.87636472259491},
    {"name": "U", "lat": 38.0084055268009, "lon": -121.87164403474979},
    {"name": "V", "lat": 38.00823645722786, "lon": -121.86692334714142},
    {"name": "W", "lat": 38.00806738726494, "lon": -121.86078645325057},
    {"name": "X", "lat": 38.00378938397287, "lon": -121.85056791253373},
    {"name": "Y", "lat": 38.00331720142464, "lon": -121.84540926125906},
    {"name": "Z", "lat": 38.00329667167967, "lon": -121.83806209126182},
    {"name": "AA", "lat": 38.00596549034543, "lon": -121.83464904382069},
    {"name": "AB", "lat": 38.01078964686703, "lon": -121.83045438256431},
    {"name": "AC", "lat": 38.015757169897796, "lon": -121.82026734853966},
    {"name": "AD", "lat": 38.01787134405292, "lon": -121.81609874144903},
    {"name": "AE", "lat": 38.01707083871175, "lon": -121.81109641252044},
    {"name": "AF", "lat": 38.00958262249506, "lon": -121.80581586558077},
    {"name": "AG", "lat": 38.006076205786805, "lon": -121.80609184583933},
    {"name": "AH", "lat": 38.00509764096123, "lon": -121.80243510741363},
    {"name": "AI", "lat": 38.00485299771418, "lon": -121.78853260188956},
    {"name": "AJ", "lat": 37.99596526145414, "lon": -121.78069165047567},
    {"name": "AK", "lat": 37.99323616265046, "lon": -121.75833942391635},
    {"name": "AL", "lat": 37.983608625886056, "lon": -121.7424867043436},
    {"name": "AM", "lat": 37.97976240057517, "lon": -121.74080766373412},
    {"name": "AN", "lat": 37.98311235002304, "lon": -121.7323599914176},
    {"name": "AO", "lat": 37.986875691066096, "lon": -121.71457265653993},
    {"name": "AP", "lat": 37.99072154357454, "lon": -121.70617745334363},
    {"name": "AQ", "lat": 37.99502204295972, "lon": -121.7053904031278},
    {"name": "AR", "lat": 37.99795781599213, "lon": -121.7126312651134},
    {"name": "AS", "lat": 37.97393064214193, "lon": -121.73645265215873},
    {"name": "AT", "lat": 37.96966071934799, "lon": -121.7352040878904},
    {"name": "AU", "lat": 37.96528540012603, "lon": -121.73657255611303},
    {"name": "AV", "lat": 37.96210863513287, "lon": -121.7411341168551},
    {"name": "AW", "lat": 37.96151907242513, "lon": -121.75097818623304},
    {"name": "AX", "lat": 37.95767631036896, "lon": -121.74992696372814},
    {"name": "AY", "lat": 37.95496365143684, "lon": -121.74677329551652},
    {"name": "AZ", "lat": 37.950857083949174, "lon": -121.74805319767091},
    {"name": "BA", "lat": 37.947563068616994, "lon": -121.74306367607852},
    {"name": "BB", "lat": 37.94545848150268, "lon": -121.74120710990465}
]

connections = [
    ["A", "B"], ["B", "C"], ["C", "D"], ["D", "E"], ["E", "F"],
    ["F", "G"], ["G", "H"], ["H", "I"], ["I", "J"], ["J", "K"],
    ["K", "L"], ["L", "M"], ["M", "N"], ["N", "O"], ["O", "P"],
    ["P", "Q"], ["Q", "R"], ["R", "S"], ["S", "T"], ["T", "U"],
    ["U", "V"], ["V", "W"], ["W", "X"], ["X", "Y"], ["Y", "Z"],
    ["Z", "AA"], ["AA", "AB"], ["AB", "AC"], ["AC", "AD"], ["AD", "AE"],
    ["AE", "AF"], ["AF", "AG"], ["AG", "AH"], ["AH", "AI"], ["AI", "AJ"],
    ["AJ", "AK"], ["AK", "AL"], ["AL", "AN"], ["AN", "AO"], ["AO", "AP"],
    ["AP", "AQ"], ["AQ", "AR"], ["AK", "AM"], ["AM", "AS"], ["AS", "AT"],
    ["AT", "AU"], ["AU", "AV"], ["AV", "AW"], ["AW", "AX"], ["AX", "AY"],
    ["AY", "AZ"], ["AZ", "BA"], ["BA", "BB"]
]

# Helper function to calculate distance between two coordinates
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of the Earth in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# Helper function to find the shortest path between stations
def find_shortest_path(start, end, connections):
    # Using BFS to find the shortest path
    from collections import deque
    graph = {station["name"]: [] for station in stations}
    for connection in connections:
        graph[connection[0]].append(connection[1])
        graph[connection[1]].append(connection[0])
    queue = deque([(start, [start])])
    visited = set()
    while queue:
        current, path = queue.popleft()
        if current == end:
            return path
        if current in visited:
            continue
        visited.add(current)
        for neighbor in graph[current]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    return []

def find_shortest_path_with_distance(start, end, connections):
    # Using BFS to find the shortest path
    from collections import deque
    graph = {station["name"]: [] for station in stations}
    for connection in connections:
        graph[connection[0]].append(connection[1])
        graph[connection[1]].append(connection[0])
    queue = deque([(start, [start], 0)])
    visited = set()
    while queue:
        current, path, distance = queue.popleft()
        if current == end:
            return path, distance
        if current in visited:
            continue
        visited.add(current)
        for neighbor in graph[current]:
            if neighbor not in visited:
                start_station = next(st for st in stations if st["name"] == current)
                end_station = next(st for st in stations if st["name"] == neighbor)
                segment_distance = calculate_distance(start_station["lat"], start_station["lon"], end_station["lat"], end_station["lon"])
                queue.append((neighbor, path + [neighbor], distance + segment_distance))
    return [], 0

# Main simulation function
def run_simulation(start_time, end_time, riders, glydcars):
    simulation_results = []
    total_ride_time = 0
    total_wait_time = 0
    total_distance_traveled = 0
    num_rides = 0
    # Convert start and end time to datetime objects
    start_time = datetime.datetime.strptime(start_time, '%H:%M:%S')
    end_time = datetime.datetime.strptime(end_time, '%H:%M:%S')
    current_time = start_time

    # Initialize glydcar statuses
    glydcar_statuses = []
    for glydcar in glydcars:
        glydcar_statuses.append({
            "glydcar": glydcar["glydcar"],
            "current_station": glydcar["start_station"],
            "available_from": datetime.datetime.strptime(glydcar["availability_start"], '%H:%M:%S'),
            "available_until": datetime.datetime.strptime(glydcar["availability_end"], '%H:%M:%S'),
            "is_available": True
        })

    # Main simulation loop
    while current_time <= end_time:
        # Process each rider request
        for rider in list(riders):  # Use a copy of the list for iteration
            request_time = datetime.datetime.strptime(rider["start_time"], '%H:%M:%S')
            if request_time > current_time:
                continue  # Skip riders whose request time is later than the current simulation time

            # Find an available glydcar
            available_glydcar = None
            travel_time_to_pickup = 0
            for status in glydcar_statuses:
                if status["is_available"] and status["available_from"] <= current_time <= status["available_until"]:
                    path_to_pickup, distance_to_pickup = find_shortest_path_with_distance(status["current_station"], rider["start_station"], connections)
                    travel_time_to_pickup = (distance_to_pickup / 30) * 60  # Convert distance to travel time in minutes
                    available_glydcar = status
                    break

            if available_glydcar:
                # Calculate the path and time required for the ride
                path, total_distance = find_shortest_path_with_distance(rider["start_station"], rider["end_station"], connections)
                travel_time = (total_distance / 30) * 60  # Convert distance to travel time in minutes
                total_ride_time += travel_time
                total_distance_traveled += total_distance
                num_rides += 1
                ride_start_time = current_time + datetime.timedelta(minutes=3) + datetime.timedelta(minutes=travel_time_to_pickup)  # 3 minutes for pickup plus travel time to pickup
                ride_end_time = ride_start_time + datetime.timedelta(minutes=travel_time)
                wait_time = (ride_start_time - request_time).total_seconds() / 60 - 3  # Exclude 3 minutes pickup time
                total_wait_time += max(wait_time, 0)  # Ensure non-negative wait time

                # Update glydcar status
                available_glydcar["is_available"] = False
                available_glydcar["current_station"] = rider["end_station"]
                available_glydcar["available_from"] = ride_end_time + datetime.timedelta(minutes=3)  # 3 minutes for drop-off

                # Log the ride
                simulation_results.append({
                    "rider": rider["rider"],
                    "start_station": rider["start_station"],
                    "end_station": rider["end_station"],
                    "total_ride_time": travel_time,
                    "total_wait_time": max(wait_time, 0),
                    "total_distance": total_distance,
                    "ride_start_time": ride_start_time.strftime('%H:%M:%S'),
                    "ride_end_time": ride_end_time.strftime('%H:%M:%S'),
                    "glydcar": available_glydcar["glydcar"]
                })

                # Remove the rider from the list as they have been served
                riders.remove(rider)

        # Update glydcar availability based on current time
        for status in glydcar_statuses:
            if not status["is_available"] and status["available_from"] <= current_time:
                status["is_available"] = True

        # Increment the simulation time
        current_time += datetime.timedelta(seconds=1)

    # Calculate average times
    average_ride_time = total_ride_time / num_rides if num_rides > 0 else 0
    average_wait_time = total_wait_time / num_rides if num_rides > 0 else 0

    return {
        "average_ride_time": average_ride_time,
        "average_wait_time": average_wait_time,
        "completed_rides": simulation_results,
        "total_distance_traveled": total_distance_traveled
    }

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()
    start_time = data["start_time"]
    end_time = data["end_time"]
    riders = data["riders"]
    glydcars = data["glydcars"]

    result = run_simulation(start_time, end_time, riders, glydcars)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
