import numpy as np
import itertools
from matplotlib import pyplot as plt


def p90_parameters() -> tuple:
    """
    Collect all the P90 parameters from the User
    P90 parameters are parameters with 90% confidence
    :return:
    """
    p90_keys = ['P90 area', 'P90 thickness', 'P90 porosity', 'P90 saturation', 'P90 pressure', 'P90 surface']

    # create a list of input values for the corresponding keys
    p90_values = [float(input(f'{key}: ')) for key in p90_keys]
    p90_tuple = tuple(zip(p90_keys, p90_values))

    return p90_tuple


def p10_parameters() -> tuple:
    """
    Collect all the P10 parameters from the User
    P10 parameters are parameters with 10% confidence
    :return:
    """
    p10_keys = ['P10 area', 'P10 thickness', 'P10 porosity', 'P10 saturation', 'P10 pressure', 'P10 surface']

    # create a list of input values for the corresponding keys
    p10_values = [float(input(f'{key}: ')) for key in p10_keys]
    p10_tuple = tuple(zip(p10_keys, p10_values))

    return p10_tuple


# create a range of values from P90 to P10 with a particular step
def convert_parameters_to_parameter_ranges() -> list:
    """
    Convert P90 and P10 values for particular parameter into a range of values
    :return:
    """
    parameter_titles = ['area_values', 'thickness_values', 'porosity_values', 'saturation_range', 'pressure_range', 'surface_range']

    # Using '*' to get rid of the redundant parentheses
    input_parameters = [*p90_parameters(), *p10_parameters()]
    ranges = []

    for parameter in range(len(parameter_titles)):
        y = np.arange(input_parameters[parameter][1], input_parameters[parameter + len(parameter_titles)][1] + 0.5, 0.5)
        ranges.append(y)

    return ranges

    # area_values = np.arange(P90_area, P10_area + 0.1, 0.1)
    # thickness_values = np.arange(P90_thickness, P10_thickness + 0.1, 0.1)
    # porosity_values = np.arange(P90_porosity, P10_porosity + 0.1, 0.1)
    # saturation_range = np.arange(P90_saturation, P10_saturation + 0.1, 0.1)
    # pressure_range = np.arange(P90_pressure, P10_pressure + 10, 10)
    # surface_range = np.arange(P90_surface, P10_surface + 0.1, 0.1)


def convert_ranges_to_cartesian_product() -> list:
    """
    Combine all the parameter ranges, e.g. [[a1, a2, a3], [b1, b2, b3], [c1, c2, c3]
    into Cartesian product, e.g. [(a1, b1, c1), (a1, b1, c2), (a1, b1, c3) ... (a3, b3, c1), (a3, b3, c2), (a3, b3, c3)])
    :return:
    """
    area_values, thickness_values, porosity_values, saturation_range, pressure_range, surface_range = convert_parameters_to_parameter_ranges()

    list_of_tuples = list(itertools.product(area_values,
                                            thickness_values,
                                            porosity_values,
                                            saturation_range,
                                            pressure_range,
                                            surface_range))
    return list_of_tuples


def get_cartesian_product_list() -> list:
    """
    Convert list of tuples into list of lists
    :return:
    """
    list_of_tuples = convert_ranges_to_cartesian_product()
    list_of_lists = [list(value) for value in list_of_tuples]

    return list_of_lists


def multiply_each_combination() -> list:
    """
    Create a list with multiplied values and sort these ('np.prod' returns a product for each list)
    :return:
    """
    cartesian_combinations = get_cartesian_product_list()
    multiplied_values = [np.prod(np.array(i)) for i in cartesian_combinations]

    return multiplied_values


def sort_multiplied_combinations() -> list:
    """
    Sort multiplied combinations
    :return:
    """
    sorted_multiplied_combinations = sorted(multiply_each_combination())

    return sorted_multiplied_combinations


def convert_to_decimal() -> list:
    """
    Make all the values float with precision of up to two decimals
    :return:
    """
    values = sort_multiplied_combinations()
    decimal_values = [float(f'{value:.2f}') for value in values]
    total_values = len(decimal_values)
    print(f'Total cartesian combinations: {total_values}')

    return decimal_values


def counter() -> dict:
    """
    Create a dictionary that counts all the similar/unique objects
    TODO: should I use collections.Counter() instead?
    """
    list_of_values = convert_to_decimal()
    counted_values = {value: list_of_values.count(value) for value in list_of_values}
    unique_values = len(counted_values)
    print(f'Total unique values: {unique_values}')

    return counted_values


def probability() -> dict:
    """
    Calculate a probability by dividing value by the total number of elements in the list
    :return:
    """
    x = counter()
    probability_dict = {k: v/sum(x.values()) for k, v in x.items()}
    max_probability = sum(prob for key, prob in probability_dict.items())
    print(f'Max probability: {round(max_probability, 2)}')

    return probability_dict


def print_report():
    """
    Print report
    :return:
    """
    probability_mass = probability()
    x_values = list(probability_mass.keys())
    y_probability = list(probability_mass.values())

    x_values_min = min(x_values)
    x_values_max = max(x_values)
    x_values_max_probable = max(probability_mass, key=probability_mass.get)
    x_values_mean = np.mean(x_values)

    print(f'P90 is: {x_values_min}')
    print(f'P10 is: {x_values_max}')
    print(f'Most probable: {x_values_max_probable}')
    print(f'Mean: {x_values_mean}')

    printable_data = [x_values,
                      y_probability,
                      x_values_min,
                      x_values_max,
                      x_values_mean,
                      x_values_max_probable]

    return printable_data


def print_diagram():
    """
    Print diagram
    :return:
    """    # print(min(y_probability), max(y_probability))

    data = print_report()
    plt.plot(data[0], data[1])
    plt.xlabel('Hydrocarbons')
    plt.ylabel('Probability')
    plt.axvline(x=data[4], color='red')
    plt.axvline(x=data[5], color='yellow')
    plt.show()


print(print_diagram())

