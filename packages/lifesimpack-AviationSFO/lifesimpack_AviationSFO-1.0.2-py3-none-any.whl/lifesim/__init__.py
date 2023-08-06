# Life simulator module for python by Steven Weinstein on 2-9-2022 (Py ver >= 3.6.0)
# Version v1.0.2
class AyoUrFatBro(Exception):
    pass
class Person:
    def __init__ (self, name, height, weight, status = "alive", age = 0):
        self.fullname = name
        self.firstname = name.split(" ")[0]
        self.lastname = name.split(" ")[1]
        self.age = age
        self.height = height
        self.weight = weight
        self.stat = status
    def ageup (self, age):
        self.age = int(age)+1
    def grow (self, height = -20, interval = 1):
        if (height == -20):
            height=self.height
        self.height = int(height)+int(interval)
    def enfatten (self, weight, interval = 1):
        self.weight = int(weight)+int(interval)
        if (self.weight > 69420):
            self.kill()
            raise AyoUrFatBro("ayo ur fat bro")
    def kill (self, newstat = "deceased"):
        self.stat = newstat
        print(f"Oops, {self.fullname} is now dead. Have fun!")
