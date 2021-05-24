#! /usr/bin/env python3
import argparse
import unittest


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
    def available_connections(cls, town: str) -> list[str]:
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


def route_distance(route: list) -> int:
    """
    Calculates the distance for a route between a number of towns.

    :param route: Towns that should be visited,
    :return: length of route, will be 0 for an empty list and just a single town.
    """

    distance = 0
    for i in range(len(route)-1):
        current_stop = route[i]
        next_stop = route[i + 1]
        distance += TownGraph.edge_distance(current_stop, next_stop)

    return distance


def handle_route_command(args):
    try:
        print(route_distance(args.towns))
    except ValueError as e:
        print(e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands', help='')

    parser_route_distance = subparsers.add_parser('route_distance', help='Get distance of a route')
    parser_route_distance.add_argument("towns", type=str, nargs="+", help="Towns to visit")
    parser_route_distance.set_defaults(func=handle_route_command)

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