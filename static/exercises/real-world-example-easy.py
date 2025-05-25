def total_risk(wind, pressure):
    risk = 5 * wind + 4 * pressure
    return risk

inputs = input("Please enter wind speed and pressure in order, seperated by commas: ")
inputs = inputs.split(',')
wind_speed = int(inputs[0])
pressure = int(inputs[1])

risk = total_risk(pressure, wind_speed)
if 37 < risk < 46:
    print("Stay in the air")
elif risk >= 46:
    print("Fly to another airport")
else:
    print("Land as soon as possible")