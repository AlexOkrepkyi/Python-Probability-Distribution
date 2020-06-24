import numpy as np
import itertools
from collections import Counter
from matplotlib import pyplot as plt
from decimal import *


# P90 values (90% confidence)
P90_area = float(input('P90 area: '))
P90_thickness = float(input('P90 thickness: '))
P90_porosity = float(input('P90 porosity: '))
P90_saturation = float(input('P90 saturation: '))
P90_pressure = float(input('P90 pressure: '))
P90_surface = float(input('P90 surface: '))

# P10 values (10% confidence)
P10_area = float(input('P10 area: '))
P10_thickness = float(input('P10 thickness: '))
P10_porosity = float(input('P10 porosity: '))
P10_saturation = float(input('P10 saturation: '))
P10_pressure = float(input('P10 pressure: '))
P10_surface = float(input('P10 surface: '))

# create a range of values from P90 to P10 with a particular step
area_values = np.arange(P90_area, P10_area + 0.1, 0.1)
thickness_values = np.arange(P90_thickness, P10_thickness + 0.1, 0.1)
porosity_values = np.arange(P90_porosity, P10_porosity + 0.1, 0.1)
saturation_range = np.arange(P90_saturation, P10_saturation + 0.1, 0.1)
pressure_range = np.arange(P90_pressure, P10_pressure + 10, 10)
surface_range = np.arange(P90_surface, P10_surface + 0.1, 0.1)

# print(area_values)
# print(thickness_values)
# print(porosity_values)

# combine all the lists into Cartesian product (i.e. [(a1, t1, p1), (a1, t1, p2) etc.])
list_of_tuples = list(itertools.product(area_values,
                                        thickness_values,
                                        porosity_values,
                                        saturation_range,
                                        pressure_range,
                                        surface_range))
# print(list_of_tuples)

# convert list of tuples into list of lists
list_of_lists = [list(elem) for elem in list_of_tuples]
print(list_of_lists)

# create a list with multiplied values and sort these ('np.prod' returns a product for each list)
multiplied_values = []
for i in list_of_lists:
    i = np.prod(np.array(i))
    multiplied_values.append(i)
multiplied_values = sorted(multiplied_values)

# getcontext().prec = 3
# ['%.2f' % elem for elem in multiplied_values]
rounded_values = [float(Decimal('%.2f' % elem)) for elem in multiplied_values]
# print('ROUNDED VALUES: ', rounded_values)
print('TOTAL NUMBER OF VALUES: ', len(multiplied_values))

# create a dictionary that counts all the similar/unique objects
counts = Counter(rounded_values)
# print('COUNTS ARE: ', counts)

# counts all the values
total = sum(counts.values())
print('TOTAL: ', total)

# calculate a probability by dividing value by the total number of elements in the list
probability_mass = {k: v/total for k, v in counts.items()}
# print('PROBABILITY MASS: ', probability_mass)

x_values = list(probability_mass.keys())
# print(min(x_values), max(x_values))

y_probability = list(probability_mass.values())
# print(min(y_probability), max(y_probability))

x_values_min = min(x_values)
print('P90 is: ', x_values_min)

x_values_max = max(x_values)
print('P10 is: ', x_values_max)

x_values_max_probable = max(probability_mass, key=probability_mass.get)
print('VALUE WITH MAX PROBABILITY: ', x_values_max_probable)

x_values_mean = np.mean(x_values)
print('MEAN IS: ', x_values_mean)


plt.plot(x_values, y_probability)
plt.xlabel('Hydrocarbons')
plt.ylabel('Probability')
plt.axvline(x=x_values_mean, color='red')
plt.axvline(x=x_values_max_probable, color='yellow')
plt.show()