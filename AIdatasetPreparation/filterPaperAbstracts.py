# --------------LIBRARIES--------------------
import multiprocessing as mp
from functools import partial
import os, re, time
import json

# -----------READ AND FILTER from 'PaperAbstracts.nt'-------------
# Read and match keywords with Pool (share in cores' set)

def ReadAndMatch(file,directory_samples,keywords,directory_filtered) :

    n = re.findall(r'\d+', file)[0] #the number of the file
    text_file = open(directory_samples + file)
    data = text_file.read() #read whole file to a string
    text_file.close() #close file

    papers = data.replace('<http://purl.org/dc/terms/abstract>','').split('^^<http://www.w3.org/2001/XMLSchema#string> .')
    match = []

    for el in papers[1:-1] :

        if any(ext.lower() in el.lower() for ext in keywords) :

            d = {}
            vv = el.replace('\n','').split('> ')
            d[vv[0].replace('<http://ma-graph.org/entity/','')] = vv[1]
            match.append(d)

    #write all matched papers in independent json files
    with open(directory_filtered + f'filtered{n}.json','w') as js :
        json.dump(match,js,indent=2)

    return dict(zip(['numfile','firstline','lastline'],[int(n),papers[0],papers[-1]])) #return only the dicts of the uncomplete lines of all files

def UncompleteLinesMatching(uncomplete,keywords,directory,filename) :

    sort = sorted(uncomplete, key = lambda x: x['numfile']) #sort the dictionnaries
    match = []

    # if there is at least one keyword in the first line of the first file, append it to match
    # in the last line of the last file because they are already complete, append it to match
    very_firstline = sort[0]['firstline']
    very_lastline = sort[-1]['firstline']
    if any(ext.lower() in very_firstline.lower() for ext in keywords) :
        match.append(very_firstline)
    if any(ext.lower() in very_lastline.lower() for ext in keywords) :
        match.append(very_lastline)

    #recombine broken lines and check if there is a match
    for i in range(len(sort)-1) :
        paper = sort[i]['lastline'] + ' ' + sort[i+1]['firstline']

        if any(ext.lower() in paper.lower() for ext in keywords) :
            d = {}
            vv = paper.replace('\n','').split('> ')
            d[vv[0].replace('<http://ma-graph.org/entity/','')] = vv[1]
            match.append(d)

    with open(directory + filename,'w') as js :
        json.dump(match,js,indent=2)

#Merge all JSON files in a directory into a single one
def MergeJSON(directory,filename) :

    files = os.listdir(directory)
    if filename in files :
        files = files[:-1]

    all_papers = []

    for file in files :
        with open(f'{directory}/{file}', 'r') as j :
            data = json.load(j)
            for i in data :
                all_papers.append(i)

    with open(f'{directory}/{filename}', 'w') as bj :
        print(len(all_papers))
        json.dump(all_papers,bj,indent=2)

#---------------EXECUTION-----------------

keywords = []
for line in open(r"your_path/wiki_ai_keywords.csv"):
    keywords = line[:-1].rstrip().replace('\'','').lower().split(', ')

keys = ['numfile','firstline','lastline']

dir_samples = ..
files = os.listdir(dir_samples)
dir_filtered = ..
files = files[1:]

nb_processes = 2

t1 = time.time()

if __name__ == '__main__' :

    pool = mp.Pool(nb_processes)
    # first treatment with static arguments
    temp = partial(ReadAndMatch, directory_samples=dir_samples, keywords=keywords,directory_filtered=dir_filtered)
    # map only on the dynamic variables, here the files. Return a tupe of results of all processes
    result = pool.map(func=temp, iterable=files)
    pool.close()
    pool.join()

UncompleteLinesMatching(result,keywords,dir_filtered,'uncomplete_bis.json')

MergeJSON(dir_filtered,'globalIA.json')

t2 = time.time()
print(f"Time for {nb_processes} processes = ", t2 - t1)
