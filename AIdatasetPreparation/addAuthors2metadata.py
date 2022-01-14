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

#----------ADD AUTHORS' ID TO METADATA FILE------------------

# given the metadata file, check the authors' IDs associated with the papers' IDs
def MatchingMetadataAuthors(metadata_split,metadata_splits_folder,PaperAuthor_dataframe,new_metadata_folder,filteredAuthor_folder) :

    num = re.findall(r'\d+', metadata_split)[0]  # the number of the metadata file
    with open(f'{metadata_splits_folder}/{metadata_split}', 'r') as bj :
        meta = json.load(bj)
    IDs_meta = [d['id'] for d in meta]

    with open(f'{filteredAuthor_folder}/authors{num}.txt','w') as ww:
        for i in IDs_meta :
            match = PaperAuthor_dataframe.loc[PaperAuthor_dataframe['paper'] == str(i)]
            if not match.empty :
                ind = IDs_meta.index(i)
                meta[ind]['authors'] = list(match['author'])[0].split(',')
                for j in list(match['author'])[0].split(',') :
                    ww.write(j + '\n')

    with open(f'{new_metadata_folder}/filtered{num}.json', 'w') as js:
        json.dump(meta, js, indent=2)

    print('done')

def MergeAuthorsFiles(dir) :


if __name__ == '__main__' :

    path_metadata_splits = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/AIfilter/metadata"
    path_linkPaperAuthors_splits = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/dataset_20200529/extracted/PaperAuthorAffiliations_simplified_splits"
    path_authors_splits = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/dataset_20200529/extracted/Authors_simplified_splits"
    new_path_metadata_splits = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/AIfilter/metadata_update"
    path_authors_filtered = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/AIfilter/FilteredAuthorsID_splits"

    # if output path exists remove the old files in the destination folder if it is not empty
    # else create the path
    if os.path.exists(new_path_metadata_splits):
        if any(os.scandir(new_path_metadata_splits)):
            shutil.rmtree(new_path_metadata_splits)
            os.mkdir(new_path_metadata_splits)
    else:
        os.mkdir(new_path_metadata_splits)

    if os.path.exists(path_authors_filtered):
        if any(os.scandir(path_authors_filtered)):
            shutil.rmtree(path_authors_filtered)
            os.mkdir(path_authors_filtered)
    else:
        os.mkdir(path_authors_filtered)

    files = natsorted(os.listdir(path_metadata_splits))
    nb_processes = 8

    for file in natsorted(os.listdir(path_linkPaperAuthors_splits)):

        t1 = time.time()

        PaperAuthors = pd.read_csv(f'{path_linkPaperAuthors_splits}/{file}',sep=';', dtype='str')
        print('open!')

        pool = mp.Pool(nb_processes)
        temp = partial(MatchingMetadataAuthors,metadata_splits_folder=path_metadata_splits,PaperAuthor_dataframe_split=PaperAuthors,new_metadata_folder=new_path_metadata_splits,filteredAuthor_folder=path_authors_filtered)  # first treatment with static arguments
        pool.map(func=temp,iterable=files)  # map only on the dynamic variables, here the files. Return a type of results of all processes
        pool.close()
        pool.join()

        del PaperAuthors

        t2 = time.time()
        print(t2-t1)