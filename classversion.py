# Lexi und Finn
#
# Evolutionärer Algorithmus zum Finden von Futter
# mit Sensorik

import random

class DNA_Sequence:
    def __init__(self, data_length = 1, data_value_set = [], data = []):
        self.data_length = data_length
        self.data_value_set = data_value_set
        self._generate_data() # Fills self.data


    # Combine this DNA sequence with another one
    # Return a new DNA sequence
    def combine(self, other):
        # Define a point where to  split the sequences
        split_point = random.randrange(0, self.data_length)
        new_data = self.data[:split_point] + other.data[split_point:] 
        return DNA_Sequence(self.data_length, self.data_value_set, new_data)

    def get_length(self):
        return len(self.data)

    def mutate(self):
        key = random.randrange(0, len(self.data))
        self.data[key] = random.choice( self.data_value_set )
        return self

    def _generate_data(self):
        self.data = []
        for i in range(self.data_length):
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
            crossed_over.append( self.dna_sequences[i].combine(other.dna_sequences[i]) )
        return DNA(crossed_over)

    # Randomly change parts of the own DNA sequences
    def mutate(self):
        for dna_sequence in self.dna_sequences:
            dna_sequence.mutate()
        return self

class Creature:
    def __init__(self, dna, world, position = (0,0)):
        self.dna = dna
        self.position = position
        self.food = 0
        self.world = world.copy()

        # DNA Usage
        self.food_sense_distance = self.dna.dna_sequences[0].data[0]
        self.move_food_path = self.dna.dna_sequences[1].data
        self.move_general_path = self.dna.dna_sequences[2].data

    def __str__(self):
        return "Food: {}, Vision: {}".format(self.food, self.food_sense_distance)

    # Breeds the child this and the other creature
    # Return new Creature
    def breed(self, other):
        return Creature( self.dna.crossover(other.dna).mutate(), world )

    # DNA Usage
    # Seq 0 = Maximum Distance for sensing food
    # Seq 1 = Food Move Path
    # Seq 2 = General Move Path

    # The acts done until it dies
    def live(self, moves):
        for i in range(moves):
            self.act()
        return self.food

    # The creature acts upon the world
    def act(self):
        # If already at food, remove it
        if(self.world.is_food_at(self.position[0], self.position[1])):
            block = self.world.get_block(self.position[0], self.position[1])
            block.has_food = False
            self.food += 1

        direction = self._sense_food()
        if( direction ):
            self._move_food( direction )
        else:
            self._move_general()
        return self

    # Returns direction in which the food is to find
    def _sense_food(self):
        # TODO: Search square around you
        # For now: Search the cross around you
        
        directions = [(0,1),(1,0),(-1,0),(0,-1)]
        
        for distance in range( self.food_sense_distance ):
            for x, y in directions:
                if self.world.is_food_at(self.position[0] + x, self.position[1] + y):
                    return (x, y)
        return None

    # Move in the direction of specified vector
    def _move(self, vector):
        self.position = (self.position[0] + vector[0], self.position[1] + vector[1])
        return self

    def _move_food(self, direction):
        self._move(direction)
        return self

    def _move_general(self):
        for step in self.move_general_path:
            self._move( step )
        return self

class Block:
    def __init__(self, has_food = False):
        self.has_food = has_food

class World: 
    def __init__(self, width, height, blocks = None):
        self.width = width
        self.height = height
        if (blocks):
            self.blocks = blocks
        else:
            self.blocks = []
            self.random_fill()


    def random_fill(self):
      for x in range(self.width):
        self.blocks.append([])
        for y in range(self.height):
            self.blocks[x].append( Block( random.random() > 0.5 ) )      

    def is_food_at(self, x, y):
        block = self.get_block(x, y)
        if block:
            return block.has_food
        else:
            return False

    def get_block(self, x, y):
        try:
            return self.blocks[x][y]
        except IndexError:
            return None

    def copy(self):
        new_blocks = []
        for x in range(self.width):
            new_blocks.append([])
            for y in range(self.height):
                new_blocks[x].append( self.blocks[x][y] )
        return World(self.width, self.height, new_blocks)

class Generation:
    def __init__(self, size, creatures = None):
        self.size = size

        if creatures:
            self.creatures = creatures
        else:
            self._populate() # Fill self.creatures

    def next_generation(self, world):
        for creature in self.creatures:
            creature.live(15)
        # Sort creatures by fitness
        self.creatures.sort(key = lambda c: c.food)
        # breed
        children = []
        for i in range(self.size):
            children.append( self.creatures[0].breed( self.creatures[1] ) )

        print(self.creatures[0])
        return Generation(self.size, children)

    def _populate(self):
        self.creatures = []
        for i in range(self.size):
            dna_sequence_sense_food =  DNA_Sequence(data_length = 1, data_value_set = [x for x in range(1,10)])
            dna_sequence_move_food = DNA_Sequence(data_length = 4, data_value_set = [(1,0),(0,1),(-1,0),(0,-1)])
            dna_sequence_move_general = DNA_Sequence(data_length = 4, data_value_set = [(1,0),(0,1),(-1,0),(0,-1)])
            dna = DNA(dna_sequences = [dna_sequence_sense_food, dna_sequence_move_food, dna_sequence_move_general])
            self.creatures.append( Creature(dna, world) )

if __name__ == "__main__":
    world = World(100, 100)
    GENERATION_SIZE = 25
    GENERATION_NUMBER = 2500

    # Create initial generation
    generation = Generation( GENERATION_SIZE )

    # Loop through generations
    for i in range(GENERATION_NUMBER):
        generation = generation.next_generation(world)
        world.random_fill()
