from fast_flights import FlightData, Passengers, Result, get_flights
from datetime import datetime

def dumpItenerary(itenerary):
    airports = []
    carriers = []
    departureTimes = []
    arrivalTimes = []
    stops = []
    costs = []
    for flight in itenerary:
        if (flight[1] not in airports):
            airports.append(flight[1])
        if (flight[2] not in airports):
            airports.append(flight[2])

        carriers.append(flight[0].name) # adds the carrier of the flight
        stops.append(flight[0].stops)
        costs.append(flight[0].price)
        departureTimes.append(flight[0].departure)
        arrivalTimes.append(flight[0].arrival)
    
    totalRoute = " -> ".join(airports)
    print(totalRoute)
    totalStops = len(stops)-1
    for stop in stops:
        totalStops += int(stop)
    print(f"    - {totalStops} Stops")
    
    firstFlightTime = departureTimes[0]
    totalTime = julian_to_time(to_julian(arrivalTimes[-1]) - to_julian(departureTimes[0]))
    print(f"    - {totalTime[0]}h{totalTime[1]}m")

    totalCost = 0
    try:
        for cost in costs:
            totalCost += int(cost[1:])
    except:
        totalCost = 1e10


    print("\n") 
    for i in range(len(carriers)):
        print(f"    {airports[i]} -> {airports[i+1]}   via   {carriers[i]} - {costs[i]}")
        print(f"    \t- {int(stops[i])} Stops")
        print(f"    {departureTimes[i]} -> {arrivalTimes[i]}\n")

    print(f"\n Total Cost : ${totalCost}")


    

    return

def appendItenerary(itenerary, newFlight, fromAirport, toAirport):
    if type(itenerary) != list:
        itenerary = list()
    verbose_flight = (newFlight, fromAirport, toAirport)
    itenerary.append(verbose_flight)
    return itenerary

# An Itenerary should be a list of flights, all being tuples. 
# The tuples structure should be (fastFlights type Flight, originatingAirport, destinationAirport)
def flight_finder(date, fromAirport, toAirport, tripType, returnDate ="", maxStops = 1, passengers=(1, 0, 0, 0), overnight=False, seat="economy", airlines=""):
    if tripType == "one-way":
        if airlines != "":
            flight_data=[
                FlightData(date=date, from_airport=fromAirport, to_airport=toAirport, max_stops=maxStops, airlines=airlines)
            ]
        else:
            flight_data=[
                FlightData(date=date, from_airport=fromAirport, to_airport=toAirport, max_stops=maxStops)
            ]
    elif tripType == "round-trip":
        # This does not work. not sure why.
        if airlines != "":
            flight_data=[
                FlightData(date=date, from_airport=fromAirport, to_airport=toAirport, airlines=airlines),
                FlightData(date=returnDate, from_airport=toAirport, to_airport=fromAirport, airlines=airlines)
            ]
        else:
            flight_data=[
                FlightData(date=date, from_airport=fromAirport, to_airport=toAirport),
                FlightData(date=returnDate, from_airport=toAirport, to_airport=fromAirport)
            ]
    
    result: Result = get_flights(
        flight_data=flight_data,
        trip=tripType,
        seat=seat,
        passengers=Passengers(adults=passengers[0], children=passengers[1], infants_in_seat=passengers[2], infants_on_lap=passengers[3]),
        fetch_mode="fallback",
        )
    #if overnight == False:
    #    for flight in result.flights:

    
    return result

def get_compatable_pairs(firstLegFlights, secondLegFlights, minLayover = 1, maxLayover=-1):
    maxLayoverSecs = maxLayover * 1.15741e-5 * 3600
    minLayoverSecs = minLayover * 1.15741e-5 * 3600
    pairs = []
    if maxLayover != -1:
        return
    else:
        for firstLeg in firstLegFlights.flights:
            for secondLeg in secondLegFlights.flights:
                try:
                    if (to_julian(secondLeg.departure) - to_julian(firstLeg.arrival)) >= minLayoverSecs:
                        pairs.append((firstLeg, secondLeg))
                except:
                    print("Error in computing flight time. will not be added.")
                    print(secondLeg.departure)
                    print(firstLeg.arrival)

    return pairs

def to_julian(time_str, year=None):
    if year is None:
        year = datetime.now().year
    
    # Parse the input time string
    dt = datetime.strptime(f"{time_str} {year}", "%I:%M %p on %a, %b %d %Y")
    
    # Convert to Julian Date
    # Formula: JD = unix_time / 86400 + 2440587.5
    julian_date = dt.timestamp() / 86400.0 + 2440587.5
    
    return julian_date

def julian_to_time(julian_day):
    # Ensure we only use the fractional part
    fractional_day = julian_day % 1  
    
    total_hours = fractional_day * 24
    hours = int(total_hours)
    
    total_minutes = (total_hours - hours) * 60
    minutes = int(total_minutes)  # Truncate decimal part
    
    return hours, minutes

def sort_iteneraries_by_cost(itenerary):
    totalCost = 0
    try:
        for flight in itenerary:
            totalCost += int(flight[0].price[1:])
    except:
        totalCost = 1e10
    return totalCost

def sort_iteneraries_by_time(itenerary):
    duration = 0
    firstFlight = itenerary[0][0] # this is the first flight.
    finalFlight = itenerary[-1][0] # this is the final flight
    duration = to_julian(finalFlight.arrival) - to_julian(firstFlight.departure)
    return duration

source = "GRR"
final = "DFW"
startDate = "2025-12-09"
endDate = "2025-12-13"

# These are directs out of the Gerald R Ford Intl' Airport in Grand Rapids, Mi
directs = ["PDX", "LAX", "LAS", "AZA", "PHX", "AUS", "IAH", "DFW", "VPS", "BNA", "DEN", "MSP", "ORD", "MDW", "DTW"
           "BOS", "LGA", "EWR", "PHL", "BWI", "DCA", "RDU", "CLT", "MYR", "ATL", "SAV", "JAX", "VPS", "SFB", "MCO"
           "LAL", "PBI", "FLL", "MIA", "RSW", "PGD", "SRQ", "TPA", "PIE"]

likelyDirects = ["PDX", "LAX", "LAS", "PHX", "AUS", "IAH", "DFW", "DEN", "MDW", "ORD", "ATL", "CLT", "DTW", "MCO", "BNA"]

shortDirects = ["AUS", "IAH", "DFW", "DEN", "MDW", "ORD", "DTW", "ATL"]

usualDirects = ["AUS", "DEN", "ORD", "ATL", "DTW"]

test = ["ORD"]

iteneraries = []
compatable_pairs = []

for connector in test:
    if connector == final:
        continue
    elif connector == source:
        continue
    else:
        firstLegs = flight_finder(startDate, source, connector, "one-way")
        secondLegs = flight_finder(startDate, connector, final, "one-way")
        compatable_pairs = get_compatable_pairs(firstLegs, secondLegs)

        for pair in compatable_pairs:
            currentItenerary = ""
            firstLeg = pair[0]
            secondLeg = pair[1]

            currentItenerary = appendItenerary(currentItenerary, firstLeg, source, connector)
            currentItenerary = appendItenerary(currentItenerary, secondLeg, connector, final)
            iteneraries.append(currentItenerary)

directs = flight_finder(startDate, source, final, "one-way")
for flight in directs.flights:
    currentItenerary = ""
    currentItenerary = appendItenerary(currentItenerary, flight, source, final)
    iteneraries.append(currentItenerary)

g = 1
iteneraries = sorted(iteneraries, key=sort_iteneraries_by_cost)
for itenerary in iteneraries:
    totalCost = 0
    try:
        for flight in itenerary:
            totalCost += int(flight[0].price[1:])
    except:
        totalCost = 1e10
    #print(itenerary)
    if totalCost <= 150:
        print(f"----------\nItenerary {g}\n----------")
        dumpItenerary(itenerary)
        # print(f"TOTAL COST : ${totalCost}")
        print(f"\n----------\n")
        g += 1
    if g >= 10:
        break


    


