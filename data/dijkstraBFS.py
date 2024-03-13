import heapq
import csv
from collections import deque

# Function to find the shortest path using Dijkstra's algorithm
def dijkstra(graph, source, destination):
    # Initialize distances
    distances = {node: float('inf') for node in graph}
    distances[source] = 0

    """
    heapq is used to create a priority queue so that dijkstra will explore nodes with the shortest distance first
    to ensure that if efficently looks for the shortest path
    """
    # Initialize priority queue
    priority_queue = [(0, source)]  # (distance, node)
    heapq.heapify(priority_queue)

    # Initialize previous nodes
    previous = {}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == destination:
            # Destination reached, backtrack to find the shortest path
            path = []
            while current_node in previous:
                path.insert(0, current_node)
                current_node = previous[current_node]
            path.insert(0, source)
            return path, distances[destination]

        if current_distance > distances[current_node]:
            # Skip if the distance to this node is not the shortest
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return None, float('inf')  # No path found

#creating a Breath-First-Search to find 3 of shortest possible distance
def bfs_shortest_paths(graph, source, destination, num_paths=3):
    shortest_paths = []  # List to store the shortest paths
    
    # Queue to perform BFS
    queue = deque([(source, [source])])  # (node, path)
    
    while queue and len(shortest_paths) < num_paths:
        current_node, current_path = queue.popleft()  # Dequeue the node and its path
        
        # If the current node is the destination, add its path to the list of shortest paths
        if current_node == destination:
            shortest_paths.append(current_path)
            continue
        
        # Explore neighbors of the current node
        for neighbor in graph[current_node]:
            if neighbor not in current_path:  # Avoid cycles
                queue.append((neighbor, current_path + [neighbor]))
    
    return shortest_paths

# Function to construct the graph from a CSV file
# type of graph use is adjacency list
def construct_graph_from_csv(csv_file, directed=False):
    graph = {}
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row if present
        for row in csv_reader:
            source_airport = row[4]  #source airport name
            destination_airport = row[13]  #destination airport name
            distance = float(row[18])  #distance

            # Add the source airport to the graph if not already present
            if source_airport not in graph:
                graph[source_airport] = {}

            # Add the destination airport and distance to the source airport's connections
            graph[source_airport][destination_airport] = distance

            # If the graph is undirected, add the reverse connection
            if not directed:
                if destination_airport not in graph:
                    graph[destination_airport] = {}
                graph[destination_airport][source_airport] = distance

    return graph

# Function to print the graph
#Python tries to encode a Unicode character that cannot be mapped to the output encoding
#hence a print function needs to be created to encode and decode
def print_graph(graph):
    for source, destinations in graph.items():
        print(f"Source: {source}")
        for destination, distance in destinations.items():
            # Encode destination to a compatible encoding before printing
            encoded_destination = destination.encode('utf-8').decode('utf-8', 'ignore')
            print(f"  Destination: {encoded_destination}, Distance: {distance}")


#Function to verify the calculation of distance of dijkstra
def calculate_distance(graph, path):
    total_distance = 0
    for i in range(len(path) - 1):
        source = path[i]
        destination = path[i + 1]
        total_distance += graph[source][destination]
    return total_distance

#Function to calculate the distance of the path for BFS
def calculate_path_distance(graph, path):
    total_distance = 0
    for i in range(len(path) - 1):
        source = path[i]
        destination = path[i + 1]
        total_distance += graph[source][destination]
    return total_distance

# Example usage:
csv_file = 'flight_routes_distance.csv'
graph = construct_graph_from_csv(csv_file, directed=False)  # Change directed to True if the graph contains one-way connections
#print_graph(graph)

# Input source and destination airports
source_airport = input("Enter source airport: ")
destination_airport = input("Enter destination airport: ")

print("----------------------------------------------")
print("Using Djistra to find the shortest distance\n")
# Check if the source and destination airports are present in the graph
if source_airport not in graph:
    print(f"Source airport '{source_airport}' is not present in the graph.")
elif destination_airport not in graph:
    print(f"Destination airport '{destination_airport}' is not present in the graph.")
else:
    # Find shortest path and distance using Dijkstra's algorithm
    shortest_path, shortest_distance = dijkstra(graph, source_airport, destination_airport)
    print("Shortest path:", shortest_path)
    print("Shortest distance:", shortest_distance)
    print("\n")
    # Verify shortest distance
    calculated_distance = calculate_distance(graph, shortest_path)
    print("Calculated distance along the shortest path:", calculated_distance)

print("\n")
print("----------------------------------------------")
print("Using BFS to find the 3 possible shortest distance\n")
# Find and print the three shortest paths using BFS
# Find and print the three shortest paths using BFS
shortest_paths = bfs_shortest_paths(graph, source_airport, destination_airport, num_paths=3)
if shortest_paths:
    # Sort the shortest paths based on their distances
    shortest_paths.sort(key=lambda path: calculate_path_distance(graph, path))
    
    print("Three shortest paths (in ascending order of distance):")
    for path in shortest_paths:
        distance = calculate_path_distance(graph, path)
        print("Path:", path)
        print("Distance:", distance)
else:
    print("No paths found between the source and destination.")
    