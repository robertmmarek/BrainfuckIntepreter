# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 14:18:21 2018

@author: ROBEMARE
"""

class BrainFuckSession:
    correct_symbols = ['>', '<', '+', '-', '.', ',', '[', ']']
    
    def check_code_validity(code):
        loop_counter = 0
        for c in code:
            if c == '[':
                loop_counter += 1
            elif c == ']':
                loop_counter -= 1
                
            if loop_counter < 0:
                return False
            
        if loop_counter != 0:
            return False
        else:
            return True
    
    #code as string
    def __init__(self, code, input_on=False, output_format='ascii'):
        self.memory = {0: 0}
        self.code_pointer = 0
        self.memory_pointer = 0
        self.input_on = input_on
        self.output_format = output_format
        self.code = [x for x in ("".join(code.split())).split() if x in self.correct_symbols]
        self.output = ""
        self.code_finished = False
        
        if not self.check_code_validity(self.code):
            self.code = []
            
    def set_data(cell_pointer, value):
        value = value%256
        if value < 0:
            value = 256 - abs(value)
            
        self.memory[cell_pointer] = value
        
    def go_to_code_position(position):
        self.code_pointer = min(len(self.code)-1, max(0, position))
        if position > len(self.code)-1:
            self.code_finished = True
            
    def increment_data_pointer(self):
        self.memory_pointer += 1
        if not self.memory_pointer in self.memory.keys():
            self.memory[self.memory_pointer] = 0
    
    def decrement_data_pointer(self):
        self.memory_pointer -= 1
        self.memory_pointer = max(0, self.memory_pointer)
        if not self.memory_pointer in self.memory.keys():
            self.memory[self.memory_pointer] =  0
    
    def increment_data(self):
        self.set_data(self.memory_pointer, self.memory[self.memory_pointer]+1)
    
    def decrement_data(self):
        self.set_data(self.memory_pointer, self.memory[self.memory_pointer]-1)
    
    def output_data(self, output_format='ascii'):
        if output_format == 'ascii':
            print(self.memory[self.memory_pointer], end='')
            self.output += self.memory[self.memory_pointer]
        elif output_format == 'ascii_no_console':
            self.output += self.memory[self.memory_pointer]
    
    def input_data(self, input_on=False):
        if input_on:
            raw_data = raw_input("")
            try:
                raw_data = int(raw_data)
            except ValueError:
                pass
    
    def jump_formard(self):
        if self.memory[self.memory_pointer] == 0:
        else:
            self.code_pointer += 1
            if self.code_pointer >= len(self.code):
                self.code_pointer = len(self.code)-1
                self.code_finished = True
        
    
    def jump_back(self):
        pass
            
    def step(self, max_steps=-1):
        pass
        