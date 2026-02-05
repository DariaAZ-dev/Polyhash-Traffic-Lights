#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module principal pour la mise en oeuvre du projet Poly#."""

import sys
from polyparser import parse_challenge
from polyscorer import score_solution, save_solution

# Import de l'heuristique gagnante (Solver 3)
from polysolver_4 import solve

def _usage_and_exit():
    print("Usage: python polyhash.py challenge.txt output.txt")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        _usage_and_exit()
    challenge_file = sys.argv[1]
    output_file = sys.argv[2]

    # 1. Chargement
    print(f"Lecture de {challenge_file}...")
    challenge = parse_challenge(challenge_file)
    
    # 2. Résolution (Solver 3)
    print("Résolution avec Solver 3 (Bracket Scaling)...")
    solution = solve(challenge)
    
    # 3. Sauvegarde
    if output_file is not None:
        save_solution(output_file, solution)
        print(f"Solution sauvegardée dans {output_file}")
    
    # 4. Score
    print(f"Score: {score_solution(challenge, solution):,}")
