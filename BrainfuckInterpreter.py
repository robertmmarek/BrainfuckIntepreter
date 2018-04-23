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
    def __init__(self, code, input_on=False, output_format='ascii_no_console'):
        self.memory = {0: 0}
        self.code_pointer = 0
        self.memory_pointer = 0
        self.input_on = input_on
        self.output_format = output_format
        self.code = [x for x in code if x in self.correct_symbols]
        self.output = ""
        self.code_finished = False
        self.step_counter = 0
        self.code_validity = BrainFuckSession.check_code_validity(self.code)
        
        if not self.code_validity:
            self.code = []
            
    def set_data(self, cell_pointer, value):
        value = value%256
        if value < 0:
            value = 256 - abs(value)
            
        self.memory[cell_pointer] = value
        
    def go_to_code_position(self, position):
        self.code_pointer = min(len(self.code)-1, max(0, position))
        if position > len(self.code)-1:
            self.code_finished = True
            
    def increment_code_position(self):
        self.go_to_code_position(self.code_pointer+1)
        
    def decrement_code_position(self):
        self.go_to_code_position(self.code_pointer-1)
            
    def increment_data_pointer(self):
        self.memory_pointer += 1
        if not self.memory_pointer in self.memory.keys():
            self.memory[self.memory_pointer] = 0
    
    def decrement_data_pointer(self):
        self.memory_pointer -= 1
        self.memory_pointer = max(0, self.memory_pointer)
        if not self.memory_pointer in self.memory.keys():
            self.memory[self.memory_pointer] =  0
            
    def get_code_validity(self):
        return self.code_validity
            
    def get_current_code_symbol(self):
        return self.code[self.code_pointer]
    
    def get_current_data(self):
        return self.memory[self.memory_pointer]
    
    def increment_data(self):
        self.set_data(self.memory_pointer, self.memory[self.memory_pointer]+1)
    
    def decrement_data(self):
        self.set_data(self.memory_pointer, self.memory[self.memory_pointer]-1)
    
    def output_data(self, output_format='ascii_no_console'):
        if output_format == 'ascii':
            print(chr(self.memory[self.memory_pointer]), end='')
            self.output += chr(self.memory[self.memory_pointer])
        elif output_format == 'ascii_no_console':
            self.output += chr(self.memory[self.memory_pointer])
        elif output_format == 'raw_numbers':
            print(str(self.memory[self.memory_pointer]), end='')
            self.output += str(self.memory[self.memory_pointer])
    
    def input_data(self, input_on=False):
        if input_on:
            raw_data = raw_input("")
            try:
                raw_data = int(raw_data)
            except ValueError:
                pass
    
    def jump_formard(self):
        if self.get_current_data() == 0:
            jump_counter = 1
            for x in range(self.memory_pointer, len(self.code)):
                self.increment_code_position()
                if self.get_current_code_symbol() == ']':
                    jump_counter -= 1
                elif self.get_current_code_symbol() == '[':
                    jump_counter += 1
                    
                if jump_counter == 0:
                    break
            
        else:
            pass
        
    
    def jump_back(self):
        jump_counter = 1
        while jump_counter > 0:
            self.decrement_code_position()
            current_symbol = self.get_current_code_symbol()
            if current_symbol == ']':
                jump_counter += 1
            elif current_symbol == '[':
                jump_counter -= 1
            
    def step(self, max_steps=None):
        action_dictionary = {'>': lambda: self.increment_data_pointer(),
                             '<': lambda: self.decrement_data_pointer(),
                             '+': lambda: self.increment_data(),
                             '-': lambda: self.decrement_data(),
                             '.': lambda: self.output_data(self.output_format),
                             ',': lambda: self.input_data(self.input_on),
                             '[': lambda: self.jump_formard(),
                             ']': lambda: self.jump_back()}
        
        if max_steps != None:
            self.code_finished = (self.step_counter >= max_steps)
        
        if self.code_finished:
            return self.output
        else:
            curr_step = self.get_current_code_symbol()
            action = action_dictionary[curr_step]
            action()
            
            if curr_step not in [']']:
                self.increment_code_position()
            
            self.step_counter += 1
            
    def run(self, max_steps=None):
        while not self.code_finished:
            self.step(max_steps)
        
        
        

        