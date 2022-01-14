# --------------LIBRARIES--------------------
import multiprocessing as mp
from functools import partial
import os, re, time
from natsort import natsorted
import json
import shutil
import pandas as pd

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

    del all_papers

# ----------ADD AUTHORS' ID TO METADATA FILE------------------

# given the metadata file, check the authors' IDs associated with the papers' IDs
def MatchingMetadataReferences(metadata_split,metadata_splits_folder,PaperReferences_splits_folder,filteredReferences_folder):

    print('enter')
    t1 = time.time()

    num1 = re.findall(r'\d+', metadata_split)[0]  # the number of the metadata split
    with open(f'{metadata_splits_folder}/{metadata_split}', 'r') as bj:
        meta = json.load(bj)
    IDs_meta = [d['id'] for d in meta]
    print('open!')

    for file in natsorted(os.listdir(PaperReferences_splits_folder)) :

        linkfile = pd.read_csv(f'{PaperReferences_splits_folder}/{file}',dtype='str',sep=';')
        num2 = re.findall(r'\d+', file)[0]  # the number of the linkfile

        all_match = []
        with open(f'{filteredReferences_folder}/references{num1}{num2}.txt', 'w') as ww:
            match = set(IDs_meta).intersection(set(linkfile['citing']))
            if match :
                for i in match:
                    refs = linkfile[linkfile['citing']==i]['cited'].values[0].split(',')
                    ind = IDs_meta.index(i)
                    meta[ind]['references'] = refs
                    for j in refs:
                        if j not in all_match:
                            all_match.append(j)
                            ww.write(j + '\n')
        print(f'references{num1}{num2}.txt')

    # rewrite the metadata file with updated references field
    with open(f'{metadata_splits_folder}/{metadata_split}', 'w') as bj:
        json.dump(meta,bj,indent=2)
    print('done')

    t2 = time.time()
    print(f'done in {t2-t1}secs')

if __name__ == '__main__' :

    path_metadata_splits = ..
    path_linkPaperReferences_splits = ..
    path_references_filtered = ..

    # if output path exists remove the old files in the destination folder if it is not empty
    # else create the path
    if os.path.exists(path_references_filtered):
        if any(os.scandir(path_references_filtered)):
            shutil.rmtree(path_references_filtered)
            os.mkdir(path_references_filtered)
    else:
        os.mkdir(path_references_filtered)

    t1 = time.time()
    files = os.listdir(path_metadata_splits)
    nb_processes = 8

    try :
        pool = mp.Pool(nb_processes)
        # first treatment with static arguments
        temp = partial(MatchingMetadataReferences,metadata_splits_folder=path_metadata_splits,PaperReferences_splits_folder=path_linkPaperReferences_splits,filteredReferences_folder=path_references_filtered)
        # map only on the dynamic variables, here the files. Return a type of results of all processes
        pool.map(func=temp,iterable=files)
        pool.close()
        pool.join()
    except KeyboardInterrupt :
        # if this error is raised, kill all workers in the pool
        pool.terminate()

    t2 = time.time()
    print(t2-t1)

# merge the updated metadata files to get a global metadata file
MergeJSON(path_metadata_splits,'AImetadata_update.json')

# get the IDs of filtered papers by opening the updated filtered metadata files
IDs = []
for file in os.listdir(path_metadata_splits) :
    with open(f'{path_metadata_splits}/{file}','r') as bj :
        metadata = json.load(bj)
    IDs = IDs + [d['id'] for d in metadata]
#print(len(IDs))

# merge all IDs file into a single one, without those already in the original filtered database
allIDrefs = set()
for file in os.listdir(path_references_filtered) :
    f = open(f'{path_references_filtered}/{file}','r')
    # get all elements of all_ID + new elements in the new read file
    allIDrefs = allIDrefs.union(set(f.read().splitlines()))
    f.close()
# filter the IDs in order to avoid doubloons with already existing IDs in splits of 'AImetadata.json'
reduced_allIDrefs = allIDrefs.difference(IDs)
with open(f'{path_references_filtered}/all_references_filtered.txt','w') as ww :
    for i in reduced_allIDrefs :
        ww.write(i+'\n')

# find the associated metadata within 'Papers_simplified.txt'
def ProcessMatchIDMeta(Papers_split,dir_Papers_splits,IDs_candidates,outputdir) :

    print('enter')
    t1 = time.time()
    num = re.findall(r'\d+', Papers_split)[0]
    meta_split = pd.read_json(f"{dir_Papers_splits}/{Papers_split}",dtype='str') # warning to 'str'
    refs_meta = meta_split.loc[meta_split['id'].isin(IDs_candidates)]
    refs_meta['queryLevel'] = "1"
    print(len(refs_meta))
    refs_meta.to_json(f'{outputdir}/references{num}.json',orient='records',indent=2)
    del refs_meta
    t2 = time.time()
    print(f'done in {t2-t1}')

if __name__ == '__main__' :

    path_allpapers = ..
    files = os.listdir(path_allpapers)
    nb_processes = 8

    reduced_allIDrefs = open(f'{path_references_filtered}/all_references_filtered.txt', 'r').read().splitlines()

    try:
        pool = mp.Pool(nb_processes)
        # first treatment with static arguments
        temp = partial(MatchIDMeta,dir_Papers_splits=path_allpapers,IDs_candidates=reduced_allIDrefs,outputdir=path_metadata_splits)
        # map only on the dynamic variables, here the files. Return a type of results of all processes
        pool.map(func=temp, iterable=files)
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        # if this error is raised, kill all workers in the pool
        pool.terminate()

# get the abstracts ?
