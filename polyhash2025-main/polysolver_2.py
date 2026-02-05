def collecting_road_occurences(paththing): # take all roads and store it in a dict[str,int]

    paths : list[list] = paththing

    roads_dict : dict[str,int] = {}

    for path in paths:

        for road in path:

            if road in roads_dict:
                roads_dict[road] +=1
            else :
                roads_dict[road] = 1    

    return roads_dict


def get_min_max(roads_dict:dict): # get min max value from dict[str,int]
    
    occ_min = next(iter(roads_dict.values())) # we tke first value in dict
    occ_max = occ_min

    for v in roads_dict.values():
        
        if v > occ_max:
            occ_max = v
        
        if v < occ_min:
            occ_min = v

    return occ_min,occ_max    

def give_proportional_time(roads_dict: dict, max_time: int, min_time: int = 1): # ignore this, depreciated
    
    if not roads_dict: # Sécurité si le dico est vide
        return {}

    occ_min, occ_max = get_min_max(roads_dict)

    delta_temps = max_time - min_time 
    delta_occ = occ_max - occ_min 

    dict_road_time = {} 

    if delta_occ == 0: 
        temps = (max_time + min_time) // 2 
        for road in roads_dict:
            dict_road_time[road] = temps      

    else: 
        for road, count in roads_dict.items():
            
            if count == occ_max:
                dict_road_time[road] = max_time
            elif count == occ_min:
                dict_road_time[road] = min_time    
            else:
                # CORRECTION MATHÉMATIQUE ICI :
                # On multiplie AVANT de diviser pour garder la précision tout en restant en entiers
                # Formule : min_time + (position_relative * echelle_temps)
                
                numerateur = (count - occ_min) * delta_temps
                ajout = numerateur // delta_occ # Division entière à la fin
                
                temps = min_time + ajout
                #temps = max_time
                dict_road_time[road] = temps   

    return dict_road_time


def give_proportional_time_2(roads_dict: dict, max_time: int = 2, min_time: int = 1):# use this one, better
    
    if not roads_dict:
        return {}

    # 1. On calcule le score "racine carrée" pour chaque rue
    # Cela réduit naturellement l'écart entre les petites et grosses rues
    scores = {}
    for road, count in roads_dict.items():
        scores[road] = count ** 0.5  # Astuce Python pour racine carrée sans 'math'

    # 2. On récupère les bornes de ces nouveaux scores
    min_score = min(scores.values())
    max_score = max(scores.values())
    delta_score = max_score - min_score

    dict_road_time = {}

    for road, score in scores.items():
        
        if delta_score == 0:
            # Si tout le monde a le même trafic
            temps = (max_time + min_time) // 2
        else:
            # 3. Interpolation linéaire basée sur le score racine
            ratio = (score - min_score) / delta_score
            
            # Formule pour projeter sur [min_time, max_time]
            valeur_flottante = min_time + (ratio * (max_time - min_time))
            
            # Arrondi manuel à l'entier le plus proche (sans module math)
            temps = int(valeur_flottante + 0.5) 

        # Sécurité pour rester dans les bornes (clamp)
        if temps < min_time: temps = min_time
        if temps > max_time: temps = max_time
        
        dict_road_time[road] = temps

    return dict_road_time


def solver_1_solution(dict_road_time: dict, incoming: dict):
    
    solution = {}

    for key, value in incoming.items(): 
        nouvelle_liste = []
        
        for e in value:
            # On vérifie d'abord si la rue existe dans le dictionnaire
            if e in dict_road_time:
                temps = int(dict_road_time[e])
            else:
                # Si elle n'existe pas, on met une valeur par défaut (ex: 1 seconde)
                # Cela permet d'éviter le KeyError ET le TypeError plus tard
                # print(f"Attention : Rue '{e}' non trouvée dans dict_road_time. Valeur par défaut utilisée.")
                temps = 0
            
            # On ajoute le tuple. 'temps' est garanti d'être un entier.
            nouvelle_liste.append((e, temps))
        
        solution[key] = nouvelle_liste

    return solution

if __name__=='__main__':
    import sys
    from polyparser import parse_challenge
    from polysolver import solve
    from polyscorer import score_solution, save_solution


    table_challenge = ["./challenges/a_example.in","challenges/b_ocean.in","challenges/c_checkmate.in",
                       "challenges/e_etoile.in","challenges/d_daily_commute.in","challenges/f_forever_jammed.in"]
    
    total_score_nouv_solution = 0
    total_score_anc_solution = 0

    for e in table_challenge:

        ch = parse_challenge(e)
        roads_dict = collecting_road_occurences(ch["paths"])
        dict_roads_time = give_proportional_time_2(roads_dict,max_time=2)

        nouv_sol = solver_1_solution(dict_roads_time,ch['incoming'])
        anc_sol = solve(ch)

        nouv_score = score_solution(ch,nouv_sol)
        anc_score = score_solution(ch,anc_sol)

        total_score_anc_solution += anc_score
        total_score_nouv_solution += nouv_score

    print("first method :",total_score_anc_solution,"second method :", total_score_nouv_solution)

    pass
