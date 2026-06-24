import random
import math
import pygame
import euk
import inp
import scr
import var
import numpy as np
from numba import njit, prange
import settings
timer = 0
clock = pygame.time.Clock()
stat_update_tick = 0
stat_update_frequency = 10
def class_to_numpy_detect(cls):
    result = [None] * len(cls)
    for index in range(len(cls)):
        result[index] = [cls[index].x, cls[index].y, cls[index].size, cls[index].sensing_range]
    return np.array(result)
def class_to_numpy_interact(cls):
    result = [None] * len(cls)
    for index in range(len(cls)):
        org = cls[index]
        result[index] = [org.x, org.y, org.size, org.interaction_range, org.energy > 1.5 * org.energy_cap * org.offspring, org.sexual_compatibility]
    return np.array(result)
@njit(parallel=True,fastmath=True)
def detect_closest(cell_pos, targt_pos):
    num_cells = len(cell_pos)
    num_targets = len(targt_pos)
    closest_ind = np.full(num_cells,-1,dtype=np.int32)
    for i in prange(num_cells):
        # print(cell_pos)
        cx = cell_pos[i, 0]
        cy = cell_pos[i, 1]
        closest_idx = -1
        base_min_dist = cell_pos[i, 2] + cell_pos[i, 3]
        first = True
        for j in range(num_targets):
            if first:
                min_dist = base_min_dist + targt_pos[j, 2]
            if i != j:
                tx = targt_pos[j][0]
                ty = targt_pos[j][1]

                dx = tx - cx
                dy = ty - cy
                distance = math.hypot(dx, dy)
                if distance < min_dist:
                    min_dist = distance
                    closest_idx = j
                    first = False
        closest_ind[i] = closest_idx
    # for index in range(num_cells):
    #     if closest_ind[index] == -1:
    #         closest_ind[index] = None
    return closest_ind
@njit(parallel=True,fastmath=True)
def detect_closest_inter(cell_pos, targt_pos):
    num_cells = len(cell_pos)
    num_targets = len(targt_pos)
    closest_ind = np.full(num_cells,-1,dtype=np.int32)
    for i in prange(num_cells):
        # print(cell_pos)
        cx = cell_pos[i, 0]
        cy = cell_pos[i, 1]
        closest_idx = -1
        base_min_dist = cell_pos[i, 2]
        first = True
        for j in range(num_targets):
            if first:
                min_dist = base_min_dist + targt_pos[j, 2]
            if i != j:
                tx = targt_pos[j][0]
                ty = targt_pos[j][1]

                dx = tx - cx
                dy = ty - cy
                distance = math.hypot(dx, dy)
                if distance < base_min_dist + targt_pos[j, 2]:
                    if cell_pos[i][4] and abs(cell_pos[i, 5] - targt_pos[j, 5]) <= 1.0:
                        closest_idx = j
                        break
                if distance < min_dist:
                    min_dist = distance
                    closest_idx = j
                    first = False
        closest_ind[i] = closest_idx
    # for index in range(num_cells):
    #     if closest_ind[index] == -1:
    #         closest_ind[index] = None
    return closest_ind

# print(calc_status_update())
while var.game:
    clock.tick(10)
    # timer += 1
    # if timer >= 150:
    #     print("result: ")
    #     print(inp.calc_populations(euk.eukaryotes))
    #     print(inp.allele_frequency_to_str(inp.calc_allele_frequency(euk.eukaryotes)))
    #     break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            var.game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                var.paused = not var.paused
            inp.detect_commands(event)
                # print("population: " + str(len(euk.eukaryotes)))

    if inp.automatic_updates:
        if stat_update_tick > stat_update_frequency:
            stat_update_tick = 0
            print("update:")
            print(inp.calc_populations(euk.eukaryotes))
            print(inp.status_update())
        stat_update_tick += 1
    if var.paused:
        continue
    scr.screen.fill((255,255,255))
    death_index = 0

    while death_index <= len(euk.eukaryotes) - 1:
        if euk.eukaryotes[death_index].energy <= 0.0:
            euk.eukaryotes.pop(death_index)
            if inp.automatic_updates and False: print("an organism has died")
        else:
            death_index += 1
    for eukaryote in euk.eukaryotes:
        eukaryote.display()
        eukaryote.run()
    euk_raw_detect = class_to_numpy_detect(euk.eukaryotes) # for normal detection
    euk_raw_interact = class_to_numpy_interact(euk.eukaryotes) # for reprod and other interactions
    # print(detect_closest(euk_raw, euk_raw))

    if len(euk.eukaryotes) > 0:
        euk_closest = detect_closest(euk_raw_detect, euk_raw_detect)
        euk_interact = detect_closest_inter(euk_raw_interact, euk_raw_interact)
        for index in range(len(euk_closest)):
            other_index_det = euk_closest[index]
                # euk.eukaryotes[index].reproduction(euk.eukaryotes[other_index])
            euk.eukaryotes[index].behavior(other_index_det, euk.eukaryotes)
            other_index_inter = euk_interact[index]
            if other_index_inter != -1:
                # print("interacting")
                euk.eukaryotes[index].interact(euk.eukaryotes[other_index_inter], euk.eukaryotes)
    
    if len(euk.eukaryotes) == 0:
        print("population extinct, ending simulation")
        var.game = False

    pygame.display.update()
    # print(len(euk.eukaryotes))
    # var.game = False