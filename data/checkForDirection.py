import csv

def check_connection_type(csv_file):
    one_way_connections = set()
    two_way_connections = set()

    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row if present
        for row in csv_reader:
            source_airport = row[0]  #source airport
            destination_airport = row[9]  #destination airport

            # Check if the connection is already recorded as a one-way connection
            if (source_airport, destination_airport) in one_way_connections:
                # This is a two-way connection
                two_way_connections.add((source_airport, destination_airport))
            else:
                # Record the connection as a one-way connection
                one_way_connections.add((source_airport, destination_airport))

            # Check if the reverse connection exists
            if (destination_airport, source_airport) in one_way_connections:
                # This is a two-way connection
                two_way_connections.add((destination_airport, source_airport))

    if len(one_way_connections) == 0:
        return "The CSV contains only two-way connections (bidirectional edges)."
    elif len(two_way_connections) == 0:
        return "The CSV contains only one-way connections."
    else:
        return "The CSV contains a mixture of one-way and two-way connections."

# Example usage:
csv_file = 'flight_routes.csv'
result = check_connection_type(csv_file)
print(result)
