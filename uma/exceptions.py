# Copyright (c) 2022 - Jojo#7791
# Licensed under MIT

class UMAException(Exception):
    """Base exception for the UMA api"""


class APIException(UMAException):
    """The exception for when something is wrong with the api itself"""

    def __init__(self):
        super().__init__("There is an error with the api. Please be patient")


class ChampionException(UMAException):
    """The exception for when getting a champion fails"""


class NodeException(UMAException):
    """The exception for when getting a node fails"""


class WarException(UMAException):
    """The exception for when getting a war fails"""
