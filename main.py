import random
import math

class Cell:
    def __init__(self,parent_gene=None):
        #gene that gets passed and mutated
        if parent_gene:
            self.gene = parent_gene
        else:
            self.gene = {
                'max_speed':2.0,
                'size':10.0,
                'sensing_range':50.0,
                'reproduction_strategy':'asexual' #we can talk about how we want to do sexual later

            }
    
        #phenotype? (is that what it's called?) traits
        self.max_speed = self.gene['max_speed']
        self.size = self.gene['size']
        self.sensing_range = self.gene['sensing_range']
        self.strategy = self.gene['reproduction_strategy']

        #starting stats
        self.energy = 100.0
        self.age = 0

        #ADD WHATEVER YOU NEED FOR PYGAMES HERE!!!


    def update(self):
        #call every frame or something idk
        self.age +=1
        #gotta nerf cells so bigger ones use wayyy more energy i think that's how it works in bio)
        energy_cost = (self.size*0.05)+(self.max_speed**2*0.1) #these numbers work fine for now 
        self.energy -= energy_cost
    
    #mutation bit
    def mutate(self,geneome):
        mutated_gene = geneome.copy()
        mutation_rate = 0.2 #20% chance of mutation it's really really visiable 
        mutation_visibility = 0.2 #how much traits change or something i think

        for trait in mutated_gene:
            if trait == 'reproduction_strategy':
                None #tell me what you want to happen here I think a continue block would be the best idea

            if random.random() < mutation_rate:
                change = random.uniform(-mutation_visibility,mutation_visibility)
                mutated_gene[trait] += mutated_gene[trait] * change

                #if traits become 0 or negative
                if mutated_gene[trait] <0.1: #or do you want 0.01?
                    mutated_gene[trait] = 0.1
        return mutated_gene
    
    def reproduce_asexual(self):
        self.energy /= 2
        child_gene = self.mutate(self.gene)
        child = Cell(parent_gene=child_gene)

        #Put pygame stuff here ig?

        return child

    def reporduce_sexual(self, partner):
        None
        #How will we do the need for a partner im thinking if 2 cells are close enough they cause just make a child if enough energy (subtract 25 from each) and make a child out of that with crossing over