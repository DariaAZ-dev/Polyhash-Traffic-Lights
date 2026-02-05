
def score_solution(challenge, solution):
    
    meta = challenge["meta"]
    streets = challenge["streets"]
    paths = challenge["paths"]
    D = meta["D"]
    F = meta["F"]
    V = meta["V"]

    # préparer cycles -> dict intersection_id -> {"sequence": [(street_name,duration),...], "total": total}
    inter_cycles = {}
    for intersection_id, sequence in solution.items():
        total = 0
        for pair in sequence:
            total += pair[1]
        inter_cycles[intersection_id] = {"sequence": sequence, "total": total}

    # structures de simulation
    queues = {}  # queues[street_name] = list of car ids (FIFO)
    for street_name in streets.keys():
        queues[street_name] = []

    car_pos = [0] * V            # indice de la rue actuelle dans path
    finished_time = [None] * V
    arrivals = {}                # arrivals[t] = list of (cid, street_name, pos_idx)

    # initial : voitures en fin de la première rue -> en queue sur path[0]
    for car_id in range(len(paths)):
        path = paths[car_id]
        if len(path) == 0:
            finished_time[car_id] = 0
            continue
        first = path[0]
        queues[first].append(car_id)
        car_pos[car_id] = 0

    # simulation t = 0..D-1
    t = 0
    while t < D:
        # process arrivals at t
        if t in arrivals:
            arrival_list = arrivals[t]
            for (car_id, street_name, pos_idx) in arrival_list:
                car_pos[car_id] = pos_idx
                if pos_idx == len(paths[car_id]) - 1:
                    finished_time[car_id] = t
                else:
                    # ajouter en queue à la rue (street_name)
                    if street_name not in queues:
                        queues[street_name] = []
                    queues[street_name].append(car_id)
            del arrivals[t]

        # pour chaque intersection, traiter feu vert
        for intersection_id, cycle in list(inter_cycles.items()):
            total = cycle["total"]
            if total == 0:
                continue
            sequence = cycle["sequence"]
            offset = t % total
            accumulated_time = 0
            green = None
            for pair in sequence:
                street_name = pair[0]; duration = pair[1]
                if accumulated_time <= offset < accumulated_time + duration:
                    green = street_name
                    break
                accumulated_time += duration
            if green is None:
                continue
            queue = queues.get(green, [])
            if len(queue) > 0:
                car_id = queue.pop(0)  # dequeue
                i = car_pos[car_id]
                next_idx = i + 1
                if next_idx >= len(paths[car_id]):
                    finished_time[car_id] = t
                    continue
                next_street = paths[car_id][next_idx]
                L = streets[next_street][2]
                arrive_time = t + L
                arrival_list = arrivals.get(arrive_time, [])
                arrival_list.append((car_id, next_street, next_idx))
                arrivals[arrive_time] = arrival_list

        t += 1

    # calcul du score
    score = 0
    for car_id in range(V):
        finish_time = finished_time[car_id]
        if finish_time is not None and finish_time <= D:
            score += F + (D - finish_time)
    return score


def save_solution(path, solution):
    
    try:
        f = open(path, "w", encoding="utf-8")
    except Exception:
        raise IOError("Impossible d'ouvrir le fichier de sortie: " + path)
    lines = []
    lines.append(str(len(solution)))
    for intersection_id, sequence in solution.items():
        lines.append(str(intersection_id))
        lines.append(str(len(sequence)))
        for pair in sequence:
            lines.append(pair[0] + " " + str(pair[1]))
    f.write("\n".join(lines) + "\n")
    f.close()
