# Lexi und Finn
#
# Evolutionärer Algorithmus zum Finden von Futter
# mit Sensorik

import random

class DNA_Sequence:
    def __init__(self, data_length = 1, data_value_set = []):
        self.data_length = data_length
        self.data_value_set = data_value_set
        self._generate_data() # Fills self.data


    # Combine this DNA sequence with another one
    # Return a new DNA sequence
    def combine(self, other):
        # Define a point where to  split the sequences
        split_point = random.random(0, sequence_length)
        new_data = self.data[:split_point] + other.data[split_point:] 
        return DNA_Sequence(self.mutate_func, new_data)

    def get_length(self):
        return len(self.data)

    def mutate(self):
        key = random.random(0, len(self.data))
        self.data[key] = random.choice( self.data_value_set )
        return self

    def _generate_data(self):
        self.data = []
        for i in range(data_length):
            self.data.append( random.choice( self.data_value_set ) )
        return self



class DNA:
    def __init__(self, dna_sequences = []):
        self.dna_sequences = dna_sequences # two dimensional array of DNA_sequences
        # [ [1,2,3,5], [5,5,6], [5,3,2,6] ...]

    # Takes another DNA and crosses itself with it
    # Return new DNA    
    def crossover(self, other):
        crossed_over = []
        for i in range( len(self.dna_sequences) ):
            # Combine fraction of self sequence with fraction of other sequence
            crossed_over[i] = self.dna_sequences[i].combine(other.dna_sequences[i])
        return DNA(crossed_over)

    # Randomly change parts of the own DNA sequences
    def mutate(self):
        for dna_sequence in self.dna_sequences:
            dna_sequence.mutate()

class Creature:
    def __init__(self, dna, position = (0,0)):
        self.dna = dna
        self.position = position

        # DNA Usage
        self.food_sense_distance = self.dna.dna_sequences[0].data[0]
        self.move_food_path = self.dna.dna_sequences[1].data
        self.move_general_path = self.dna.dna_sequences[2].data

    # Breeds the child this and the other creature
    # Return new Creature
    def breed(self, other):
        return Creature( self.dna.crossover(other.dna).mutate() )

    # DNA Usage
    # Seq 0 = Maximum Distance for sensing food

    # The creature acts upon the world
    def act(self, world):
        if( direction = self._sense_food(world) ):
            self._move_food( direction )
        else
            self._move_general()

    # Returns direction in which the food is to find
    def _sense_food(self, world):
        # TODO: Search square around you
        # For now: Search the cross around you
        
        directions = [(0,1),(1,0),(-1,0),(0,-1)]
        
        for distance in range( self.food_sense_distance )
            for x, y in directions:
                world.is_food_at(self.position[0] + x, self.position[1] + y):
                    return (x, y)
        return None

    # Move in the direction of specified vector
    def _move(self, vector):
        self.position[0] += vector[0]
        self.position[1] += vector[1]
        return self

    def _move_food(self, direction):
        self.move(direction)
        return self

    def _move_general(self):
        for step in self.move_general_path:
            self.move( step )
        return self

class Block:
    def __init__(self, has_food = False):
        self.has_food = has_food

class World: 
    def __init__(self, width, height):
        self.blocks = []
        self.width = width
        self.height = height
        for x in range(width):
            self.blocks[x] = []
            for y in range(height):
                self.blocks[x][y] = Block( Math.random() > 0.9 )

    def is_food_at(self, x, y):
        block = self.get_block(x, y)
        if block:
            return block.has_food
        else:
            return False

    def get_block(self, x, y):
        try:
            return self.block[x][y]
        except IndexError:
            return None

if __name__ == "__main__":
    world = World(100, 100)
    generation_size = 25
    

    # Create initial generation
    generation = []
    for i in range(generation_size):
        dna_sequence_sense_food = DNA_Sequence(data_length = 1, data_value_set = [x for x in range(1,4)])
        dna_sequence_move_food = DNA_Sequence(data_length = 4, data_value_set = [(1,0),(0,1),(-1,0),(0,-1)])
        dna_sequence_move_general = DNA_Sequence(data_length = 4, data_value_set = [(1,0),(0,1),(-1,0),(0,-1)])
        dna = DNA(dna_sequences = [dna_sequence_sense_food, dna_sequence_move_food, dna_sequence_move_general])
        generation[i] = Creature(dna)


    # Loop through generations





