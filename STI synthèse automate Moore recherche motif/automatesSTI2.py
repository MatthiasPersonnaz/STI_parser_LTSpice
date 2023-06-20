# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 12:34:35 2021

@author: matth
"""



from automata.fa.dfa import DFA
from automata.fa.nfa import NFA

from visual_automata.fa.dfa import VisualDFA
from visual_automata.fa.nfa import VisualNFA


import numpy as np
import graphviz

import itertools

nfa = VisualNFA(
    states={"q0", "q1", "q2", "q3", "q4"},
    input_symbols={"0", "1"},
    transitions={
        "q0": {"0": {"q3"}, "1": {"q1", "q2"}},
        "q1": {"0": {"q3"}, "1": {"q1"}},
        "q2": {"0": {"q3"}, "1": {"q2", "q3"}},
        "q3": {"0": {"q4"}, "1": {"q1"}},
        "q4": {"0": {"q4"}, "1": {"q1"}},
    },
    initial_state="q0",
    final_states={"q2", "q4"},
)

dfa = VisualDFA(
    states={"q0", "q1", "q2", "q3", "q4"},
    input_symbols={"0", "1"},
    transitions={
        "q0": {"0": "q3", "1": "q1"},
        "q1": {"0": "q3", "1": "q2"},
        "q2": {"0": "q3", "1": "q2"},
        "q3": {"0": "q4", "1": "q1"},
        "q4": {"0": "q4", "1": "q1"},
    },
    initial_state="q0",
    final_states={"q2", "q4"},
)







alphabet = {"0","1"}
motBinaire = "101100101"
motif = list(motBinaire)
etats = set([f"q{i}" for i in range(len(motif)+1)])
ef = f"q{len(motif)}"


trans = [{motif[i]:set([f"q{i+1}"])} for i in range(len(motif))]
delta = {f"q{i}":x for i,x in enumerate(trans)} # dict(enumerate(trans)) donnerait des entiers

# on ajoute les deux transitions absorbantes dans le dernier état:
delta[ef] = {e: {ef} for e in alphabet} # pour détecter une séquence    CONTENANT     le motif
delta[ef] = {}                          # pour détecter une séquence SE TERMINANT par le motif


for a in alphabet:
    if a == motBinaire[0]:
        delta["q0"][a].add("q0")
    else:
        delta["q0"][a] = {"q0"}


nfa = NFA(states=etats, input_symbols=alphabet, transitions=delta, initial_state="q0", final_states={ef})
nfav = VisualNFA(nfa)
dfa = DFA.from_nfa(nfa)
dfav = VisualDFA(dfa)
minimal_dfa = dfa.minify(retain_names=False)
min_dfav = VisualDFA(minimal_dfa)
    


# min_dfav.show_diagram(view=True) # pour l'afficher en pdf
# min_dfav.show_diagram            # pour afficher le tableau des transitions
# min_dfav.show_diagram()          # pour afficher le graphe



def integer2binaryArray(i,nBits):
    return np.chararray.astype(np.array(list( format(i, f"0{nBits}b") )),int)


nStates = len(min_dfav.states)
lAlpha  = len(min_dfav.input_symbols)

bStates = np.ceil(np.log2(nStates)).astype(int)
bAlpha = np.ceil(np.log2(lAlpha)).astype(int)

transitionTable = np.zeros((lAlpha*nStates,2*(bStates+2)),dtype=int)


for e in sorted(min_dfav.states):
    en = int(e)
    for c in sorted(min_dfav.input_symbols):
        cn = int(c)
        
        # numéro état de départ
        transitionTable[en*lAlpha+cn][0]                            = e
        # codage binaire état de départ
        transitionTable[en*lAlpha+cn][1:bStates+1]                  = integer2binaryArray(en,bStates)
        # numéro du caractère lu
        transitionTable[en*lAlpha+cn][bStates+1]                    = cn
        
        # numéro état d'arrivée
        transitionTable[en*lAlpha+cn][bStates+2]                    = int(min_dfav.transitions[e][c])
        
        # codage binaire état arrivée
        transitionTable[en*lAlpha+cn][bStates+3:bStates+3+bStates]  = integer2binaryArray(int(min_dfav.transitions[e][c]),bStates)
        
        # sortie (binaire): état acceptant ou non
        transitionTable[en*lAlpha+cn][bStates+3+bStates]            = int(min_dfav.transitions[e][c] in min_dfav.final_states)
        
# Réduction par l'algorithme de Quine-McCluskey pour chaque bit de codage de l'état:
from sympy.logic import SOPform
from sympy import symbols

import string
alphabet_string = string.ascii_lowercase
alphabet_list = list(alphabet_string)

def solveForBoolExpr(q):
    symb = symbols(' '.join(alphabet_list[:bStates])+' char')

    
    # on peut choisir de faire la formule booléenne minimale pour chaque bit de range(bStates+3:bStates+3+bStates)
    dontcares = [list(np.append(integer2binaryArray(m,bStates),s)) for (m,s) in \
                 itertools.product(range(nStates,2**bStates),range(lAlpha))]
    minterms = [list(r[1:bStates+2]) for r in transitionTable if r[q]]
    return SOPform(list(symb), minterms, dontcares)
    
for q in range(bStates+3,bStates+3+bStates):
    print(f"SOP du bit de poids {2*bStates+2-q}  {solveForBoolExpr(q)}\n")
print(f"SOP d'acceptation  {solveForBoolExpr(2*bStates+3)}")