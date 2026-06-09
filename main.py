import random
import math

class Speed:
    def __init__(self, dominant: bool, value: float):
        self.dominant = dominant
        self.value = value

    def express(self, organism):
        organism.speed += self.value
        # FIXED THE TRADE OFF SO IT ISN'T BROKEN
        organism.energy_consumption += (self.value * 0.1)


class Gene:
    def __init__(self, allele_pair):
        self.alleles = list(allele_pair)  # [Allele 1, Allele 2]? Is that what you were going for?

        if self.alleles[1].dominant:
            self.phen = self.alleles[1]
        else:
            self.phen = self.alleles[0]




class Eukaryote:
    def __init__(self, genome, energy, x=0, y=0): #added x and y for detection
        self.genome = genome
        self.energy = energy
        self.x = x
        self.y = y
        self.age = 0
        
        # 1. Dynamically express all alleles (attaches .photosynthetic, .sensing_range, etc.)
        for chromosome in self.genome:
            for gene in chromosome:
                gene.phen.express(self)
        
        if not hasattr(self, "photosynthetic"): self.photosynthetic = 0.0 #hasattr basically checks if an object jas a specific attribute or not
        if not hasattr(self, "sensing_range"): self.sensing_range = 30.0 
        if not hasattr(self, "speed"): self.speed = 1.0
    @property
    def energy_consumption(self):
        base_cost = 0.2
        # Running faster or having  eyes/sensors costs more energy
        trait_costs = (self.speed ** 2 * 0.05) + (self.sensing_range * 0.002)
        
        photo_off = self.photosynthetic * 0.4 
        
        # Ensure energy consumption never drops below a tiny minimum cost to stay alive
        return max(0.02, base_cost + trait_costs - photo_off)

    def run(self):
        self.age += 1
        self.energy -= self.energy_consumption

    def detect_closest(self,targets):

        closest_target = None
        closest_dis = self.sensing_ran

        for target in targets:
            if target == self:
                continue
        
            dx = target.x -  self.x
            dy = target.y - self.y
            distance = math.hyplot(dx,dy)

            if distance < closest_dis:
                closest_dis = distance
                closest_target = target
        return closest_target
    
    def reproduction(self,closest_target):
        if isinstance(closest_target,Eukaryote) == True:
            #reproduction
            None
        else:
            #add some food class? Do you want me to do that
            None