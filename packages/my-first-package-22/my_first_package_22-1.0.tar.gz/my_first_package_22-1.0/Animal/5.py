
from abc import abstractclassmethod, ABC

class Animal(ABC):
    
    def __init__(self, name, age, color,  wild=True):

        self.name = name
        self.age = age
        self.color = color
        self.wild = wild


    @property
    def age(self):
        return self.__age


    @age.setter
    def age(self, age):
        if age < 0:
            raise ValueError("age can not be less negative zero.")
        self.__age = age


    @abstractclassmethod
    def move(self, mile):
        if self.energy >= mile:
            self.energy = mile
            print(f"{self.name} moved {mile} miles ")

        else:
            print(f"{self.name} moved {self.energy} miles ")
            self.energy = 0



class Lion(Animal):
    
    def __init__(self, name, age, color, energy, energyPerTime=2, energyPerVolume=2 ,wild=True):
        
        super().__init__(name, age, color, wild)
        
        self.energy = energy
        self.energyPerTime = energyPerTime
        self.energyPerVolume = energyPerVolume

    def move(self, mile):
        if self.energy >= mile:
            self.energy = mile
            print(f"{self.name} moved {mile} miles ")

        else:
            print(f"{self.name} moved {self.energy} miles ")
            self.energy = 0

    def eat(self, volume):
        addedEnergy = self.energyPerVolume * volume
        self.energy += addedEnergy
        print(f"{self.name} moved {addedEnergy} energy ")

    def rest(self, time):
        addedEnergy = self.energyPerTime * time
        self.energy += addedEnergy
        print(f"{self.name} moved {addedEnergy} energy ")

    def amperes(self):
        print(f"energy: {self.energy}")

    def __str__(self):
        # print(str(self.energy and self.energy))
        # print(str(self.name and self.energy))
        return self.name

    def __add__(self, other):
        
        newLion = Lion(name=self.name , 
                           age=0,
                           color=other.color,
                           energy=0,
                           energyPerTime=other.energyPerTime)

        return newLion



lion1 = Lion(name="max", age=3, color="red", energy=2, energyPerTime=2, energyPerVolume=2, wild=False)
lion2 = Lion(name="leo", age=3, color="blue", energy=2, energyPerTime=2, energyPerVolume=2, wild=False)

baby = lion1 + lion2

print(baby.age)