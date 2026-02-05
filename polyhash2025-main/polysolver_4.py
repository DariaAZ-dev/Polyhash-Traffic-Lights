def solve(challenge):
    # --- DATA EXTRACTION ---
    # Extracting core challenge components:
    # streets: dict of street details, paths: list of car routes, 
    # incoming: mapping of which streets enter which intersection.
    streets = challenge["streets"]
    paths = challenge["paths"]
    incoming = challenge["incoming"]
    
    # --- PILLAR 1: GLOBAL DEMAND ANALYSIS ---
    # We count how many cars will ever travel on each street (Frequency).
    # Logic: More cars = more green-light time needed.
    # Note: We ignore the last street in a path (p[-1]) because cars 
    # don't cross an intersection at their final destination.
    freq = {}
    for p in paths:
        for i in range(len(p) - 1):
            s = p[i]
            freq[s] = freq.get(s, 0) + 1

    # --- PILLAR 2: INITIAL BOTTLENECK REMOVAL (T=0 Strategy) ---
    # We identify "Starter" streets where cars are already waiting at Time = 0.
    # Logic: Clearing these immediately prevents a queue 'ripple effect' 
    # across the whole map, which is crucial for maximizing early arrivals.
    starts = {}
    for p in paths:
        first_street = p[0]
        starts[first_street] = starts.get(first_street, 0) + 1

    solution = {}
    for inter, ins in incoming.items():
        # --- PILLAR 3: TRAFFIC FILTERING ---
        # We only consider 'active' streets (those with at least one car).
        # This prevents wasting time on empty intersections (Green light for 0 cars).
        active = []
        for s in ins:
            if s in freq:
                active.append(s)
        
        if not active:
            continue

        # --- PILLAR 4: DYNAMIC HEURISTIC SORTING ---
        # We prioritize the schedule order based on two criteria:
        # 1. Primary Priority: Does it have T=0 waiting cars? (starts)
        # 2. Secondary Priority: Total volume of cars (freq)
        # Result: The busiest, most urgent streets get the green light first.
        active.sort(key=lambda s: (starts.get(s, 0), freq.get(s, 0)), reverse=True)

        # --- PILLAR 5: BRACKET SCALING (Efficiency Optimization) ---
        # Instead of heavy math libraries or linear scaling (which makes cycles too long),
        # we use 'Bracket Logic'. 
        # Goal: Keep total cycle duration low (1-4s) so traffic flows constantly.
        res = []
        for s in active:
            count = freq[s]
            
            # Non-linear assignment to prevent 'starvation' of low-traffic streets
            # while giving a slight edge to heavy traffic.
            if count <= 10:
                duration = 1
            elif count <= 50:
                duration = 2
            elif count <= 200:
                duration = 3
            else:
                duration = 4
                
            res.append((s, duration))
        
        # Mapping the schedule to the specific intersection ID
        solution[inter] = res

    return solution