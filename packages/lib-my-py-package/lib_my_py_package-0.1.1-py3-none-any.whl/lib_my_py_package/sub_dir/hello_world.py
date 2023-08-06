#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse


class HelloWorld:
    """Class that performs functions for login"""

    def __init__(self):
        """ """

    def say_hello(self):
        """says hello to the world"""

        print("Hello World!")
        self._echo_args()

    def _echo_args(self):
        """echos args to terminal"""

        parser = argparse.ArgumentParser()

        parser.add_argument('x', type=str)

        args = parser.parse_args()

        output = f'echoing: {args.x}'

        print(output)


# if __name__ == "__main__":
#     HelloWorld().say_hello()
