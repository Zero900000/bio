import random
import math
import pygame
import euk
import scr
import var
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

while var.game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            var.game = False
    scr.screen.fill((255,255,255))
    for eukaryote in euk.eukaryotes:
        eukaryote.run()
        eukaryote.display()
    pygame.display.update()