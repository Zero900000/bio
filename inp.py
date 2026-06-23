import pygame
import euk

automatic_updates = True

def calc_allele_frequency(population): #returns a dictionary
    result = {}
    for organism in population:
        for chromosome in organism.genome:
            for gene in chromosome:
                result.update({gene: [0, 0]})
    for organism in population:
        for chromosome in organism.genome:
            for gene in chromosome:
                for allele in chromosome[gene].alleles:
                    index = 1
                    if allele.dominant:
                        index = 0
                    result[gene][index] += 1
    return result
def allele_frequency_to_str(frequency):
    intermed = ""
    for trait in frequency:
        dom = frequency[trait][0]
        rec = frequency[trait][1]
        total = dom + rec
        dom_percent = int((dom / total) * 100)
        intermed += trait + ": "
        intermed += str(dom) + " dom (" + str(dom_percent) + "%), "
        intermed += str(rec) + " rec (" + str(100 - dom_percent) + "%) || "
    result = ""
    for char_index in range(len(intermed) - 4):
        result += intermed[char_index]

    return result
def status_update():
    seperator = "/"
    result = seperator
    result += "population: " + str(len(euk.eukaryotes)) + seperator
    result += " " + seperator + allele_frequency_to_str(calc_allele_frequency(euk.eukaryotes)) + seperator
    return result
def detect_commands(event):
    ref = event.key
    if ref == pygame.K_p:
        print("population: " + str(len(euk.eukaryotes)))
    if ref == pygame.K_f:
        print(allele_frequency_to_str(calc_allele_frequency(euk.eukaryotes)))
    if ref == pygame.K_s:
        print(status_update())
    if ref == pygame.K_a:
        global automatic_updates
        automatic_updates = not automatic_updates