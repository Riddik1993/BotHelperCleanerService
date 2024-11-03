import argparse
from argparse import Namespace


def get_arguments() -> Namespace:
    parser = argparse.ArgumentParser(description='arguments')
    parser.add_argument("lessons_ttl_days", type=int)
    return parser.parse_args()
