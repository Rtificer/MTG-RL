import numpy as np

def obtainpositiveinteger(prompt):
    while True:
        try:
            value = int(input(prompt))
            
            if value > 0:
                return value
            else:
                print(f"{value} is not a valid input. Please input a positive value.")
        except ValueError:
            print("Please input an integer value.")
            
class WriteIndexArray:
    def __init__(self, size):
        
        self.array = np.zeros(size, np.uint16)
        self.start = 0
        self.size = size
    
    def add(self, data):
        
        if self.start <= self.size-1:

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
            self.array[index:self.start] = np.roll(self.array[index:self.start], shift=-1, axis=1)
        
            # Reset the last column to zero
            self.array[self.start-1] = 0
            
        #Decrement start counter
        self.start -= 1
        
    def query(self, index):
        
        if index < 0 or index >= self.start:
            
            raise ValueError(f"Index {index} is not within 1DWriteIndexArray bounds.")
        
        return self.array[index]
        
        
class TwoDimenionalWriteIndexArray:
    def __init__(self, rows, columns):
        
        self.array = np.zeros((rows, columns), np.uint16)
        self.start = 0
        self.maxindex = columns-1
    
    def add(self, data):
        if len(data) != self.array.shape[0]:
                
                raise ValueError(f"Data must have {self.array.shape[0]} rows, but got {len(data)}")
            
        if self.start <= self.maxindex:
            
            #Write to first empty index
            self.array[:, self.start] = data
            #Increment start counter
            self.start += 1
                
        else:
            
            raise ValueError("No Space Left in 2DWriteIndexArray")
        
    def remove(self, index):
        if index is None:
            
            raise ValueError("No Index given.")            
        
        #Check if the index is valid            
        if index >= self.start or index < 0:
            
            raise ValueError(f"Target index {index} is not within the 2DWriteIndexArray bounds.")           
            
        #If index is the last value containing data
        if index == self.start - 1:
            
            #There is no need to shift, just set that column to 0
            self.array[:, index] = 0
        
        else:
            
            # Shift all data left from the target index    
            self.array[:, index:self.start] = np.roll(self.array[:, index:self.start], shift=-1, axis=1)
        
            # Reset the last column to zero
            self.array[:, self.start-1] = 0
        
        #Decrement start counter
        self.start -= 1
        
    def query(self, index):
        
        if index < 0 or index >= self.start:
            
            raise ValueError(f"Index {index} is not within 2DWriteIndexArray bounds.")
        
        return self.array[:, index]
        
class TwoDimensionalStartIndexArray:
    def __init__(self, rows, columns):
        
        self.array = np.zeros((rows, columns), np.uint16)
        self.start = 0
        self.maxindex = columns-1
    
    def add(self, data, index):
        if index is None:
            
            raise ValueError("No Index given.")
        
        #Check if the index is valid            
        if index >= self.maxindex or index < 0:
            
            raise ValueError(f"Target index {index} is not within the 2DStartIndexArray bounds.")
        
        if index > self.start:
            
            raise ValueError(f"Target index {index} is within unoccuped space.")
              
        if len(data) != self.array.shape[0]:
                
            raise ValueError(f"Data must have {self.array.shape[0]} rows, but got {len(data)}")
            
        if self.start > self.maxindex:

            raise ValueError("No Space Left in 2DStartIndexArray")
               
        if index < self.start:
            
            #Roll data from index to 1 
            self.array[:, index:self.start+1] = np.roll(self.array[:, index:self.start+1], shift=1, axis=1)
            
            #The only case this is false is if we are trying to write to the bottom of the deck, in which case no shifting is nessasary
            
        self.array[:, index] = data
        self.start += 1
        
    def remove(self, index):
        if index is None:
            
            raise ValueError("No Index given.")            
        
        #Check if the index is valid            
        if index >= self.start or index < 0:
            
            raise ValueError(f"Target index {index} is not within the 2DStartIndexArray bounds.")           
            
        #If index is the last value containing data
        if index == self.start - 1:
            
            #There is no need to shift, just set that column to 0
            self.array[:, index] = 0
        
        else:
            
            # Shift all data left from the target index    
            self.array[:, index:self.start] = np.roll(self.array[:, index:self.start], shift=-1, axis=1)
        
            # Reset the last column to zero
            self.array[:, self.start-1] = 0
        
        #Decrement start counter
        self.start -= 1

    def query(self, index):
        
        if index < 0 or index >= self.start:
            
            raise ValueError(f"Index {index} is not within 2DStartIndexArray bounds.")
        
        return self.array[:, index]