#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des deux heuristiques sur tous les challenges
"""

import os
from polyparser import parse_challenge
from polysolver import solve as solver_original
from solver_2 import solve as solver_ratio
from polyscorer import score_solution

challenges_dir = "./challenges"
challenge_files = [
    "a_example.in",
    "b_ocean.in",
    "c_checkmate.in",
    "d_daily_commute.in",
    "e_etoile.in",
    "f_forever_jammed.in"
]

print("=" * 80)
print("COMPARAISON DES HEURISTIQUES SUR TOUS LES CHALLENGES")
print("=" * 80)
print()

results = []

for filename in challenge_files:
    filepath = os.path.join(challenges_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"  {filename} - Fichier non trouvé")
        continue
    
    print(f" {filename}...")
    
    try:
        challenge = parse_challenge(filepath)
        
        # Test heuristique originale
        sol1 = solver_original(challenge)
        score1 = score_solution(challenge, sol1)
        
        # Test heuristique Linear Ratio
        sol2 = solver_ratio(challenge)
        score2 = score_solution(challenge, sol2)
        
        diff = score2 - score1
        percent = (diff / score1 * 100) if score1 > 0 else 0
        
        results.append({
            'file': filename,
            'score1': score1,
            'score2': score2,
            'diff': diff,
            'percent': percent
        })
        
        # Affichage compact
        winner = "" if diff > 0 else "" if diff == 0 else ""
        print(f"   Original: {score1:>12,}  |  Ratio: {score2:>12,}  |  {winner} {diff:+,} ({percent:+.2f}%)")
        print()
        
    except Exception as e:
        print(f"    Erreur: {e}")
        print()

# Résumé
print("=" * 80)
print("RÉSUMÉ")
print("=" * 80)

total_original = sum(r['score1'] for r in results)
total_ratio = sum(r['score2'] for r in results)
total_diff = total_ratio - total_original
total_percent = (total_diff / total_original * 100) if total_original > 0 else 0

print(f"Score total Original:     {total_original:>15,}")
print(f"Score total Linear Ratio: {total_ratio:>15,}")
print(f"Différence:               {total_diff:>15,} ({total_percent:+.2f}%)")
print()

if total_diff > 0:
    print(" L'heuristique Linear Ratio GAGNE !")
elif total_diff < 0:
    print(" L'heuristique Originale est MEILLEURE")
else:
    print(" Les deux heuristiques sont ÉQUIVALENTES")

print("=" * 80)
