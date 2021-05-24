#! /usr/bin/env python3
import argparse
import unittest

from typing import List


# Assume we can hard code the graph.
# Would probably store it in something else if it is expected to change often.
class TownGraph:
    graph = {
        "A": {
            "B": 5,
            "D": 5,
            "E": 7
        },
        "B": {
            "C": 4
        },
        "C": {
            "D": 8,
            "E": 2
        },
        "D": {
            "C": 8,
            "E": 6
        },
        "E": {
            "B": 3
        }
    }

    @classmethod
    def has_connection(cls, town_a: str, town_b: str) -> bool:
        """
        Checks if a connection exists from town_a to town_b
        """
        if town_b in cls.graph[town_a]:
            return True
        else:
            return False

    @classmethod
    def available_connections(cls, town: str) -> List[str]:
        """
        Returns all available connections from a town.
        """
        return list(cls.graph[town].keys())
    
    @classmethod
    def edge_distance(cls, town_a: str, town_b: str) -> int:
        """
        Calculates the distance between to towns.
        Is directional and can be different (or non-existent) when swapped.

        Will throw a ValueError if the route between town_a and town_b does not exist.
        """
        if not cls.has_connection(town_a, town_b):
            raise ValueError("NO SUCH ROUTE")
        return cls.graph[town_a][town_b]


def route_distance(route: List[str]) -> int:
    """
    Calculates the distance for a route between a number of towns.

    :param route: List of towns as strings that should be visited,
    :return: length of route, will be 0 for an empty list and just a single town.
    """

    distance = 0
    for i in range(len(route)-1):
        current_stop = route[i]
        next_stop = route[i + 1]
        distance += TownGraph.edge_distance(current_stop, next_stop)

    return distance


def get_routes(start_town: str, end_town: str, max_stops=1000, min_stops=0) -> List[List[str]]:
    """
    Finds all routes between start_town and end_town that satisfies the max_stops and min_stops limits.

    :return: List of found trips which in turn is a list of strings.
    """
    possible_routes: List[List[str]] = [[start_town]]
    found_routes = []

    while len(possible_routes) > 0:
        route = possible_routes.pop()
        route_length = len(route)

        if route_length <= max_stops:
            for town in TownGraph.available_connections(route[-1]):
                if town == end_town and route_length >= min_stops:
                    found_routes.append(route + [end_town])
                else:
                    possible_routes.append(route + [town])
    return found_routes


def handle_route_distance_command(args):
    try:
        print(route_distance(args.towns))
    except ValueError as e:
        print(e)


def handle_get_routes_command(args):
    try:
        routes = get_routes(args.start_town, args.end_town, args.max_stops, args.min_stops)
        print(f"Found {len(routes)} routes:")
        for route in sorted(routes, key=lambda x: len(x)):
            print("    " + "->".join(route))
    except ValueError as e:
        print(e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands', help='')

    parser_route_distance = subparsers.add_parser('route_distance', help='Get distance of a route')
    parser_route_distance.add_argument("towns", type=str, nargs="+", help="Towns to visit")
    parser_route_distance.set_defaults(func=handle_route_distance_command)

    parser_get_routes = subparsers.add_parser('get_routes', help='Get available routes between two towns.')
    parser_get_routes.add_argument("start_town", type=str, help="Town where the trip starts.")
    parser_get_routes.add_argument("end_town", type=str, help="Town where the trip ends.")
    parser_get_routes.add_argument("--max-stops", type=int, default=1000, help="Maximum stops to visit")
    parser_get_routes.add_argument("--min-stops", type=int, default=1, help="Minimum stops to visit")
    parser_get_routes.set_defaults(func=handle_get_routes_command)

    args = parser.parse_args()
    args.func(args)


class HWTests(unittest.TestCase):
    def test_case_1(self):
        self.assertEqual(route_distance(["A", "B", "C"]), 9)

    def test_case_2(self):
        self.assertEqual(route_distance(["A", "D"]), 5)

    def test_case_3(self):
        self.assertEqual(route_distance(["A", "D", "C"]), 13)

    def test_case_4(self):
        self.assertEqual(route_distance(["A", "E", "B", "C", "D"]), 22)

    def test_case_5(self):
        with self.assertRaises(ValueError, msg="NO SUCH ROUTE"):
            route_distance(["A", "E", "D"])

    def test_case_6(self):
        self.assertEqual(get_routes("C", "C", max_stops=3), [
            ['C', 'E', 'B', 'C'],
            ['C', 'D', 'C']
        ])

    def test_case_7(self):
        self.assertEqual(get_routes("A", "C", max_stops=4, min_stops=4), [
            ['A', 'D', 'E', 'B', 'C'],
            ['A', 'D', 'C', 'D', 'C'],
            ['A', 'B', 'C', 'D', 'C']
        ])
