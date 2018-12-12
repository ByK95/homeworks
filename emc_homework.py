#Written by Bayram Kaya in order to solve electromagnetic compabability problem
#source https://github.com/ByK95/homeworks/blob/master/emc_homework.py

from math import pi,sqrt,log10
from enum import Enum

#Constants
#speen of light in universe
c = 3*10**8 
mur = 1
sigmar = 1

class Material(Enum):
    """
    Material conductivity and magnetic permeability values for given materials
    First item is conductivity
    Second item is magnetic permeability
    """
    Silver = (1.05,1)
    Copper = (1,1)
    Aluminum = (0.61,1)
    Steel = (0.1,1000)

class emcsolver:
    def __init__(self,f,r,d,tp=False):
        self._f = f
        self._r = r
        self._d = d
        self._stype = tp #True if electric field

    def close_zone(self):
        """
        Function that decides whether given range is in close zone
        @param r => Distance between device and screen
        @param f => Frequency of circuit
        @return True if zone is in close range , False otherwise 
        """
        wavelenght = c / self._f
        zone = self._r < wavelenght / (2 * pi)
        return zone

    def absorbtion_loss(self):
        loss = 131.8 * self._d * sqrt(self._f*mur*sigmar)
        return loss

    def reflection_loss(self):
        if self.close_zone:
            if self._stype:
                return 321.74 + 10*log10(sigmar / (self._f ** 3 * self._r ** 2 * mur) )
            else:
                return 14.6 + 10*log10(self._f*self._r**2*sigmar*mur)
        else:
            return 168.2 + 10*log10( sigmar / (self._f * mur) )

    def many_reflection_loss(self):
        if self.close_zone:
            if self._stype:
                return 0
            elif self.absorbtion_loss() > 10:
                return 29.6+ 10*log10(self._d**2*self._f*sigmar*mur)
        else:
            return 0

    def Se(self):
        if self.close_zone:
            if self._stype:
                return self.absorbtion_loss() + self.reflection_loss() + self.many_reflection_loss()
            else:
                return self.absorbtion_loss() + self.reflection_loss()
        else:
            return self.absorbtion_loss() + self.reflection_loss()
        

    def _calculate(self):
        for f in self.__dir__():
            if not f.startswith('_'):
                print(f,self.__getattribute__(f)())

def let_user_pick(options):
    print("Please choose:")
    for idx, element in enumerate(options):
        print("{}) {}".format(idx+1,element))
    i = input("Enter number: ")
    try:
        if 0 < int(i) <= len(options):
            return options[int(i)-1]
    except:
        pass
    return None

def ask_for_input():
    f = input("Enter frequency (Hz): ")
    r = input("Enter radius (m): ")
    d = input("Enter distance (m): ")
    e = input("Enter source type e\m: ")
    e = 'e' == e.lower()
    return emcsolver(float(eval(f)),float(eval(r)),float(eval(d)),e)
    


if __name__ == "__main__":
    mat = let_user_pick(list(Material))
    sigmar = mat.value[0]
    mur = mat.value[1]
    vals = ask_for_input()
    vals._calculate()

"""
Test Case
d=2*10**-4
f=5*10**3
r=0.03
a = emcsolver(5*10**3,0.03,2*10**-4)
a.close_zone()
a.absorbtion_loss()
a.reflection_loss()
a.many_reflection_loss()
a._calculate()
"""
