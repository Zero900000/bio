import math
import random
import scr
#trait list: speed, durability (hp), energy cap (how much energy an organism will acquire before trying to reproduce),
# digestion speed / efficiency (more speed = less efficiency), cold or warmblooded, photosynthetic, mutation resistance,
# number of offspring, crossover rate


#alleles
class Speed:
    def __init__(self, dominant: bool, value = None):
        self.dominant = dominant
        self.value = value
        if value is None:
            if self.dominant:
                self.value = 4.0
            else:
                self.value = 2.0
    def express(self, organism):
        organism.speed += self.value
        organism.energy_consumption += (self.value * 0.1)

class Photosynthetic:
    def __init__(self, dominant: bool, value = None):
        self.dominant = dominant
        self.value = value
        if value is None:
            if self.dominant:
                self.value = 2.0
            else:
                self.value = 0.0
    def express(self, organism):
        if self.value > 0.0:
            organism.is_photosynthetic = True
            organism.speed /= self.value
            organism.energy_consumption_change += self.value

#genes
class Gene:
    def __init__(self, allele_pair: tuple):
        self.alleles = allele_pair  # (Allele 1, Allele 2)
        if self.alleles[1].dominant:
            self.phen = self.alleles[1]
        else:
            self.phen = self.alleles[0]

class Eukaryote:
    def __init__(self, genome, energy, pos): #added x and y for detection
        self.genome = genome
        self.energy = energy
        self.x = pos[0]
        self.y = pos[1]
        self.age = 0
        self.speed = 0.0
        self.is_photosynthetic = False
        self.energy_consumption = 0.0
        self.crossover_rate = 0.2
        self.color = (0,0,0)
        self.sensing_range = 5
        self.sexual_compatibility = 4.0
        self.energy_cap = 10.0
        self.offspring = 2
        # 1. Dynamically express all alleles (attaches .photosynthetic, .sensing_range, etc.)
        for chromosome in self.genome:
            for gene in chromosome:
                chromosome[gene].phen.express(self)
        if self.is_photosynthetic:
            self.color = (0, 127, 0)

#hasattr basically checks if an object jas a specific attribute or not
        if not hasattr(self, "sensing_range"): self.sensing_range = 30.0
        if self.speed <= 0.0:
            self.speed = 1.0

    # @property
    # def energy_consumption(self):
    #     base_cost = 0.2
    #     # Running faster or having  eyes/sensors costs more energy
    #     trait_costs = (self.speed ** 2 * 0.05) + (self.sensing_range * 0.002) + self.energy_consumption_change
	#
    #     # Ensure energy consumption never drops below a tiny minimum cost to stay alive
    #     return max(0.02, base_cost + trait_costs)

    def run(self):
        self.age += 1
        self.energy -= self.energy_consumption
    def display(self):
        size = (self.energy, self.energy)
        scr.rect((self.x - size[0] * 0.5, self.y - size[1] * 0.5), size, self.color)
    # def detect_closest(self,targets):
    #
    #     closest_target = None
    #     closest_dis = self.sensing_range
    #
    #     for target in targets:
    #         if target == self:
    #             continue
    #
    #         dx = target.x - self.x
    #         dy = target.y - self.y
    #         distance = math.hypot(dx,dy)
    #
    #         if distance < closest_dis:
    #             closest_dis = distance
    #             closest_target = target
    #     return closest_target

    def meiosis(self):
        proper_genome = [[],[]]
        for chromosome_number in range(len(self.genome)):
            proper_genome[0].append({})
            proper_genome[1].append({})
            for gene in self.genome[chromosome_number]:
                proper_genome[0][chromosome_number].update({gene: self.genome[chromosome_number][gene].alleles[0]})
                proper_genome[1][chromosome_number].update({gene: self.genome[chromosome_number][gene].alleles[1]})
        # print(proper_genome)
        for chromosome_number in range(len(proper_genome[0])):
            for gene_name in proper_genome[0][chromosome_number]:
                if random.random() < self.crossover_rate:
                    place_holder = proper_genome[0][chromosome_number][gene_name]
                    proper_genome[0][chromosome_number][gene_name] = proper_genome[1][chromosome_number][gene_name]
                    proper_genome[1][chromosome_number][gene_name] = place_holder
        gamete = []
        for chromosome_number in range(len(proper_genome[0])):
            gamete.append(proper_genome[0][chromosome_number])
        return gamete
    def new(self):
        return Eukaryote(self.genome, self.energy, (self.x, self.y))
    def reproduction(self, target, population = None):#WIP
        if population is None:
            population = eukaryotes
        if isinstance(target, Eukaryote):
            if abs(self.sexual_compatibility - target.sexual_compatibility) <= 1: #reproduction
                self_cost = self.energy_cap * self.offspring
                if self.energy > self_cost * 1.5 and target.energy > target.energy_cap * target.offspring * 1.5:
                    self.energy -= self_cost
                    for offspring_index in range(self.offspring):
                        self_gamete = self.meiosis()
                        target_gamete = target.meiosis()
                        new_genome = self.genome
                        gamete_index = 0
                        for chromosome in new_genome:
                            for gene in chromosome:
                                chromosome[gene].alleles = self_gamete[gamete_index], target_gamete[gamete_index]
                                gamete_index += 1
                        population.append(Eukaryote(new_genome, (self.energy_cap + target.energy_cap) * 0.5, (self.x, self.y)))
        else:
            #add some food class? Do you want me to do that
            pass
rabbit = Eukaryote([{"speed" : Gene((Speed(True), Speed(True)))}, {"photosynthetic" : Gene((Photosynthetic(False), Photosynthetic(False)))}], 50, (0, 0))
# eukaryotes = [None] * 8
# for index in range(len(eukaryotes)):
#     eukaryotes[index] = rabbit.new()
#     eukaryotes[index].x = random.randint(0, scr.screen_size[0])
#     eukaryotes[index].y = random.randint(0, scr.screen_size[1])
eukaryotes = [rabbit.new(), rabbit.new()]

print(rabbit.meiosis())
# class Eukaryote:
# 	def __init__(self, genome, energy):
# 		self.genome = genome
# 		self.energy = energy
# 		self.speed = 0
# 		self.energy_consumption = 0
# 		self.crossover_rate = 0.2
# 		for chromosome in genome:
# 			for gene in chromosome:
# 				gene.phen.express(self)
# 		# for chromosome_number in range(len(genome[0])):
# 		# 	for gene_name in genome[0][chromosome_number]:
# 		# 		first_allele = genome[0][chromosome_number][gene_name]
# 		# 		second_allele = genome[1][chromosome_number][gene_name]
# 		# 		if second_allele.dominant:
# 		# 			second_allele.express(self)
# 		# 		else:
# 		# 			first_allele.express(self)
# 	def run(self):
# 		self.energy -= self.energy_consumption


# d_speed_al = Speed(True, 4)
# r_speed_al = Speed(False, 2)
# homo_dom_genome = [[Gene((d_speed_al, d_speed_al))]]
# rabbit = Eukaryote(homo_dom_genome, 5)
# print(rabbit.speed)
# rabbit.run()
# print(rabbit.energy)
