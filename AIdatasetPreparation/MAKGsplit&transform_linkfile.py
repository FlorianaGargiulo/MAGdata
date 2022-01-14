import os, shutil

# WARNING : APPLY CODES FROM "simplifyMAGKfiles.py" to have simplified .txt files

# ------------BIG LINKFILE SPLIT (transform .txt to another .txt)-----------------

# transform the file with two columns into a file containing lines like 'id_papers;id_author1,id_author2...'
# or 'id_papers;id_cited1,id_cited2...'
# filetype = {'paperauthors','paperreferences','paperdiscipline}
def ReadAssembleSplit(dir,input,output_dir,maxsize) :

    i = 0 # number of line
    j = 0 # counter for papers
    k = 0 # counter for created splits
    set_aff = []
    indices = 'citing;cited\n'
    with open(f'{dir}/{input}.txt','r') as f:
        for line in f :
            if i == 1 :
                l = line.split(';')
                current_id = l[0]  # very first paper ID
                current_assoc = f'{current_id};{l[1][:-1]},'
            elif i > 1 :
                l = line.split(';')
                paper_id = l[0]
                if paper_id == current_id :
                    current_assoc = current_assoc + str(l[1][:-1]) + ','
                else :
                    set_aff.append(current_assoc[:-1]+'\n') # to remove the last ',' and add breakline
                    current_id = paper_id
                    current_assoc = str(paper_id) + ';' + str(l[1][:-1]) + ','
                    j += 1
                if j > maxsize :
                    print(k)
                    with open(f'{output_dir}/{input}_{k}.txt','w') as ww:
                        ww.write(indices)
                        for h in set_aff :
                            ww.write(h)
                    set_aff = []
                    j = 0
                    k += 1
            i += 1

    # don't forget the very last set
    set_aff.append(current_assoc[:-1]+'\n')
    with open(f'{output_dir}/{input}_{k}.txt', 'w') as ww:
        ww.write(indices)
        for h in set_aff:
            ww.write(h)

# -------------EXECUTION FOR "PaperAffiliation_simplified.txt-------------------
dir = ..
input = 'PaperReferences_simplified'
output_dir = ..

# if output path exists remove the old files in the destination folder if it is not empty
# else create the path
if os.path.exists(output_dir):
    if any(os.scandir(output_dir)):
        shutil.rmtree(output_dir)
        os.mkdir(output_dir)
else:
    os.mkdir(output_dir)

ReadAssembleSplit(dir,input,output_dir,1000000)
