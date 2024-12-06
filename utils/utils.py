import numpy as np

def obtainpositiveinteger(prompt):
    while True:
        try:
            value = int(input(prompt))
            
            #For a power of 2 the leading bit will always be 1 followed by zeros.
            #Subtracting one leads to 0111...111111
            #The & operation ands all the bits together, but because subtracting one returns 0111...111, none of the bits between the two numbers will be the same
            #Thus the & operation yields a false in the case that value is a power of two.
            if value > 0 and (value & (value - 1)) == 0:
                return value
            else:
                print(f"{value} is not a valid input. Please input a positive power of two.")
        except ValueError:
            print("Please input an integer value.")
            
class WriteIndexArray:
    def __init__(self, size):
        
        self.array = np.zeros(size, np.uint16)
        self.start = 0
        self.size = size
    
    def add(self, data):
        
        if self.start < self.size:

            #Write to first empty index            
            self.array[self.start] = data
            #Increment start counter
            self.start += 1
            
        else:
            
            raise ValueError("No Space Left in 1DWriteIndexArray")
        
    def remove(self, index):
        if index is None:
            
            raise ValueError("No Index given.")            
        
        #Check if the index is valid            
        if index >= self.start or index < 0:
            
            raise ValueError(f"Target index {index} is not within the 1DWriteIndexArray bounds.")           
            
        #If index is the last value containing data
        if index == self.start - 1:
            
            #There is no need to shift, just set that column to 0
            self.array[index] = 0
        
        else:
            
            # Shift all data left from the target index    
            self.array[index:self.start-1] = self.array[index+1:self.start]
        
            # Reset the last column to zero
            self.array[self.start-1] = 0
        
        
class TwoDimenionalWriteIndexArray:
    def __init__(self, rows, columns):
        
        self.array = np.zeros((rows, columns), np.uint16)
        self.start = 0
        self.totalcolumns = columns
    
    def add(self, data):
        if len(data) != self.array.shape[0]:
                
                raise ValueError(f"Data must have {self.array.shape[0]} rows, but got {len(data)}")
            
        if self.start < self.totalcolumns:
            
            #Write to first empty index
            self.array[:, self.start] = data
            #Increment start counter
            self.start += 1
                
        else:
            
            raise ValueError("No Space Left in 2DWriteIndexArray")
        
    def remove(self, index):
        if index is None:
            
            raise ValueError("No Index or given.")            
        
        #Check if the index is valid            
        if index >= self.start or index < 0:
            
            raise ValueError(f"Target index {index} is not within the 2DWriteIndexArray bounds.")           
            
        #If index is the last value containing data
        if index == self.start - 1:
            
            #There is no need to shift, just set that column to 0
            self.array[:, index] = 0
        
        else:
            
            # Shift all data left from the target index    
            self.array[:, index:self.start-1] = self.array[:, index+1:self.start]
        
            # Reset the last column to zero
            self.array[:, self.start-1] = 0
        
        #Decrement start counter
        self.start -= 1