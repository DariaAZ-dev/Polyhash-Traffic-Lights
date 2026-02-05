#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
polyparser.py - parse un fichier challenge sans utiliser de bibliothèques externes.

Fonction exportée :
    parse_challenge(filename) -> dict
"""
def _read_nonempty_noncomment_line(f):
    # Retourne la prochaine ligne non vide et non comment (commentaire débutant par '#'),
    # ou None si fin de fichier.
    while True:
        line = f.readline()
        if not line:
            return None
        s = line.strip()
        if s == "":
            continue
        # support simple commentaires commençant par '#'
        if s.startswith("#"):
            continue
        return s

def parse_challenge(filename):
    """
    Parse un fichier challenge et renvoie un dict :
    {
      "meta": {"D":..., "I":..., "S":..., "V":..., "F":...},
      "streets": {street_name: (B, E, L), ...},
      "incoming": {intersection_id: [street_name, ...], ...},
      "paths": [ [street_name,...], ... ]  # une liste par voiture
    }
    """
    try:
        f = open(filename, "r", encoding="utf-8")
    except Exception:
        raise FileNotFoundError("Fichier introuvable: " + filename)

    # première ligne utile
    first = _read_nonempty_noncomment_line(f)

    if first is None:
        raise ValueError("Error : first is none")

    parts = first.split()
    D = int(parts[0]); I = int(parts[1]); S = int(parts[2]); V = int(parts[3]); F = int(parts[4])
    meta = {"D": D, "I": I, "S": S, "V": V, "F": F}

    # lire S descriptions de rues
    streets = {}       # street_name -> (B, E, L)
    incoming = {}      # inter_id -> list of street_names
    for i in range(I):
        incoming[i] = []

    for si in range(S):
        line = _read_nonempty_noncomment_line(f)
        
        if line is None:
            raise ValueError("Error : line is none")
    
        tokens = line.split()
        B = int(tokens[0]); E = int(tokens[1]); name = tokens[2]; Ltime = int(tokens[3])
        streets[name] = (B, E, Ltime)
        # ajouter à incoming
        if E not in incoming:
            incoming[E] = [name]
        else:
            incoming[E].append(name)

    # lire V chemins de voitures
    paths = []
    for vi in range(V):
        line = _read_nonempty_noncomment_line(f)

        if line is None:
            raise ValueError("Error : line is none")

        tokens = line.split()
        P = int(tokens[0])
        street_names = tokens[1:]
        paths.append(street_names)

    f.close()
    return {"meta": meta, "streets": streets, "incoming": incoming, "paths": paths}

    #TODO give each road its own time depending on  how busy the road is

# Petit test local si exécuté directement
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python polyparser.py input.txt")
    else:
        ch = parse_challenge(sys.argv[1])
        print("META:", ch["meta"])
        print("Nb rues:", len(ch["streets"]))
        print("Nb voitures:", len(ch["paths"]))

        print("incoming:", ch["incoming"])
        print("path:",ch["paths"])

