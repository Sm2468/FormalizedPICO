from Bio import Entrez, Medline

#Initialisation
Entrez.api_key = "example"
Entrez.email = "example@gmail.com"

TERM = input('input query: ')

handle = Entrez.egquery(term=TERM)
record = Entrez.read(handle)
for row in record["eGQueryResult"]:
    if row["DbName"]=="pubmed":
        print(row["Count"])

handle = Entrez.esearch(db="pubmed",
                        term=TERM,
                        retmax='30',
                        sort='relevance',
                        retmode='xml',
                        mindate= '2019/06/10')
                        #maxdate = )
record = Entrez.read(handle)
handle.close()
idlist = record["IdList"]
for i in idlist:
    if i == '16437530': #delete the PMID of the Systematic Review itself
        idlist.remove(i)
print(idlist)

#downloading the corresponding MEDLINE records
handle = Entrez.efetch(db="pubmed",
                       id=idlist, rettype="medline", retmode="json")
records = Medline.parse(handle)
records = list(records)
output = []

for record in records:
    print("Title:", record.get("TI", "?"))
    print("PMID:", record.get("PMID", "?"))
    if 'MH' in record:
        print("MeSH Terms:", record.get("MH","?"))
        output.append(record["MH"])
    else:
        print('no MeSH terms found')
    if 'AB' in record:
        print("Abstract:", record.get("AB", "?"))
    else:
        print('no abstract found')
    output.append(record["TI"])
    output.append(record["PMID"])
    print("")

with open('bp_results.txt', 'w') as f:
    for record in output:
        f.write("%s \n" % record)
