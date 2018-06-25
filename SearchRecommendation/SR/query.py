#_*_ coding:utf-8 _*_
from SPARQLWrapper import  SPARQLWrapper, JSON
from SR.crawler import get_infor

#电影搜索与推荐
def get_content_list(search_txt):
    #电影搜索
    query_film_str = """
        PREFIX dbo:<http://dbpedia.org/ontology/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dct: <http://purl.org/dc/terms/>
        
        SELECT * WHERE{
            ?url rdf:type<http://dbpedia.org/ontology/Film>;
            rdfs:label ?label;
            foaf:name ?name;
            dbo:director ?director;
            dbo:wikiPageID ?wikiPageID;
            dbo:abstract ?abstract
            
            filter regex(str(?label),'""" + search_txt + "')}"
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query_film_str)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()

    # save searched text times
    sw_dict = {}
    f = open('VisualAnalysis/search_temp.txt', 'r')
    if f:
        a = f.read()
        sw_dict = eval(a)
    f.close()

    if search_txt in sw_dict:
        sw_dict[search_txt] = sw_dict[search_txt] + 1
    else:
        sw_dict[search_txt] = 1

    f = open('VisualAnalysis/search_temp.txt', 'w')
    f.write(str(sw_dict))
    f.close()



    table = []
    wikiPageIDs = []

    for item in result["results"]["bindings"]:
        Item = {}
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


        director = item["director"]["value"]
        director1 = director.split(' ')
        for token in director1:
            director2 = token.split('/')[-1]
        Item['director'] = director2


        Item['name'] = add_property(item,"name")
        #Item['writer'] = add_property(item,"writer")


        abstract = add_property(item,"abstract")
        strlen = len(abstract)
        if strlen >200:
            abstract = str(abstract)[0:200] + "..."
        Item['abstract'] = abstract



        #爬虫爬取的下面信息
        orter = get_infor(Item['label'])
        #Item['writer'] = orter['writer']
        Item['staring'] = orter['staring']
        Item['style'] = orter['style']
        Item['picture'] = orter['picture']


        table.append(Item)
# 电影推荐
    query_film_str1 = """
            PREFIX dbo:<http://dbpedia.org/ontology/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dct: <http://purl.org/dc/terms/>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>

            SELECT ?name ?film 
            WHERE
            {{
                ?film rdf:type dbo:Film .
                ?film rdfs:label ?name .
                
                
                ?film dbo:director dbr:{}.
                FILTER ((lang(?name) ="zh")&&(?name != '{}'@zh)) .
            }}
        """.format(director2,label)
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query_film_str1)
    sparql.setReturnFormat(JSON)
    result1 = sparql.query().convert()



    for item in result1["results"]["bindings"]:
        Film = {}
        if (str(language) != str("en") and str(language) != str("zh")):
            continue

        film_name = item["name"]["value"]
        Film['film_name'] = film_name

        if('film' in item):
            film0 = item["film"]["value"]
            film1 = film0.split(' ')
            for token in film1:
                film2 = token.split('/')[-1]
                film = film2
        Film['film_url'] = film
        table.append(Film)

    return table

#图书搜索与推荐
def get_content_book_list(search_txt):
    #图书搜索
    query_str = """
        PREFIX dbo:<http://dbpedia.org/ontology/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>

        SELECT * WHERE{
            ?url rdf:type<http://dbpedia.org/ontology/Book>;
            rdfs:label ?label;
            foaf:name ?name;
            dbo:wikiPageID ?wikiPageID;
            dbo:abstract ?abstract;
            
            dbo:literaryGenre ?genre
            OPTIONAL{?url dbo:writer ?writer}
            filter regex((str(?label)),'""" + search_txt + "')}"
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query_str)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()

    table = []
    wikiPageIDs = []

    author2 = ' '
    label = ' '
    for item in result["results"]["bindings"]:
        Item = {}
        language = item["abstract"]["xml:lang"]
        if (str(language) != str("en") and str(language) != str("zh")):
            continue
        # 同一条检索信息结果只显示一次
        wikiPageID = item["wikiPageID"]["value"]
        if (wikiPageID not in wikiPageIDs):
            wikiPageIDs.append(wikiPageID)
        else:
            continue
        url = item["url"]["value"]
        Item['url'] = url

        label = item["label"]["value"]
        Item['label'] = label

        #author = item["author"]["value"]
        #author1 = author.split(' ')
        #for token in author1:
         #   author2 = token.split('/')[-1]
        #Item['author'] = author2


        Item['name'] = add_property(item, "name")
        Item['writer'] = add_property(item, "writer")

        abstract = add_property(item, "abstract")
        strlen = len(abstract)
        if strlen > 200:
            abstract = str(abstract)[0:200] + "..."
        Item['abstract'] = abstract

        # 爬虫爬取的下面信息
        orter = get_infor(Item['label'])
        Item['writer'] = orter['writer']
        Item['style'] = orter['style']
        Item['picture'] = orter['picture']
        author2 = Item['writer']

        table.append(Item)



    #图书推荐
    query_film_str1 = """
                PREFIX dbo:<http://dbpedia.org/ontology/>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dct: <http://purl.org/dc/terms/>
                PREFIX dc: <http://purl.org/dc/elements/1.1/>

                SELECT ?name ?book 
                WHERE
                {{
                    ?book rdf:type dbo:Film .
                    ?book rdfs:label ?name .
                    ?book dbo:author dbr:{}.
                    FILTER ((lang(?name) ="zh")&&(?name != '{}'@zh)) .
                }}
            """.format(author2, label)
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query_film_str1)
    sparql.setReturnFormat(JSON)
    result1 = sparql.query().convert()


    for item in result1["results"]["bindings"]:
        Book = {}
        if (str(language) != str("en") and str(language) != str("zh")):
            continue

        book_name = item["name"]["value"]
        Book['book_name'] = book_name

        if ('book' in item):
            book0 = item["book"]["value"]
            book1 = book0.split(' ')
            for token in book1:
                book2 = token.split('/')[-1]
                book = book2
        Book['book_url'] = book
        table.append(Book)

    return table

#游戏搜索与推荐
def get_content_game_list(search_txt):
    #游戏搜索
    query_str = """
        PREFIX dbo:<http://dbpedia.org/ontology/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>

        SELECT ?label ?developer ?genre ?abstract
        WHERE{{
            ?game rdf:type dbo:VideoGame .
            ?game rdfs:label ?label .
            ?game foaf:name ?name .
            ?game dbo:developer ?developer .
            ?game dbo:wikiPageID ?wikiPageID .
            ?game dbo:abstract ?abstract .
            ?game dbo:genre ?genre
            FILTER ((lang(?name)="zh")&&(lang(?abstract)="zh")&&(regex(?name,'{}'))).
        }}LIMIT 3
        """.format(search_txt)
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query_str)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()

    table = []
    wikiPageIDs = []

    genre = ' '
    label = ' '
    for item in result["results"]["bindings"]:
        Item = {}
        language = item["abstract"]["xml:lang"]
        if (str(language) != str("en") and str(language) != str("zh")):
            continue
        # 同一条检索信息结果只显示一次
        wikiPageID = item["wikiPageID"]["value"]
        if (wikiPageID not in wikiPageIDs):
            wikiPageIDs.append(wikiPageID)
        else:
            continue
        url = item["url"]["value"]
        Item['url'] = url

        label = item["label"]["value"]
        Item['label'] = label

        Item['name'] = add_property(item, "name")
        #Item['writer'] = add_property(item, "writer")


        if ('genre' in item):
            genre = item["genre"]["value"].split('/')[-1]
        else:
            genre = 'NONE'
        Item['genre'] = genre



        abstract = add_property(item, "abstract")
        strlen = len(abstract)
        if strlen > 200:
            abstract = str(abstract)[0:200] + "..."
        Item['abstract'] = abstract

        # 爬虫爬取的下面信息
        orter = get_infor(Item['label'])
        #Item['writer'] = orter['writer']
        #Item['staring'] = orter['staring']
        Item['style'] = orter['style']
        Item['picture'] = orter['picture']

        table.append(Item)

    #游戏推荐
    query_film_str1 = """
                PREFIX dbo:<http://dbpedia.org/ontology/>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dct: <http://purl.org/dc/terms/>
                PREFIX dc: <http://purl.org/dc/elements/1.1/>

                SELECT ?name ?game 
                WHERE
                {{
                    ?film rdf:type dbo:VideoGame .
                    ?film rdfs:label ?name .
                    ?film dbo:genre dbr:{}.
                    FILTER ((lang(?name) ="zh")&&(?name != '{}'@zh)) .
                }}
            """.format(genre, label)
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query_film_str1)
    sparql.setReturnFormat(JSON)
    result1 = sparql.query().convert()


    for item in result1["results"]["bindings"]:
        Game = {}
        if (str(language) != str("en") and str(language) != str("zh")):
            continue

        game_name = item["name"]["value"]
        Game['game_name'] = game_name

        if ('game' in item):
            game0 = item["game"]["value"]
            game1 = game0.split(' ')
            for token in game1:
                game2 = token.split('/')[-1]
                game = game2
        Game['game_url'] = game
        table.append(Game)
    return table





def add_property(item,propertyname):
    try:
        property = item[propertyname]["value"]
    except KeyError:
        property = ""
    return property