import random
import copy

target_point = (10, 5)
start_point = (0, 0)

possible_steps = [(-1,0),(0,1),(0,-1),(1,0)]

# Return the Entpoint of the given movement
def perform_steps(start_point, steps):
    end_point = (start_point[0], start_point[1])
    for step in steps:
        end_point = vec_add(end_point, step)
    return end_point

# Add two Vektors
def vec_add(vec1, vec2):
    return (vec1[0] + vec2[0], vec1[1] + vec2[1])

# Calculates the Manhattan Distance between two vectors
def distance(vec1, vec2):
    return (abs(vec1[0] - vec2[0]) + abs(vec1[1] - vec2[1]))


# Return random sequence of steps from possible_steps with the lenght of the minimum way from 
# start_point to target_point
def create_initial_steps():
    nsteps = distance(start_point, target_point)
    steps = []
    for i in range(nsteps):
        steps.append(possible_steps[random.randrange(len(possible_steps))])
    return steps

# n is the size of the generation
def create_first_generation(n):
    generation = []
    for i in range(n):
        generation.append(create_initial_steps())
    return generation

# Takes steps and creates mutations
def mutate(steps):
    mutated_step = random.randrange(len(steps))
    new_step = possible_steps[random.randrange(len(possible_steps))]
    child_steps = []
    for step in steps:
        child_steps.append(step)
    child_steps[mutated_step] = new_step
    return child_steps

def create_new_generation(parent, n):
    new_generation = [parent]
    for i in range(n):
        new_generation.append( mutate(parent) )
    return new_generation

# Calculates the fitness
def fitness(steps):
    return distance(perform_steps(start_point, steps), target_point)

# Takes: Generation is a list of steps
def select_best(generation):
    min_n = fitness(generation[0])
    min_steps = generation[0]

    for steps in generation:
        dist = fitness(steps)
        if dist < min_n:
            min_n = dist
            min_steps = copy.copy(steps)
    return min_steps



generation_size = 5
max_generations = 2000

generation = create_first_generation( generation_size )

for i in range( max_generations ):
    best = select_best(generation)
    print(fitness(best))
    # print(best)
    generation = create_new_generation(best, generation_size)

print(best)



