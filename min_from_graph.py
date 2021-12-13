airports = [ "BGI", "CDG", "DEL", "DOH", "DSM", "EWR", "EYW", "HND", "ICN", "JFK", "LGA", "LHR", "ORD", "SAN", "SFO", "SIN", "TLV", "BUD" ]

stagingAirport = "LGA"

routes = [["DSM", "ORD"],
      	["ORD", "BGI"],
      	["BGI", "LGA"],
      	["SIN", "CDG"],
      	["CDG", "SIN"],
      	["CDG", "BUD"],
      	["DEL", "DOH"],
      	["DEL", "CDG"],
      	["TLV", "DEL"],
      	["EWR", "HND"],
      	["HND", "ICN"],
      	["HND", "JFK"],
      	["ICN", "JFK"],
      	["JFK", "LGA"],
      	["EYW", "LHR"],
      	["LHR", "SFO"],
      	["SFO", "SAN"],
      	["SFO", "DSM"],
      	["SAN", "EYW"]]


class Graph:
    def __init__(self, routes) -> None:
        self.routes = routes
        self.heads = set()
        self.children_of_heads = dict()
        self.graph = self.construct_graph()
        self.find_heads()
        self.all_children = self.find_all_children()

    def construct_graph(self):
        graph = dict()
        starting = set([start[0] for start in routes])
        for item in starting:
            graph[item] = set([place[1] for place in routes if place[0] == item])
        return graph
    
    def find_heads(self):
        for place in [places[0] for places in routes if places[0] not in [destinations[1] for destinations in routes]]:
            self.heads.add(place)
            self.find_children(place)

    def find_children(self, head):
        # first add first layer children
        self.children_of_heads[head] = self.graph[head]
        # then add further layers
        already_done = set()
        not_done = True
        while not_done:
            for x in list(self.children_of_heads[head]):
                if x not in already_done and x in self.graph:
                    self.children_of_heads[head].update(self.graph[x])
                already_done.add(x)
            if already_done == self.children_of_heads[head]:
                not_done = False

    def find_all_children(self):
        children = set()
        for key, value in self.children_of_heads.items():
            children.update(value)
        return children

def find_min(missing, missed_dict):
    if missed_dict == {}: return []
    d2 = {tuple(v): k for k, v in missed_dict.items()}  # exchange keys, values (to remove duplicates)
    missed_dict = {v: list(k) for k, v in d2.items()}   # exchange again
    #  now remove items that are common to all
    result = set([missed_dict[item] for item in missed_dict.keys()][0])
    for item in missed_dict.keys():
        result.intersection_update(item)
    for item in missed_dict.keys():
        for common_element in result:
            missed_dict[item].remove(common_element)
        if missed_dict[item] == []:
            missed_dict.pop(item)
    # we should now need everything thats left
    return [head for head in missed_dict.keys()]

                  

def min_additions(destinations, routes, starting):
    graph = Graph(routes)
    # first find whats not in the routes at all    
    minimum = [[starting, missed] for missed in destinations if missed not in graph.heads and missed not in graph.all_children]
    for item1, item2 in minimum:
        destinations.remove(item2)
    #return minimum
    # If one head is not in the destinations list AND the other head can get to all destinations, then we only need to connect to one head
    included = [head for head in graph.heads if head in destinations]
    if set(included) == graph.heads:
        minimum.extend([[starting, head] for head in graph.heads])
        return minimum
    # check if non-needed head goes to anywhere that is needed that the other heads can't get to
    full = set()
    for head in included:
        full.update(graph.children_of_heads[head])
        full.add(head)
    missing = [place for place in destinations if place not in full]
    if missing == []:
        minimum.extend([[starting, head] for head in included])
        return minimum
    else:
        # now need to find which heads to inlcude to get to remainder
        missed_dict = dict()
        for head in [head for head in graph.heads if head not in included]:
            missed_dict[head] = [item for item in missing if item in graph.children_of_heads[head]]
            if missed_dict[head] == missing:
                # that means we only need to inlcude this one head
                return minimum.extend([[starting, missed] for missed in missing])
        found_missing = find_min(missing, missed_dict)
        if found_missing:
            minimum.extend([[starting, place] for place in found_missing])
        return minimum

if __name__ == '__main__':
    print(min_additions(airports, routes, stagingAirport))
