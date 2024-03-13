import csv
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # Radius of the Earth in kilometers
    return distance

def add_distance_to_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        csv_reader = csv.reader(infile)
        csv_writer = csv.writer(outfile)

        # Read and store the header
        header = next(csv_reader)
        
        # Write the header to the output file
        csv_writer.writerow(header)

        for row in csv_reader:
            source_lat = float(row[5])  #source latitude
            source_lon = float(row[6])  #Sourec longitude
            dest_lat = float(row[14])    #Destination latitude
            dest_lon = float(row[15])    #Destination longitude

            # Calculate distance using Haversine formula
            distance = haversine(source_lat, source_lon, dest_lat, dest_lon)

            # Append the distance to the current row
            row.append(distance)

            # Write the modified row to the output file
            csv_writer.writerow(row)


def csv_to_array(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data_array = []
        for row in csv_reader:
            data_array.append(row)
    return data_array

def print_data(data):
    for row in data:
        # Joining each element of the row into a string
        # and explicitly encoding it to UTF-8 before printing
        print(', '.join(row).encode('utf-8').decode('utf-8'))


csv_file_input = 'flight_routes.csv'
csv_file_output = 'flight_routes_distance.csv'
data = csv_to_array(csv_file_input)
#print_data(data)
add_distance_to_csv(csv_file_input,csv_file_output)

