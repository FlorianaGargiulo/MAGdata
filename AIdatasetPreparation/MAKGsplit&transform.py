import os, shutil, time
import json

# WARNING : APPLY CODES FROM "simplifyMAGKfiles.py" to have simplified .txt files
# ------------BIG FILE SPLIT (transform .txt to .json)-----------------

# transform a list of lines associated with the same ID in the file into a dictionary
# filetype = {'papers',authors','journals','fos','affiliations'...}
def list2dict(u,filetype) :
    ind = u[0].split(';')[0]
    d = {'id': ind}  # initiate a vector of many field
    # WARNING : some lines are divided in two or more lines because of '\n'
    r = []
    for i in reversed(range(len(u))):
        if ind not in u[i] :
            u[i-1] = u[i-1] + u[i] # append to the previous line until reaching the line containing 'ind', ie. the main one
            r.append(i) # append the index of the incomplete lines
    for i in r:
        u.pop(i) # remove all incomplete lines
    for k in u : # process each saved line in u
        l = k.split(';')  # let blank spaces for article's field not written with latin alphabet
        if len(l) > 3:
            repl = ';'.join(l[2:])
            while len(l) > 2 :
                l.pop()
            l.append(repl)
        #print(l)
        if filetype == 'papers' :
            key = l[1][1:]
            if 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' in key:
                d['type'] = l[-1].split('/')[-1][:-1]  # '\n' is a single character
            elif key == 'doi':
                d[key] = l[-1][1:-2]  # drop out '\n"' in strings
            else:
                d[key] = l[-1][2:-2] # drop out '\n"' in strings
        elif filetype == 'authors':
            key = l[1]
            d[key] = l[-1][:-1] # drop out '\n' in strings
        else:
            key = l[1]
            d[key] = l[-1][1:-2] # drop out '\n' in strings
    return d

# create a new folder
# read .txt file (enter filetype accorded to above)
# transform sets of lines into dictionaries
# save it into multiple .json files into the new folder
def SplitTXT2MULTIJSON(dir,input_file,filetype,maxsize) :

    # if output path exists remove the old files in the destination folder if it is not empty
    # else create the path
    output_path = f'{dir}/{input_file}_splits'
    if os.path.exists(output_path):
        if any(os.scandir(output_path)):
            shutil.rmtree(output_path)
            # time.sleep(10)
            os.mkdir(output_path)
    else:
        os.mkdir(output_path)

    if filetype == 'papers' :
        tag = 'http://ma-graph.org/class/Paper'
    elif filetype == 'authors' :
        tag = 'type;Author'
    elif filetype == 'journals' :
        tag = 'type;Journal'
    elif filetype == 'fos' :
        tag = 'type;FieldOfStudy'
    elif filetype == 'affiliations':
        tag = 'type;Affiliation'
    t1 = time.time()

    with open(f'{dir}/{input_file}.txt','r') as f:
        papers = []
        u = []
        i = 0
        for line in f:
            if tag not in line:
                u.append(line)
            elif len(u) != 0:
                papers.append(list2dict(u,filetype))
                u = []
            if len(papers) >= maxsize: # if file's size is bigger than 1Gb, close the file and open another one
                print(i)
                with open(f'{output_path}/{input_file}_{i}.json', 'w') as bj:
                    json.dump(papers, bj, indent=2)
                papers = []
                i += 1

    # don't forget to write in the file the very last lines
    papers.append(list2dict(u,filetype))
    with open(f'{output_path}/{input_file}_{i}.json', 'w') as bj:
        json.dump(papers, bj, indent=2)

    t2 = time.time()
    print(t2 - t1)

# ----------------EXECUTION----------------
dir = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/dataset_20200529/extracted/"
input = 'Affiliations_simplified'

SplitTXT2MULTIJSON(dir,input,'affiliations',1000000)

# ------------BIG LINKFILE SPLIT (transform .txt to another .txt)-----------------

# transform the file with two columns into a file containing lines like 'id_papers;id_author1,id_author2...'
# or 'id_papers;id_cited1,id_cited2...'
# filetype = {'paperauthors','paperreferences','paperdiscipline}
def ReadAssembleSplit(input,output_dir,maxsize) :

    i = 0 # number of line
    j = 0 # counter for papers
    k = 0 # counter for created splits
    current_id = '9'
    current_assoc = '9;' # very first paper ID
    set_aff = []
    with open(input,'r') as f:
        for line in f :
            if i == 0 :
                indices = line # already '\n' in it
                i = 1
            else :
                l = line.split(';')
                paper_id = l[0]
                if paper_id == current_id :
                    current_assoc = current_assoc + str(l[1][:-1]) + ','
                else :
                    set_aff.append(current_assoc[:-1]) # to remove the last ','
                    current_id = paper_id
                    current_assoc = str(paper_id) + ';' + str(l[1][:-1]) + ','
                    j += 1
                if j > maxsize :
                    print(k)
                    with open(f'{output_dir}/{input}_{k}.txt','w') as ww:
                        ww.write(indices)
                        for h in set_aff :
                            ww.write(h + '\n')
                    set_aff = []
                    j = 0
                    k += 1

    # don't forget the very last set
    set_aff.append(current_assoc[:-1])
    with open(f'{output_dir}/{input}_{k}.txt', 'w') as ww:
        ww.write(indices)
        for h in set_aff:
            ww.write(h + '\n')

# -------------EXECUTION FOR "PaperAffiliation_simplified.txt-------------------
dir = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/dataset_20200529/extracted"
input = 'PaperReferences_simplified_sample.txt'
output_dir = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/dataset_20200529/extracted/PaperReferences_simplified_splits"

# if output path exists remove the old files in the destination folder if it is not empty
# else create the path
if os.path.exists(output_dir):
    if any(os.scandir(output_dir)):
        shutil.rmtree(output_dir)
        os.mkdir(output_dir)
else:
    os.mkdir(output_dir)

ReadAssembleSplit(f'{dir}/{input}',output_dir,10000000)