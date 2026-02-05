#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
polysolver.py - Heuristique de résolution pour le challenge Poly#

Fonction exportée :
 - solve(challenge) -> solution_dict

Ce module contient l'heuristique de résolution. Pour le scoring et la sauvegarde,
voir le module polyscorer.py qui est indépendant et réutilisable.

Politique implémentée :
 - intersections avec 0 incoming ou 0 outgoing : rien (tout rouge)
 - intersections avec 1 incoming : cette rue a le vert toute la durée D
 - intersections avec >1 incoming : 1s à chaque rue entrante qui a >=1 voiture (ordre d'origine)
"""
def solve(challenge):
    meta = challenge["meta"]
    D = meta["D"]
    streets = challenge["streets"]      # name -> (B,E,L)
    incoming = challenge["incoming"]    # inter -> [street_name,...]
    paths = challenge["paths"]          # list of [street_name,...]

    # compter nombre de voitures par rue
    freq = {}
    for p in paths:
        for s in p:
            freq[s] = freq.get(s, 0) + 1

    # calculer outgoing counts
    outgoing_count = {}
    for sname, beL in list(streets.items()):
        B = beL[0]
        outgoing_count[B] = outgoing_count.get(B, 0) + 1

    solution = {}  # intersection_id -> [(street_name, duration), ...]

    for inter in incoming.keys():
        ins = incoming.get(inter, [])
        in_count = len(ins)
        out_count = outgoing_count.get(inter, 0)

        # règle : si 0 incoming ou 0 outgoing => on ignore (tout rouge)
        if in_count == 0 or out_count == 0:
            continue

        # si 1 incoming => toujours vert sur cette rue (durée = D)
        if in_count == 1:
            s = ins[0]
            if s in streets:
                solution[inter] = [(s, D)]
            continue

        # si >1 incoming => 1s pour chaque rue active (freq>0)
        active = []
        for s in ins:
            if freq.get(s, 0) > 0:
                active.append(s)
        if len(active) == 0:
            # aucune rue actives -> rien
            continue
        seq = []
        for s in active:
            seq.append((s, 1))
        solution[inter] = seq

    return solution

