# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 10:13:53 2021

@author: matth

Création de machines de Moore pour la STI
"""

class Automate:
    def __init__(self, S, E, q0, delta, F):
        self.__sigma         = S
        self.__states        = E
        self.__initialStates = q0
        self.__transitions   = delta
        self.__finalStates   = F
    
    
    def addState(self,q):
        self.__etats.add(q)

    
    def removeState(self,q):
        try:
            self.__etats.remove(q)
            del self.__transitions[q] # ok car non état implique non transition cf constructeur ajouterTransition
        except KeyError:
            pass
    
    
    def addTransition(self,q,a,r):
        if (q in self.__states) and (r in self.__states):
            self.__transitions[q][a] = r
        else:
            raise ValueError('L\'un des états départ ou arrivée n\'existe pas.')
    
    def deleteTransition(self,q,a):
        try:
            del self.__transitions[q][a]
        except KeyError:
            pass
    
    
    
    
    
if __name__ == '__main__':
    a = Automate({'a','b'},{1,0},0,{0:{'b':1}},{1})
    