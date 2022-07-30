from tabulate import tabulate
from matplotlib import pyplot, axes
import kmeans

import utils


def minkowski_distance(x: list, y: list, r: int):
    if not utils.is_equal_len(x, y, "The points do not have equal dimensions"):
        return -1
    result = 0
    for i in range(len(x)):
        result += (abs(x[i] - y[i])) ** r
    return round(result ** (1 / r), 3)


def euclidean_distance(x: list, y: list, round_to_decimals=3):
    return round(minkowski_distance(x, y, 2), round_to_decimals)


def squared_euclidean_distance(x: list, y: list):
    if not utils.is_equal_len(x, y, "The points do not have equal dimensions"):
        return -1
    result = 0
    for i in range(len(x)):
        result += (abs(x[i] - y[i])) ** 2
    return round(result, 3)


def manhattan_distance(x: list, y: list):
    return minkowski_distance(x, y, 1)


def smc(x: list, y: list):
    if not utils.is_equal_len(x, y, "The points do not have equal dimensions"):
        return -1
    nominator = 0
    for i in range(len(x)):
        if x[i] == y[i]:
            nominator += 1
    result = round(nominator / len(x), 5)
    print(f"SMC = number of matching attribute values / number of attributes = {nominator} / {len(x)} = {result}")
    return result


def jaccard_coefficient(x: list, y: list):
    """ Can only be used for binary data. Use extended Jaccard Coefficient for document data """
    if not utils.is_equal_len(x, y, "The points do not have equal dimensions"):
        return -1
    nominator = 0
    denominator = 0
    for i in range(len(x)):
        if x[i] == 1 and y[i] == 1:
            nominator += 1
        if x[i] != 0 or y[i] != 0:
            denominator += 1
    result = round(nominator / denominator, 5)
    print(f"J = number of matching presences / number of attributes not involved in 00 matches "
          f"= {nominator} / {denominator} = {result}")
    return result


def cosine_similarity(x: list, y: list):
    nominator = utils.vector_multiply(x, y)
    len_x = utils.vector_len(x)
    len_y = utils.vector_len(y)
    result = round(nominator / (len_x * len_y), 5)
    print(f"Cosine similarity: cos(x,y) = x · y / (||x|| · ||y||) = {nominator} / ({len_x} · {len_y}) = {result}")
    return result


def display_points(points_list: list):
    x = []
    y = []
    names = []
    for point in points_list:
        x.append(point.coordinates[0])
        names.append(point.name)
        if len(point.coordinates) > 1:
            y.append(point.coordinates[1])
        else:
            y.append(0)
    pyplot.plot(x, y, 'go-', lw=0)
    pyplot.grid(color='b', linewidth=0.2)
    pyplot.autoscale(enable=None, axis="x", tight=False)
    for i, txt in enumerate(names):
        pyplot.annotate(txt, (x[i], y[i]))
    pyplot.show()


def L_min(x: list, y: list):
    min_arr = []
    for i in range(len(x)):
        min_arr.append(abs(x[i] - y[i]))
    return min(min_arr)


def compute_proximity_matrix(points_list: list):
    """ Takes in a list of Point objects """
    headers = ["ID"]
    for point in points_list:
        headers.append(point.name)
    rows = []
    for point in points_list:
        row = [point.name]
        x = point.coordinates
        for p in points_list:
            y = p.coordinates
            distance = L_min(x, y)  # SELECT DISTANCE MEASURE HERE
            row.append(distance)
        rows.append(row)
    print(tabulate(rows, headers=headers))


def main():
    # x = kmeans.Point([], "")
    x1 = kmeans.Point([3, 15], "a")
    x2 = kmeans.Point([3, 13], "b")
    x3 = kmeans.Point([3, 11], "c")
    x4 = kmeans.Point([3, 8], "d")
    x5 = kmeans.Point([3, 6], "e")
    x6 = kmeans.Point([5, 4], "f")
    x7 = kmeans.Point([5, 12], "g")
    x8 = kmeans.Point([7, 14], "h")
    x9 = kmeans.Point([7, 10], "i")
    x10 = kmeans.Point([7, 6], "j")
    x11 = kmeans.Point([13, 13], "k")
    x12 = kmeans.Point([16, 10], "l")
    x13 = kmeans.Point([13, 6], "m")
    point_arr = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13]
    compute_proximity_matrix(point_arr)
    display_points(point_arr)


if __name__ == "__main__":
    main()
