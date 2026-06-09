import random
import math
import numpy as np
from numba import njit, prange

@njit(parallel=True,fastmath=True)
def detect_closest(cell_pos,targt_pos,sensing_range):
    num_cells = cell_pos.shape[0]
    num_targets=targt_pos.shape[0]

    closest_ind = np.full(num_cells,-1,dtype=np.int32)

    for i in prange(num_cells):
        cx,cy = cell_pos[i,0], cell_pos[i,1]
        closest_idx = -1
        min_dist = sensing_range

        for j in range(num_targets):
            tx,ty = targt_pos[j,0], targt_pos[j,1]

            dx = tx-cx
            dy=ty-cy
            distance = math.hypot(dx,dy)
            if distance<min_dist:
                min_dist=distance
                closest_idx = j
        closest_ind[i] = closest_idx
    return closest_ind
    
class Speed:
    def __init__(self, dominant: bool, value: float):
        self.dominant = dominant
        self.value = value

    def express(self, organism):
        organism.speed += self.value
        # FIXED THE TRADE OFF SO IT ISN'T BROKEN
        organism.energy_consumption_change += (self.value * 0.1)


class Gene:
    def __init__(self, allele_pair):
        self.alleles = list(allele_pair)  # [Allele 1, Allele 2]? Is that what you were going for?

        if self.alleles[1].dominant:
            self.phen = self.alleles[1]
        else:
            self.phen = self.alleles[0]

class photosynthetic:
    def __init__(self,dominant: bool, value: bool):
        self.dominant = dominant
        self.value = value
    def express(self,organism):
        if self.value:
            organism.is_photosynthetic = True
            organism.speed *= 0.5


class Eukaryote:
    def __init__(self, genome, energy, x=0, y=0): #added x and y for detection
        self.genome = genome
        self.energy = energy
        self.x = x
        self.y = y
        self.age = 0

        self.speed = 0.0
        self.is_photosynthetic = False
        self.energy_consumption_change  = 0.0
        # 1. Dynamically express all alleles (attaches .photosynthetic, .sensing_range, etc.)
        for chromosome in self.genome:
            for gene in chromosome:
                gene.phen.express(self)
        
#hasattr basically checks if an object jas a specific attribute or not
        if not hasattr(self, "sensing_range"): self.sensing_range = 30.0
        if self.speed <= 0.0:
            self.speed = 1.0

    @property
    def energy_consumption(self):
        base_cost = 0.2
        # Running faster or having  eyes/sensors costs more energy
        trait_costs = (self.speed ** 2 * 0.05) + (self.sensing_range * 0.002) + self.energy_consumption_change
        
        # Ensure energy consumption never drops below a tiny minimum cost to stay alive
        return max(0.02, base_cost + trait_costs)

    def run(self):
        self.age += 1
        self.energy -= self.energy_consumption
        if self.is_photosynthetic:
            self.energy += 0.5

    
    def reproduction(self,closest_target):
        if isinstance(closest_target,Eukaryote) == True:
            #reproduction
            None
        else:
            #add some food class? Do you want me to do that
            None