from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import numpy as numpy

# Distance callback
def create_distance_callback(W):
    # Create a callback to calculate distances between cities.

    def distance_callback(from_node, to_node):
        return int(W[from_node][to_node])

    return distance_callback

import numpy as np
import pdb
# import tqdm

def print_path(filename, path):
    fp = open(filename.split('.')[0]+'.out', 'w')
    fp.write(str(len(path))+'\n')
    fp.write('\n'.join([str(x) for x in path]))
    fp.close()

def find_path(idlist, W):
	path = [idlist[0]]
	prev_row = 0
	# for i in range(0, N):
	while True:
		maxcol = -1
		# argpos = np.argsort(W[i,:])
		# while (1):
		next_row = np.argmax(W[prev_row, :])
		if (W[prev_row, next_row] > 0):
			path.append(idlist[next_row])
			W[:, prev_row] = 0
			prev_row = next_row
			# print(next_row)
			# print(W)
		else:
			break
	# print path
	return path

def find_weights(photos):
    W = []
    for i, item_i in enumerate(photos):
        W.append([])
        A = set(item_i['tags'])
        for j, item_j in enumerate(photos):
            B = set(item_j['tags'])
            W[i].append(min([len(A.intersection(B)), len(A.difference(B)), len(B.difference(A))]))
    # print np.array(W)
    return np.array(W)

def vertical_to_slides(verticalPhotos):
    slides = []
    alreadyPicked = []
    chechingAgain = False
    # all_Idx = list(range(len(verticalPhotos)))
    for i in range(0, len(verticalPhotos)):
        if not chechingAgain:
            minCommonTags = 0
        else:
            i = i-1
        if (i in alreadyPicked):
            continue
        A = set(verticalPhotos[i]['tags'])
        for j in range(0, len(verticalPhotos)):
            if (j <= i) or (j in alreadyPicked):
                continue
            chechingAgain = False
            B = set(verticalPhotos[j]['tags'])
            if len(A.intersection(B)) <= minCommonTags:
                alreadyPicked.append(i)
                alreadyPicked.append(j)
                # pdb.set_trace()
                slides.append({'id':str(verticalPhotos[i]['id']) + ' ' + str(verticalPhotos[j]['id']), 'tags': list(A.union(B))})
                break
            if j == len(verticalPhotos)-1:
                minCommonTags += 1
                chechingAgain = True
    return slides

def find_verticals(photos):
    # complete = [i for i in range(0, N)]
    verticals = [i for i, photo in enumerate(photos) if (photo['align'] == 'V')]
    return verticals 

def read_input(filename):
    fp = open(filename, 'r').read().split('\n')
    photos = []
    for i, line in enumerate(fp):
        if (i==0):
            N = int(line)
        elif len(line)>0:
            id = i-1
            align = line.split(' ')[0]
            tags = [x for x in line.split(' ')[2:]]
            photos.append({'id':str(id), 'align': align, 'tags': tags})
    # print (N, photos)
    return N, photos

def photos(filename):
    # Nodes and weights
    N, photos = read_input(filename)
    complete = [x for x in range(0, N)]
    V = find_verticals(photos)
    H = [x for x in complete if x not in V]
    # print V
    v_photos = [photo for i, photo in enumerate(photos) if i in V]
    h_slides = [photo for i, photo in enumerate(photos) if i not in V]

    v_slides = vertical_to_slides(v_photos)
    for slide in v_slides:
        h_slides.append(slide)

    # print(h_slides)
    W = find_weights(h_slides)
    idlist = [item['id'] for item in h_slides]
    # path = find_path([item['id'] for item in h_slides], W)
    

    # city_names = ["New York", "Los Angeles", "Chicago", "Minneapolis", "Denver", "Dallas", "Seattle",
    #                 "Boston", "San Francisco", "St. Louis", "Houston", "Phoenix", "Salt Lake City"]

    #   W = [
    #     [   0, 2451,  713, 1018, 1631, 1374, 2408,  213, 2571,  875, 1420, 2145, 1972], # New York
    #     [2451,    0, 1745, 1524,  831, 1240,  959, 2596,  403, 1589, 1374,  357,  579], # Los Angeles
    #     [ 713, 1745,    0,  355,  920,  803, 1737,  851, 1858,  262,  940, 1453, 1260], # Chicago
    #     [1018, 1524,  355,    0,  700,  862, 1395, 1123, 1584,  466, 1056, 1280,  987], # Minneapolis
    #     [1631,  831,  920,  700,    0,  663, 1021, 1769,  949,  796,  879,  586,  371], # Denver
    #     [1374, 1240,  803,  862,  663,    0, 1681, 1551, 1765,  547,  225,  887,  999], # Dallas
    #     [2408,  959, 1737, 1395, 1021, 1681,    0, 2493,  678, 1724, 1891, 1114,  701], # Seattle
    #     [ 213, 2596,  851, 1123, 1769, 1551, 2493,    0, 2699, 1038, 1605, 2300, 2099], # Boston
    #     [2571,  403, 1858, 1584,  949, 1765,  678, 2699,    0, 1744, 1645,  653,  600], # San Francisco
    #     [ 875, 1589,  262,  466,  796,  547, 1724, 1038, 1744,    0,  679, 1272, 1162], # St. Louis
    #     [1420, 1374,  940, 1056,  879,  225, 1891, 1605, 1645,  679,    0, 1017, 1200], # Houston
    #     [2145,  357, 1453, 1280,  586,  887, 1114, 2300,  653, 1272, 1017,    0,  504], # Phoenix
    #     [1972,  579, 1260,  987,  371,  999,  701, 2099,  600, 1162,  1200,  504,   0]] # Salt Lake City

    tsp_size = len(h_slides)
    num_paths = 1
    depot = 0

    # Create routing model
    if tsp_size > 0:
        routing = pywrapcp.RoutingModel(tsp_size, num_paths, depot)
        search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
        # Create the distance callback.
        dist_callback = create_distance_callback(W)
        routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)
        # Solve the problem.
        assignment = routing.SolveWithParameters(search_parameters)
        if assignment:
            print ("Total distance: " + str(assignment.ObjectiveValue()) + " miles\n")
            # Solution distance.
            # Display the solution.
            # Only one path here; otherwise iterate from 0 to routing.vehicles() - 1
            path_number = 0
            index = routing.Start(path_number) # Index of the variable for the starting node.
            path = [idlist[0]]
            while not routing.IsEnd(index):
                # Convert variable indices to node indices in the displayed path.
                path.append(idlist[routing.IndexToNode(index)])
                index = assignment.Value(routing.NextVar(index))
            path.append(idlist[routing.IndexToNode(index)])
        else:
            print ('No solution found.')
    else:
        print ('Specify an instance greater than 0.')
    del path[len(path)-1]
    del path[0]
    print_path(filename, path)

if __name__ == '__main__':
    # filename = 'a_example.txt'
    # photos(filename)
    # filename = 'b_lovely_landscapes.txt'
    # photos(filename)
    filename = 'c_memorable_moments.txt'
    photos(filename)
    # filename = 'd_pet_pictures.txt'
    # photos(filename)
    # filename = 'e_shiny_selfies.txt'
    # photos(filename)