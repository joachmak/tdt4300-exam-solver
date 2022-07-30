import sys

import const
import distances
from tabulate import tabulate
import utils


class Point:
    def __init__(self, coordinates, name=None, cluster=None):
        self.coordinates = coordinates
        self.name = name if name is not None else str(self.coordinates)
        self.cluster = cluster
        if cluster is not None:
            cluster.add_point(self)

    def __str__(self):
        return str(self.coordinates)


class Cluster:
    def __init__(self, name: str, proximity_function: str):
        self.points = []
        self.centroid = None
        self.old_centroid = None
        self.proximity_function = proximity_function
        self.name = name

    def add_point(self, point: Point):
        if point not in self.points:
            self.points.append(point)
            point.cluster = self

    def add_points(self, points: list):
        for point in points:
            self.add_point(point)
        print(f"Points in {str(self)}: {utils.str_obj_list([point.name for point in self.points])}")

    def remove_point(self, point: Point):
        self.points.remove(point)
        point.cluster = None

    def clear_points(self):
        self.points.clear()

    def calculate_centroid(self):
        self.old_centroid = self.centroid
        if self.proximity_function in const.MEAN_DISTANCES:
            self.centroid = utils.find_avg_point(self.points, prepend_str=f"{self}: ")
        elif self.proximity_function in const.MEDIAN_DISTANCES:
            self.centroid = utils.find_median_point(self.points, prepend_str=f"{self}: ")
        else:
            print(f"proximity function {self.proximity_function} not found in mean or median table in constants")

    def has_centroid_changed(self, print_txt=True):
        if print_txt:
            print(f"""The centroid of {self} has {"not " if self.centroid == self.old_centroid else ""}changed.""")
        return self.centroid != self.old_centroid

    def print_points(self):
        point_list = [point.name for point in self.points]
        point_list.sort()
        print(f"{self}: {utils.str_obj_list(point_list)}")

    def __str__(self):
        return self.name


def have_centroids_changed(centroid_list: list, print_txt=True):
    for centroid in centroid_list:
        if centroid.has_centroid_changed(print_txt):
            return True
    return False


def reassign_points(point_arr: list, cluster_list: list, proximity_function: str):
    print(f"We reassign points to their nearest cluster. \nFirst, we find each point's proximity (distance, d)"
          f" to each cluster's centroid. We are using {proximity_function} to measure distance. \nThen we assign each "
          f"point to the cluster with the nearest centroid.\n")
    cluster_reassignment_log = ""
    headers = ["Point"]
    for cluster in cluster_list:
        cluster.clear_points()
        headers.append(f"d_{cluster} {tuple(cluster.centroid)}")
    headers.append("Nearest centroid")
    rows = []
    for point in point_arr:
        row = [point.name]
        distances = {}
        for cluster in cluster_list:
            d = utils.calculate_distance_with_proximity_str(cluster.centroid, point.coordinates, proximity_function)
            distances[cluster] = d
            row.append(d)
        min_distance = sys.maxsize
        closest_cluster = None
        for cluster in distances:
            d = distances[cluster]
            if d < min_distance:
                closest_cluster = cluster
                min_distance = d
        if closest_cluster is None:
            print("ERROR: closest cluster is None during point cluster reassignment!")
            return
        row.append(closest_cluster.name.lower() + (" (reassigned this iteration)" if point.cluster != closest_cluster else ""))
        closest_cluster.add_point(point)
        rows.append(row)
    print(tabulate(rows, headers=headers))
    print(cluster_reassignment_log)
    pass


def main():
    proximity_function = const.EUCLIDEAN
    # define clusters
    c1 = Cluster("C1", proximity_function)
    c2 = Cluster("C2", proximity_function)
    c3 = Cluster("C3", proximity_function)
    cluster_arr = [c1, c2, c3]
    # define points
    x1 = Point([2])
    x2 = Point([4])
    x3 = Point([10])
    x4 = Point([12])
    x5 = Point([3])
    x6 = Point([20])
    x7 = Point([30])
    x8 = Point([11])
    x9 = Point([25])
    point_arr = [x1, x2, x3, x4, x5, x6, x7, x8, x9]
    # Add points to initial clusters
    # c1.add_points([x1, x2, x4])
    # c2.add_points([x3, x5])
    CALCULATE_INITIAL_CENTROIDS = False  # if false, set centroids manually below
    CALCULATE_SSE_FOR_EACH_ITERATION = False  # Lower SSE indicates better clustering
    # Define centroids
    c1.centroid = [2]
    c2.centroid = [4]
    c3.centroid = [6]

    # =======================

    if CALCULATE_INITIAL_CENTROIDS:
        print("\nWe calculate an initial centroid for all clusters.")
        for cluster in cluster_arr:
            cluster.calculate_centroid()
    print("Centroids for each cluster: ")
    for cluster in cluster_arr:
        print(f"{cluster}: {cluster.centroid}")
    i = 0
    while have_centroids_changed(cluster_arr, print_txt=False):
        i += 1
        print(f"\nITERATION {i}")
        reassign_points(point_arr, cluster_arr, proximity_function)
        print("The clusters now contain the following points:")
        for cluster in cluster_arr:
            cluster.print_points()
        print("\nWe calculate new centroids for each cluster:")
        for cluster in cluster_arr:
            cluster.calculate_centroid()
        if CALCULATE_SSE_FOR_EACH_ITERATION:
            print("\nWe calculate the SSE for the new clustering.")
            if proximity_function == const.SQUARED_EUCLIDEAN:
                print("We have already calculated squared euclidean distances from each point to its centroid."
                      " For each point, we can take the distance to the point's nearest centroid and add it to the SSE.")
            else:
                print("We must find the squared euclidean distance from each point to its nearest cluster centroid.")
                headers = ["Point", "Cluster", "Squared Euclidean Distance"]
                rows = []
                for point in point_arr:
                    d = distances.squared_euclidean_distance(point.coordinates, point.cluster.centroid)
                    rows.append([point.name + " " + str(point.coordinates), point.cluster.name + " " + str(point.cluster.centroid), d])
                print(tabulate(rows, headers=headers))
            SSE = 0
            for cluster in cluster_arr:
                centroid = cluster.centroid
                for point in cluster.points:
                    SSE += distances.squared_euclidean_distance(point.coordinates, centroid)
            print(f"SSE for this clustering = {SSE}")

    print("\nThe centroids haven't changed since the last iteration, so we terminate.")
    for cluster in cluster_arr:
        cluster.print_points()


if __name__ == "__main__":
    main()
