from abc import ABC, abstractmethod


class GenericBot(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def play_game(self):
        pass


class VampireSurvivorBot(GenericBot):

    def play_game(self):
        pass