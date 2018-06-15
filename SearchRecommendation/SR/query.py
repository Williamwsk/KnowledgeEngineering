#_*_ coding:utf-8 _*_
from SPARQLWrapper import  SPARQLWrapper, JSON
from SR.crawler import get_infor

def get_content_list(search_txt):
    query_str = """
        PREFIX dbo:<http://dbpedia.org/ontology/>
        SELECT * WHERE{
            ?url rdf:type<http://dbpedia.org/ontology/Film>;
            rdfs:label ?label;
            foaf:name ?name;
            dbo:wikiPageID ?wikiPageID;
            dbo:abstract ?abstract
            OPTIONAL{?url dbo:writer ?writer}
            filter regex(str(?label),'""" + search_txt + "')}"
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query_str)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()

    table = []
    wikiPageIDs = []
    for item in result["results"]["bindings"]:
        Item ={}
        language = item["abstract"]["xml:lang"]
        if(str(language) != str("en") and str(language) != str("zh")):
            continue
        #同一条检索信息结果只显示一次
        wikiPageID = item["wikiPageID"]["value"]
        if(wikiPageID not in wikiPageIDs):
            wikiPageIDs.append(wikiPageID)
        else:
            continue
        url = item["url"]["value"]
        Item['url'] = url


        label = item["label"]["value"]
        Item['label'] = label


        Item['name'] = add_property(item,"name")
        item['writer'] = add_property(item,"writer")


        abstract = add_property(item,"abstract")
        strlen = len(abstract)
        if strlen >200:
            abstract = str(abstract)[0:200] + "..."
        Item['abstract'] = abstract



        #爬虫爬取的下面信息
        orter = get_infor(Item['label'])
        Item['writer'] = orter['writer']
        Item['staring'] = orter['staring']
        Item['style'] = orter['style']
        Item['picture'] = orter['picture']


        table.append(Item)
    return table





def add_property(item,propertyname):
    try:
        property = item[propertyname]["value"]
    except KeyError:
        property = ""
    return property