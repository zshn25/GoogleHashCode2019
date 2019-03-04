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
    path = find_path([item['id'] for item in h_slides], W)
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

