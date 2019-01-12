'''
Author: Monique Chan
Last Modified: May 23, 2018

A class representation of a Matrix with attributes of its entries and its size
'''
class Matrix():
    def __init__(self, size):
        '''(Matrix, int)--> NoneType
        Creates a sizexsize matrix 
        '''
        # create a list representation of a sizexsize matrix
        self._entries = []
        for i in range(size):
            self._entries.append([None]*size)
        self._size = size

    def __str__(self):
        return str(self._entries)
        
    def is_valid(self):
        '''(Matrix) -> bool
        checks if the matrix has None in as its entry. Returns true if no
        NoneTypes are found
        '''
        # check each row
        i = 0
        valid = True
        # loop through whole matrix of until a None is found
        while(valid == True and i < self._size):
            valid = not None in self._entries[i]
            i += 1
            
        return valid
    
    def add_entry(self, row, column, entry):
        '''(Matrix, int, int, float) -> NoneType
        adds entry at given row and column
        '''
        self._entries[row][column] = entry
        
    def determinant(self):
        '''(Matrix) -> float
        Calculates the determinant of the matrix
        '''
        # if the size of the matrix is 2
        if(self._size == 2):
            # calculate determinant of 2x2 matrix
            det = ((self._entries[0][0]*self._entries[1][1]) -
                   (self._entries[0][1]*self._entries[1][0]))

        # recursive case    
        else:
            row = 0
            result = []
            det = 0
            for column in range(self._size):
                result.append(self._entries[row][column]*(self.minor(row, column).determinant()))
            for column in range(self._size):
                det = det + ((-1)**(column))*result.pop(0)

        return det
    
    def minor(self, row, column):
        '''(Matrix, row, column) -> Matrix
        returns the minor of the matrix at the given entry
        '''
        # create a new matrix for the minor
        minor = Matrix(self._size - 1)
        # keeps track of where next entry is to be added
        curr = [0,0]
        # loop through the rows
        for i in range(self._size):
            # loop through the columns
            for j in range(self._size):
                # add entry if i is not equal to row and j is not
                # equal to column
                if(i is not row and j is not column):
                    minor.add_entry(curr[0],curr[1],self._entries[i][j])
                    # increment curr
                    self.increment(curr)
        return minor
                    
    def increment(self, curr):
        '''(Matrix, list of int) -> tuple of int
        Increments curr so that the column is incremented by one. If column
        is size-2 then column becomes 0 and row is incremented by one
        '''
        # if column is equal to size-2
        if(curr[1] == self._size - 2):
            # column = 0 and row increments by one
            curr[1] = 0
            curr[0] += 1
        
        else:
            curr[1] += 1
    
    def invert(matrix):
        '''(Matrix) -> Matrix or str
        Returns the inverse of given matrix, if the matrix is not invertable
        then "Not Invertable" is returned
        '''
        # find determinant
        det = matrix.determinant()
        
        # if determinant is 0 then matrix is not invertable
        if(det == 0):
            result = "Not Invertable"
            
        else:
            clone = matrix.copy()
            result = clone.find_inverse()
            # round decimals
            for row in range(matrix._size):
                for column in range(matrix._size):
                    result._entries[row][column] = round(result._entries[row][column],3)

        return result
                
    def find_inverse(self):
        '''(Matrix) -> Matrix
        Takes a Matrix and returns the inverse
        '''
        # create an identity matrix
        inverse = Matrix.identity(self.get_size())
        clone = self._entries[:]
        for i in range(self._size):
            inverse.add_entry(i, i, 1)
        # for every row in the matrix
        for pivot in range(self._size):
            # if the pivot is equal to zero
            if(clone[pivot][pivot] == 0):
                # swap the row with another that is below it
                not_swap = True
                next_row = 1
                while(not_swap):
                    # if the next row is equal to zero
                    if(clone[next_row][pivot] == 0):
                        # check next row
                        next_row += 1
                    # if the next row is not zero
                    else:
                        # swap the rows
                        temp_row = clone[pivot]
                        clone[pivot] = clone[next_row]
                        clone[next_row] = temp_row
                        # do the same for the inverse
                        temp_row = inverse._entries[pivot]
                        inverse._entries[pivot] = inverse._entries[next_row]
                        inverse._entries[next_row] = temp_row
                        # break the loop
                        not_swap = False
            # reduce the value of row so the pivot = 1
            value = clone[pivot][pivot]
            for column in range(self._size):
                clone[pivot][column] = clone[pivot][column]/value
                inverse._entries[pivot][column] = inverse._entries[pivot][column]/value
            # make all other rows at this column = 0
            for row in range(self._size):
                if(row != pivot):
                    value = clone[row][pivot]
                    # for every column in the current row
                    for column in range(self._size):
                        clone[row][column] = clone[row][column]- (value*clone[pivot][column])
                        inverse._entries[row][column] = inverse._entries[row][column]-(value*inverse._entries[pivot][column])
        return inverse
        
    def copy(matrix):
        '''(Matrix) -> Matrix
        Returns a hard copy of the given Matrix
        '''
        result = Matrix(matrix.get_size())
        result._entries = matrix._entries[:]
        return result
        
    def get_size(self):
        '''(Matrix) -> int
        returns the size of the matrix
        '''
        return self._size
                    
    def identity(size):
        '''(int) -> Matrix
        Creates and returns an identity matrix of given size
        '''
        identity = Matrix(size)
        # create a zero matrix
        for row in range(identity.get_size()):
            for column in range(identity.get_size()):
                identity.add_entry(row, column,0)
        # create pivots = 1
        for i in range(identity.get_size()):
            identity.add_entry(i,i,1)
            
        return identity