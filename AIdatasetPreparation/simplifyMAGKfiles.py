import pandas as pd

# ---------SIMPLIFY 'Papers.nt'-----------
path_papers = r"/media/sylvain/TOSHIBA EXT/microsoft_academic_RDF20200529/extracted/"
monster = path_papers + 'Papers.nt'
outFile = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/dataset_20200529/extracted/Papers_simplified.txt"
ww = open(outFile,'w')

c1='http://ma-graph.org/property/'
c2='http://prismstandard.org/namespaces/1.2/basic/'
c3='http://prismstandard.org/namespaces/basic/2.0/'
c4='http://purl.org/dc/terms/'
c5='http://purl.org/spar/datacite/'

f1='^^<http://www.w3.org/2001/XMLSchema#date> .'
f2='^^<http://www.w3.org/2001/XMLSchema#integer> .'
f3='^^<http://www.w3.org/2001/XMLSchema#string> .'

repl2='<http://ma-graph.org/entity/'

def replaTot(text):
    t2=text.replace(c1,'').replace(c2,'').replace(c3,'').replace(c4,'').replace(c5,'').replace(f1,'').replace(f2,'').replace(f3,'').replace(repl2,'').replace('> .','').replace('>',';').replace('<','')
    return t2

for line in open(monster):
    ww.write(replaTot(line))
ww.close()

# ---------SIMPLIFY 'Journals.nt'-----------

path_journals = r"/media/sylvain/TOSHIBA EXT/microsoft_academic_RDF20200529/extracted/"
monster = path_journals + 'Journals.nt'
outFile = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/dataset_20200529/extracted/Journals_simplified.txt"
ww = open(outFile,'w')

c1='http://ma-graph.org/property/'
c2='http://xmlns.com/foaf/0.1/'
c3='http://id.loc.gov/vocabulary/identifiers/'
c4='http://purl.org/dc/terms/'

f1='^^<http://www.w3.org/2001/XMLSchema#date> .'
f2='^^<http://www.w3.org/2001/XMLSchema#integer> .'
f3='^^<http://www.w3.org/2001/XMLSchema#string> .'

repl1='<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://ma-graph.org/class/'
repl2='<http://ma-graph.org/entity/'

def replaTot(text):
    t2=text.replace(c1,'').replace(c2,'').replace(c3,'').replace(c4,'').replace(f1,'').replace(f2,'').replace(f3,'').replace(repl1,'type;').replace(repl2,'').replace('> .','').replace('> ',';').replace('<','')
    return t2

for line in open(monster):
    ww.write(replaTot(line))
ww.close()

# ---------SIMPLIFY 'FieldsOfStudy.nt'-----------

path_fos = r"/media/sylvain/TOSHIBA EXT/microsoft_academic_RDF20200529/extracted/"
monster = path_fos + 'FieldsOfStudy.nt'
outFile = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/dataset_20200529/extracted/FieldsOfStudy_simplified.txt"
ww = open(outFile,'w')

c1='http://ma-graph.org/property/'
c2='http://xmlns.com/foaf/0.1/'
c3='http://purl.org/dc/terms/'

f1='^^<http://www.w3.org/2001/XMLSchema#date> .'
f2='^^<http://www.w3.org/2001/XMLSchema#integer> .'
f3='^^<http://www.w3.org/2001/XMLSchema#string> .'

repl1='<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://ma-graph.org/class/'
repl2='<http://ma-graph.org/entity/'

def replaTot(text):
    t2=text.replace(c1,'').replace(c2,'').replace(c3,'').replace(f1,'').replace(f2,'').replace(f3,'').replace(repl1,'type;').replace(repl2,'').replace('> .','').replace('> ',';').replace('<','')
    return t2

for line in open(monster):
    ww.write(replaTot(line))
ww.close()

# ---------SIMPLIFY 'Affiliations.nt'-----------

path_aff = r"/media/sylvain/TOSHIBA EXT/microsoft_academic_RDF20200529/extracted/"
monster = path_aff + 'Affiliations.nt'
outFile = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/dataset_20200529/extracted/Affiliations_simplified.txt"
ww = open(outFile,'w')

c1='http://ma-graph.org/property/'
c2='http://xmlns.com/foaf/0.1/'
c3='http://purl.org/dc/terms/'
c4='http://www.w3.org/2000/01/rdf-schema#seeAlso'
c5='http://www.w3.org/2002/07/owl#sameAs'

f1='^^<http://www.w3.org/2001/XMLSchema#date> .'
f2='^^<http://www.w3.org/2001/XMLSchema#integer> .'
f3='^^<http://www.w3.org/2001/XMLSchema#string> .'

repl1='<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://ma-graph.org/class/'
repl2='<http://ma-graph.org/entity/'

def replaTot(text):
    t2=text.replace(c1,'').replace(c2,'').replace(c3,'').replace(c4,'seeAlso').replace(c5,'owl#sameAs').replace(f1,'').replace(f2,'').replace(f3,'').replace(repl1,'type;').replace(repl2,'').replace('> .','').replace('> ',';').replace('<','')
    return t2

for line in open(monster):
    ww.write(replaTot(line))
ww.close()

# ---------SIMPLIFY 'PaperAuthorAffiliations.nt'-----------
repla1='<http://ma-graph.org/entity/'
repla2='> <http://purl.org/dc/terms/creator> '

infile = r"/media/sylvain/TOSHIBA EXT/microsoft_academic_RDF20200529/extracted/PaperAuthorAffiliations.nt"
# infile = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/dataset_20200529/samples/PaperAuthorAffiliations_sample.nt"
outFile = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/dataset_20200529/extracted/PaperAuthorAffiliations_simplified.txt"
ww = open(outFile,'w')
ww.write('paper;author\n')
for line in open(infile):
    ww.write(line.replace(repla1,'').replace(repla2,';').replace('> .',''))
ww.close()

# ---------SIMPLIFY 'Authors.nt'-----------
begin='<http://ma-graph.org/entity/'
end_string='"^^<http://www.w3.org/2001/XMLSchema#string> .'
end_int = '"^^<http://www.w3.org/2001/XMLSchema#integer> .'
end_date = '"^^<http://www.w3.org/2001/XMLSchema#date> .'

t1='> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://ma-graph.org/class/Author> .'
t2='> <http://www.w3.org/ns/org#memberOf> '
t3='> <http://xmlns.com/foaf/0.1/name> "'
t4='> <http://ma-graph.org/property/'
t5='> <http://purl.org/dc/terms/created> "'

infile = r"/media/sylvain/TOSHIBA EXT/microsoft_academic_RDF20200529/extracted/Authors.nt"
#infile = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/dataset_20200529/samples/Authors_sample.nt"
outFile = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/dataset_20200529/extracted/Authors_simplified.txt"
ww = open(outFile,'w')
for line in open(infile):
    if t1 in line:
        ww.write(line.replace(begin, '').replace(t1, ';type;Author'))
    elif t2 in line:
        ww.write(line.replace(begin, '').replace(t2, ';affiliation;').replace('> .', ''))
    elif t3 in line:
        ww.write(line.replace(begin, '').replace(t3, ';name;').replace(end_string, ''))
    else:
        if end_int in line:
            ww.write(line.replace(begin, '').replace(t4, ';').replace(end_int, '').replace('> "', ';'))
        elif end_string in line:
            ww.write(line.replace(begin, '').replace(t4, ';').replace(end_string, '').replace('> "', ';'))
        elif end_date in line:
            ww.write(line.replace(begin, '').replace(t5, ';date;').replace(end_date, '').replace('> "', ';'))
ww.close()

# ---------SIMPLIFY 'PaperReferences.nt'-----------

infile = r"/media/sylvain/TOSHIBA EXT/microsoft_academic_RDF20200529/extracted/PaperReferences.nt"
#infile = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/dataset_20200529/samples/PaperReferences_sample.nt"
outfile = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/dataset_20200529/extracted/PaperReferences_simplified.txt"

i = 0
chunksize = 10 ** 6
for chunk in pd.read_csv(infile, chunksize=chunksize, names=['citing', 'cited'],sep=' <http://purl.org/spar/cito/cites> ',engine='python'):
    chunk['citing']=chunk['citing'].apply(lambda x:x.replace('<http://ma-graph.org/entity/','').replace('>',''))
    chunk['cited']=chunk['cited'].apply(lambda x:x.replace('<http://ma-graph.org/entity/','').replace('> .',''))
    if i==0:
        chunk.to_csv(outfile,index=False,sep=';')
    else:
        chunk.to_csv(outfile, mode='a', header=False,index=False,sep=';')
    i += 1

# ---------SIMPLIFY 'PaperFieldsOfStudy.nt'-----------

infile = r"/media/sylvain/TOSHIBA EXT/microsoft_academic_RDF20200529/extracted/PaperFieldsOfStudy.nt"
#infile = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/dataset_20200529/samples/PaperReferences_sample.nt"
outfile = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/dataset_20200529/extracted/PaperFieldsOfStudy_simplified.txt"

i = 0
chunksize = 10 ** 6
for chunk in pd.read_csv(infile, chunksize=chunksize, names=['paper', 'discipline'],sep=' <http://purl.org/spar/fabio/hasDiscipline> ',engine='python'):
    chunk['paper']=chunk['paper'].apply(lambda x:x.replace('<http://ma-graph.org/entity/','').replace('>',''))
    chunk['discipline']=chunk['discipline'].apply(lambda x:x.replace('<http://ma-graph.org/entity/','').replace('> .',''))
    if i==0:
        chunk.to_csv(outfile,index=False,sep=';')
    else:
        chunk.to_csv(outfile, mode='a', header=False,index=False,sep=';')
    i += 1

# ----------------DISAMBIGUATED FILES--------------------

# ---------SIMPLIFY 'Authors_disambiguated.nt'-----------
repla1='<https://makg.org/entity/'
repla2='^^<http://www.w3.org/2001/XMLSchema#string> .'
repla3='> <http://www.w3.org/ns/org#memberOf> <https://makg.org/entity/' # ;affiliation;

t1='> <http://xmlns.com/foaf/0.1/name> '
t2='<http://www.w3.org/ns/org#memberOf>'

infile = r"/media/sylvain/TOSHIBA EXT/microsoft_academic_RDF20200619/extracted/Authors_disambiguated.nt"
outFile = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/dataset_20200619/extracted/Authors_disambiguated_simplified.txt"
ww = open(outFile,'w')
for line in open(infile):
    if t1 in line:
        ww.write(line.replace(t1,';name;').replace(repla1,'').replace(repla2,''))
    if t2 in line:
        ww.write(line.replace(repla3,';affiliation;').replace(repla1,'').replace('> .',''))
ww.close()

# ---------SIMPLIFY 'PaperAuthorAffiliations_disambiguated.nt'-----------
repla1='> <http://purl.org/dc/terms/creator> <https://makg.org/entity/'
repla2='<https://makg.org/entity/'
repla3='> .'

infile = r"/media/sylvain/TOSHIBA EXT/microsoft_academic_RDF20200619/extracted/PaperAuthorAffiliations_disambiguated.nt"
outFile = r"/home/sylvain/DOCTORAT/DATA/microsoft_academic/dataset_20200619/extracted/PaperAuthorAffiliations_disambiguated_simplified.txt"
ww = open(outFile,'w')
for line in open(infile):
    ww.write(line.replace(repla1,';').replace(repla2,'').replace(repla3,''))
ww.close()