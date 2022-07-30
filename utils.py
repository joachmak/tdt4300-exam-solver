import math
from statistics import median

import const
import distances


def get_list_str_without_citation_marks(l: list):
    """ Convert a list that would be printed on the form ['A', 'B', 'C'] to a string on the form "[A, B, C]" """
    string = "["
    for i in range(len(l)):
        string += l[i]
        if i + 1 < len(l):
            string += ", "
    string += "]"
    return string


def print_itemset(itemsets: list):
    # get all 1-itemsets then all 2-itemset ... etc., sort each itemset and concat
    itemsets_dict = {}
    for itemset in itemsets:
        if len(itemset) in itemsets_dict:
            itemsets_dict[len(itemset)].append(itemset)
        else:
            itemsets_dict[len(itemset)] = [itemset]
    # sort
    result = []
    for i in range(1, 10):
        if i not in itemsets_dict:
            continue
        sorted_itemsets = itemsets_dict[i]
        for itemset in sorted_itemsets:
            itemset.sort()
        sorted_itemsets.sort()
        result += sorted_itemsets
    print("[")
    for item in result:
        print(f"{get_list_str_without_citation_marks(item)},")
    print("]")


def str_to_arr(string: str):
    """ Convert string to array of characters. E.g. "ABC" -> ['A','B','C'] """
    res: list = []
    for char in string:
        res.append(char)
    return res


def is_equal_len(x, y, error_msg=None):
    equal = len(x) == len(y)
    if equal or error_msg is None:
        return equal
    print(error_msg)
    return equal


def vector_len(x):
    result = 0
    for dim in x:
        result += dim ** 2
    return round(math.sqrt(result), 5)


def vector_multiply(x: list, y: list):
    if not is_equal_len(x, y, "The points do not have equal dimensions"):
        return -1
    result = 0
    for i in range(len(x)):
        result += x[i] * y[i]
    return result


def calculate_distance_with_proximity_str(x: list, y: list, proximity_str: str):
    if proximity_str == const.COSINE:
        return distances.cosine_similarity(x, y)
    elif proximity_str == const.MANHATTAN:
        return distances.manhattan_distance(x, y)
    elif proximity_str == const.SQUARED_EUCLIDEAN:
        return distances.squared_euclidean_distance(x, y)
    elif proximity_str == const.EUCLIDEAN:
        return distances.euclidean_distance(x, y)
    else:
        print("ERROR: REQUESTED PROXIMITY FUNCTION NOT IMPLEMENTED D:")
        return 0


def find_avg_point(points: list, prepend_str=""):
    if len(points) == 0:
        print("ERROR: No points given, cannot find average")
        return None
    dimension_size = len(points[0].coordinates)
    avg_point = [0] * dimension_size
    calculations = [""] * dimension_size
    for point in points:
        for i in range(dimension_size):
            avg_point[i] += point.coordinates[i]
            calculations[i] += f"{point.coordinates[i]}+"
    for i in range(dimension_size):
        avg_point[i] = avg_point[i] / len(points)
    print_str = "("
    for calculation in calculations:
        for i in range(dimension_size):
            print_str += calculation[0:-1]
        print_str += f" / {len(points)}, "
    print_str += f") = {avg_point}"
    print(prepend_str + print_str)
    return avg_point


def find_median_point(points: list, prepend_str=""):
    if len(points) == 0:
        print("ERROR: No points given, cannot find average")
        return None
    dimension_size = len(points[0].coordinates)
    median_point = []
    for i in range(dimension_size):
        median_point.append([])
    for point in points:
        for i in range(dimension_size):
            median_point[i].append(point.coordinates[i])
    print_str = prepend_str + "("
    i = 0
    for point_list in median_point:
        point_list.sort()
        last_idx = i == dimension_size - 1
        print_str += f"median({str_obj_list(point_list)})"
        if not last_idx:
            print_str += ", "
        i += 1
    print_str += ") = "
    for i in range(dimension_size):
        median_point[i] = median(median_point[i])
    print_str += str(tuple(median_point))
    print(print_str)
    return median_point


def str_obj_list(li: list):
    """ Convert list of objects to string format """
    res = "["
    i = 0
    for obj in li:
        last_idx = i == len(li) - 1
        res += str(obj)
        if not last_idx:
            res += ", "
        i += 1
    res += "]"
    return res

