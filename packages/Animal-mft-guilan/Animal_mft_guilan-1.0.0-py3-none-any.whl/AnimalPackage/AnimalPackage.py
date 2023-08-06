from abc import ABC, abstractmethod
from random import choice

class Animal(ABC):
    def __init__(self, name: str, age: int, color: str, isWild: bool):
        self.name = name
        self.age = age
        self.color = color
        self.isWild = isWild
    

    @abstractmethod
    def eat(self, volume: int):
        pass


    @abstractmethod
    def move(self, distance: int):
        pass


class Lion(Animal):
    def eat(self, volume: int):
        self.energy = volume
        
        print(f"{self.name} earned {self.energy} energies...")
    

    def move(self, distance: int):
        if self.energy >= distance:
            self.energy -= distance

            print(f"{self.name} moved {distance} km, he`s got {self.energy} energy.")
        else:
            print(f"{self.name} moved {self.energy} km, now he is so hungry.")

            self.energy = 0
    

    def __add__(self, other: object):
        newAnimal = Lion(self.name, 0, other.color, choice([True, False]))

        return newAnimal
    

    def __str__(self):
        return f"{self.name} - {self.color} - {self.age} - {self.isWild}"