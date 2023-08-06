from abc import ABC, abstractmethod 
from enum import Enum
from random import choice
from time import sleep

class AnimalType(Enum):
    WILD = 0,
    DOMESTIC = 1

class Gender(Enum):
    MALE = 0,
    FEMALE = 1

class Animal(ABC):

    def __init__(self, name: str, gender: Gender, age: int, color, animaltype: AnimalType):
        self.name = name
        self.gender = gender
        self.age = age
        self.color = color
        self.animaltype = animaltype
        self.energy = 0

    @abstractmethod
    def eating(self):
        pass

    @abstractmethod
    def moving(self, length):
        pass

    def __add__(self, other):
        if (self.gender != other.gender) and (type(self) == type(other)) : 
            '''shared mro point can be a better implemention'''
            if self == Gender.MALE:
                father = self
                mother = other
            else:
                father = other
                mother = self
            return type(self)(name=father.name,
                              gender=choice([Gender.FEMALE,
                                             Gender.MALE]),
                              color=mother.color,
                              age=0,
                              animaltype=choice([AnimalType.WILD,
                                                 AnimalType.DOMESTIC]))
        else:
            print("Can't mate")

class Lion(Animal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def eating(self, amount):
        print("Lion is eating",end="")
        for i in range(amount):
            self.energy += amount
            print(".",end="")
            sleep(0.5)
        print("\nLion ate")

    def moving(self, length):
        if (length > self.energy):
            print("Lion cant move, not enough energy, going to eat")
            self.eating(length)
        else:
            self.energy -= length
            print("Lion is moving",end="")
            for i in range(length):
                print(".",end="")
                sleep(0.5)
            print("\nLion moved")
            



