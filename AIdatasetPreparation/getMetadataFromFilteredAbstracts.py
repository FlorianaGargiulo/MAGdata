# --------------LIBRARIES--------------------
import multiprocessing as mp
from functools import partial
import os, re, time
from natsort import natsorted
import json
import shutil

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

# ---------FIND ASSOCIATED METADATA FOR AI PAPERS (PARALLELIZED) (on AIfiltered's json)-----------------
# EDIT : USE OF SIMPLIFIED FILE OF PAPERS
# EDIT : USE OF AUTOMATIC REDUCING OF FILTERED ABSTRACTS'S FILES IN ORDER TO SPEED UP THE MATCHING ALONG THE PROCESS

def SearchAndAddMetadata(file,directory_abstracts,metadata,num_metafile,directory_filtered): # duration for one abstracts' file : ~15sec

    print('enter')
    num = re.findall(r'\d+', file)[0]  # the number of the file
    with open(f'{directory_abstracts}/{file}','r') as f :
        abstracts = json.load(f)
    IDs = []
    for ab in abstracts:
        IDs.append(list(ab.keys())[0])
    allID = [m['id'] for m in metadata]
    match = set(allID).intersection(set(IDs)) # best way of matching : intersection of sets (built-in)
    indices = [allID.index(i) for i in match] # return the indices of the found IDs in the list allID
    papers_match = []
    remove = [] # get the indices in 'abstracts' in order to remove it and rewrite a reduced file
    print('match done!')
    for i in indices :
        d = metadata[i]
        ind = IDs.index(d['id'])
        d['abstract'] = abstracts[ind][IDs[ind]][2:-1]
        remove.append(ind)
        papers_match.append(d)

    if papers_match :
        # write matches into a new file
        with open(f'{directory_filtered}/filtered{num_metafile}{num}.json','w') as js :
            json.dump(papers_match,js,indent=2)
        papers_match.clear()
        match.clear()
        indices.clear()

        # remove the old file and rewrite another reduced one
        update_abstracts = [abstracts[i] for i in range(len(abstracts)) if i not in remove]
        os.remove(f'{directory_abstracts}/{file}')
        with open(f'{directory_abstracts}/{file}', 'w') as js :
            json.dump(update_abstracts,js,indent=2)
        remove.clear()
        update_abstracts.clear()

    abstracts.clear()
    IDs.clear()
    allID.clear()

if __name__ == '__main__' :

    path_allpapers = ..
    path_abstractsAI = ..
    path_abstractsAI_copy = ..
    path_filteredAI = ..

    # to prevent errors : remove copy folder and get the initial files before starting the process
    if os.path.exists(path_abstractsAI_copy) :
        shutil.rmtree(path_abstractsAI_copy)
    shutil.copytree(path_abstractsAI,path_abstractsAI_copy)

    # if output path exists remove the old files in the destination folder if it is not empty
    # else create the path
    if os.path.exists(path_filteredAI) :
        if any(os.scandir(path_filteredAI)) :
            shutil.rmtree(path_filteredAI)
            # time.sleep(10)
            os.mkdir(path_filteredAI)
    else :
        os.mkdir(path_filteredAI)

    files = natsorted(os.listdir(path_abstractsAI_copy))
    nb_processes = 8
    manager = mp.Manager()

    for file in natsorted(os.listdir(path_allpapers)): # duration for one metadata file : ~10min

        t1 = time.time()
        n = re.findall(r'\d+', file)[0]
        with open(f'{path_allpapers}/{file}', 'r') as js:
            papers = json.load(js)
        print('open!')

        pool = mp.Pool(nb_processes)
        # first treatment with static arguments
        temp = partial(SearchAndAddMetadata, directory_abstracts=path_abstractsAI_copy, metadata=papers, num_metafile=n, directory_filtered=path_filteredAI)
        # map only on the dynamic variables, here the files. Return a type of results of all processes
        pool.map(func=temp, iterable=files)
        pool.close()
        pool.join()

        papers.clear()

        t2 = time.time()
        print(t2-t1)

# Merge the splits
MergeJSON(path_filteredAI,'AImetadata.json')
