supported_areas = {"protected_area", "nature_reserve", "forest"}

def is_polygon_interested(element: object) -> bool:
    if element["type"] != "relation":
        return False

    tags = element.get("tags", {})
    name = tags.get("name") or tags.get("ref")

    if not name:
        return False

    return get_area_type(element) in supported_areas

def get_area_type(element: object) -> str:
    tags = element.get("tags", {})
    if tags.get("boundary") == "protected_area":
        return "protected_area"
    elif tags.get("leisure") == "nature_reserve":
        return "nature_reserve"
    elif tags.get("landuse") == "forest":
        return "forest"
    else:
        return "unknown"
    
def merge_rings(ways):
    if not ways:
        return []

    unmerged = [list(way) for way in ways]
    closed_rings = []

    while unmerged:
        current_ring = unmerged.pop(0)

        while current_ring[0] != current_ring[-1]:
            match_index = -1
            reverse = False
            append_front = False

            for i, way in enumerate(unmerged):
                if current_ring[-1] == way[0]:      # Matches end-to-start
                    match_index, reverse, append_front = i, False, False
                    break
                elif current_ring[-1] == way[-1]:   # Matches end-to-end
                    match_index, reverse, append_front = i, True, False
                    break
                elif current_ring[0] == way[-1]:    # Matches start-to-end
                    match_index, reverse, append_front = i, False, True
                    break
                elif current_ring[0] == way[0]:     # Matches start-to-start
                    match_index, reverse, append_front = i, True, True
                    break

            if match_index != -1:
                way = unmerged.pop(match_index)
                if reverse:
                    way = way[::-1]
                
                if append_front:
                    current_ring = way[:-1] + current_ring
                else:
                    current_ring = current_ring + way[1:]
            else:
                break
                
        closed_rings.append(current_ring)
        
    return closed_rings