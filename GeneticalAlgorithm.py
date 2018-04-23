# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 19:39:56 2018

@author: rober
"""

from BrainfuckInterpreter import BrainFuckSession as bfs
from numpy import random 
import numpy as np

#symbols
symbols = {0: '>',
           1: '<',
           2: '+',
           3: '-',
           4: '.',
           5: '[',
           6: ']',
           7: ' '}

#maximum code length
code_len = 10

#maximum steps per 
max_steps = 150

#x and y are simply strings
#assuming the same length
def cross_two(x, y):
    selector = random.randint(0, 2, size=len(x))
    out = [x_ if s == 0 else y_ for x_, y_, s in zip(x, y, selector)]
    return "".join(out)

#assuming x is string
def mutate_one(x, chance=0.1):
    selector = [random.ranf() < chance for c in x]
    out = [c if s == False else symbols[random.randint(0, len(symbols.keys()))] for c, s in zip(x, selector)]
    return "".join(out)

def rate_one(x, target_ascii="Hello world!"):
    session = bfs(x)
    correct = 1 if session.get_code_validity() else 0
    sess_output = ""
    if correct:
        session.run(max_steps=max_steps)
        sess_output = session.output
        
    correct_letters_count = 0
    for c in sess_output:
        if c in target_ascii:
            correct_letters_count += 1
            
    len_diff = abs(len(target_ascii)-len(sess_output))
    diff = 0.
    
    for i in range(0, min(len(x), len(sess_output))):
        diff += abs(ord(x[i])-ord(sess_output[i]))
        
    return correct*10. + correct_letters_count*5. + 100*(1./(1.+len_diff)) + 100.*(1./(1.+diff))

def generate_initial(number):
    generation = []
    
    for i in range(number):
        generation.append("".join([symbols[random.randint(0, len(symbols.keys()))] for _ in range(code_len)]))

    return generation

def do_generation(generation, percent_to_procreate=0.25):
    rates = [rate_one(g) for g in generation]
    pack = [(r, g) for r, g in zip(rates, generation)]
    pack = sorted(pack, key=lambda x: -x[0])
    
    to_procreate = generation[0:int(len(pack)*percent_to_procreate)]
    
    new_generation = []
    for i in range(len(generation)):
        child = cross_two(random.choice(to_procreate, replace=False), random.choice(to_procreate, replace=False))
        child = mutate_one(child)
        new_generation.append(child)
        
    return new_generation, max(rates), min(rates), np.mean(rates)


max_iter = 10000

initial_gen = generate_initial(100)

for i in range(max_iter):
    initial_gen, mx, mi, mn = do_generation(initial_gen)
    if i % 10 == 0:
        print(i, mx, mi, mn)
    

