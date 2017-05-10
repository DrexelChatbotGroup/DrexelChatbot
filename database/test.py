from SPARQLWrapper import SPARQLWrapper, JSON

endpoint = "http://10.246.251.67:5820/chatbotDB/query/"
sparql = SPARQLWrapper(endpoint)
sparql.setQuery("""
    prefix cb: <http://drexelchatbot.com/rdf/>
    SELECT ?phone ?email 
    WHERE
    {
        ?s cb:name "Marcello Balduccini" .
        ?s cb:phone ?phone .
        ?s cb:email ?email .
    }
    """)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
bindings = results["results"]["bindings"]
res = {}
if bindings:
    bindings = bindings[0]
    for key in bindings:
        res[key] = bindings[key]["value"]
    
print(res)
'''
for result in results["results"]["bindings"]:
    print(result["label"]["value"])
    quit() 
'''
