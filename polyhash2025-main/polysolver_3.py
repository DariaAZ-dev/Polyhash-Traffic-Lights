#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
polysolver_3.py - Heuristique Linear Ratio Proportionnelle

Politique implémentée :
 - intersections avec 0 incoming ou 0 outgoing : rien (tout rouge)
 - intersections avec 1 incoming : cette rue a le vert toute la durée D
 - intersections avec >1 incoming : Linear Ratio basé sur le trafic réel
   et un budget temps (MAX_Ti) spécifique à l'intersection.
"""

def solve(challenge):
    meta = challenge["meta"]
    D = meta["D"]
    streets = challenge["streets"]      # name -> (B,E,L)
    incoming = challenge["incoming"]    # inter -> [street_name,...]
    paths = challenge["paths"]          # list of [street_name,...]

    # --- PARAMÈTRES DE RÉGLAGE ---
    # Optimisé par tests : 0.5 à 1 donnent les meilleurs scores
    AVG_GREEN_TIME = 1
    SINGLE_STREET_DURATION = 1  # Pour intersections avec 1 seule rue entrante 

    # 1. Compter le nombre de voitures passant par chaque rue (Demande)
    freq = {}
    for p in paths:
        for s in p:  # Compte TOUTES les rues
            freq[s] = freq.get(s, 0) + 1

    # 2. Calculer le nombre de sorties par intersection
    outgoing_count = {}
    for sname, beL in streets.items():
        B = beL[0]
        outgoing_count[B] = outgoing_count.get(B, 0) + 1

    solution = {}  # intersection_id -> [(street_name, duration), ...]

    for inter, ins in incoming.items():
        in_count = len(ins)
        out_count = outgoing_count.get(inter, 0)

        # Règle : si 0 incoming ou 0 outgoing => on ignore
        if in_count == 0 or out_count == 0:
            continue

        # Règle : si 1 incoming => feu vert court (pas besoin de D entier)
        if in_count == 1:
            s = ins[0]
            # On ne l'allume que si au moins une voiture l'emprunte
            if freq.get(s, 0) > 0:
                solution[inter] = [(s, SINGLE_STREET_DURATION)]
            continue

        # Règle : si >1 incoming => Stratégie Linear Ratio Proportionnelle
        # On ne garde que les rues entrantes qui ont du trafic
        active_streets = {s: freq[s] for s in ins if freq.get(s, 0) > 0}
        
        if not active_streets:
            continue

        # Calcul du budget temps pour cette intersection (MAX_Ti)
        ei = len(active_streets)
        max_ti = ei * AVG_GREEN_TIME
        total_cars_at_inter = sum(active_streets.values())

        seq = []
        for s, count in active_streets.items():
            # Formule de ratio linéaire
            # (Trafic de la rue / Trafic total inter) * Budget Total
            valeur_flottante = (count / total_cars_at_inter) * max_ti
            
            # Arrondi à l'entier le plus proche, minimum 1s
            duration = int(valeur_flottante + 0.5)
            if duration < 1:
                duration = 1
                
            seq.append((s, duration))
        
        solution[inter] = seq

    return solution