from Bio import Entrez, Medline

#Initialisation
Entrez.api_key = "6156daa8c7104e81363c7b4373a4a458d708"
Entrez.email = "selma2468@gmail.com"

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
                        #mindate=,
                        maxdate= '2005/11/05')
record = Entrez.read(handle)
handle.close()
idlist = record["IdList"]
for i in idlist:
    if i == '16437530':
        idlist.remove(i)

print(idlist)

#downloading the corresponding MEDLINE records
handle = Entrez.efetch(db="pubmed",
                       id=idlist, rettype="medline", retmode="json")
records = Medline.parse(handle)
records = list(records)
output = []
tweede = []
for record in records:
    #if record[PMID] == '27631535':
        #records.remove(record)
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
