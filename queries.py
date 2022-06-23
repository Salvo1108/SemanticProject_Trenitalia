import rdflib
# from utils import syntax_to_owl
from utils import convert_list_queries_to_df


prefix = """
        PREFIX ns: <http://www.semanticweb.org/amivid/ontologies/2022/2/untitled-ontology-38#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX tg: <http://www.turnguard.com/functions#>
    """


def start_queries(ontology: str):
    g = rdflib.graph.ConjunctiveGraph()
    g.parse(ontology)
    return g


def query_get_all_nature(path: str):
    graph = start_queries(path)
    nature_query = """
        SELECT DISTINCT ?sub
        WHERE {
            ?sub rdfs:subClassOf ns:Object .
        }
    """
    res = graph.query(prefix + '\n' + nature_query)
    l_elt = [row.sub.split('#')[1] for row in res]
    l_elt.append('All')
    return l_elt


def query_get_instances(path: str):
    graph = start_queries(path)
    condition_query = """
            SELECT ?nature ?fDate ?rDate ?codice ?lat ?long
            WHERE {
                ?nature rdfs:subClassOf ns:Object .
                ?obj rdf:type ?nature .
                ?obj ns:foundDate ?fDate .
                ?obj ns:recoveredDate ?rDate . 
                ?obj ns:hasBeenFoundHere ?place .
                ?place ns:nomeStazione ?nomeStazione .
                ?place ns:codice ?codice .
                ?place ns:latitudine ?lat .
                ?place ns:longitudine ?long .
            }
    """
    res = graph.query(prefix + '\n' + condition_query)
    l_elt = [[row.nature.split('#')[1], row.fDate.value, row.rDate.value, row.uic.value,
              float(row.lat.value), float(row.long.value)] for row in res]
    return l_elt


def query_condition_rdate_not_nan(path: str, nature: str, place: str):
    graph = start_queries(path)
    condition_query1 = """
        SELECT ?obj ?fDate ?rDate
        WHERE{
    """
    condition_query2 = f"""
            ?obj rdf:type ns:{nature}.
            ?obj ns:foundDate ?fDate. 
            ?obj ns:recoveredDate ?rDate. 
            ?obj ns:hasBeenFoundHere ns:{place}.
            FILTER(?rDate != "nan")
    """
    condition_query3 = """
    }
    """
    res = graph.query(prefix + '\n' + condition_query1 + condition_query2 + condition_query3)
    l_elt = [[row.obj('#')[1], row.fDate.value, row.rDate.value] for row in res]
    return l_elt


def query_condition_rdate_nan(path: str, nature: str, place: str):
    graph = start_queries(path)
    condition_query1 = """
        SELECT ?obj ?fDate ?rDate
        WHERE{
    """
    condition_query2 = f"""
            ?obj rdf:type ?{nature}.
            ?obj ns:foundDate ?fDate. 
            ?obj ns:recoveredDate ?rDate. 
            ?obj ns:hasBeenFoundHere ns:{place}.
            FILTER(?rDate = "nan")
    """
    condition_query3 = """
    }
    """
    res = graph.query(prefix + '\n' + condition_query1 + condition_query2 + condition_query3)
    l_elt = [[row.obj.split('#')[1], row.fDate.value, row.rDate.value] for row in res]
    return l_elt


def query_get_train_station_by_Regione(path: str, regione: str):
    graph = start_queries(path)
    condition_query1 = """
        SELECT DISTINCT ?place ?regione
        WHERE{
    """
    condition_query2 = f"""
            ?nature rdfs:subClassOf ns:Object .
            ?obj rdf:type ?nature .
            ?obj ns:hasBeenFoundHere ?place.
            ?place ns:regione ?regione.
            FILTER(?regione = "{regione}")
    """
    condition_query3 = """
    }
    """
    res = graph.query(prefix + '\n' + condition_query1 + condition_query2 + condition_query3)
    elt = [row.place.split('#')[1] for row in res]
    return ''.join(elt)


def query_get_last_date_of_lost_objects(path: str):
    graph = start_queries(path)
    condition_query = """
        SELECT ?nature ?fDate ?nomeStazione
        WHERE{
            ?nature rdfs:subClassOf ns:Object .
            ?obj rdf:type ?nature .
            ?obj ns:foundDate ?fDate.
            ?obj ns:hasBeenFoundHere ?place.
            ?place ns:nomeStazione ?nomeStazione.
    }
    ORDER BY DESC(?fDate)
    """
    res = graph.query(prefix + '\n' + condition_query)
    l_elt = [[row.nature.split('#')[1], row.fDate.value, row.nomeStazione.value] for row in res][0]
    return l_elt


def query_get_lat_long_name_train_station(path: str):
    graph = start_queries(path)
    condition_query = """
        SELECT ?lat ?long ?nomeStazione ?citta ?regione ?codiceRegione
        WHERE{
            ?nature rdfs:subClassOf ns:Object .
            ?obj rdf:type ?nature .
            ?obj ns:hasBeenFoundHere ?place.
            ?place ns:latitudine ?lat.
            ?place ns:longitudine ?long.
            ?place ns:nomeStazione ?nomeStazione.
            ?place ns:citta ?citta.
            ?place ns:regione ?regione.
            ?place ns:codiceRegione ?codiceRegione.
    }
    """
    res = graph.query(prefix + '\n' + condition_query)
    l_elt = [{'lat': row.lat.value, 'lon': row.long.value, 'popup': f'{row.nomeStazione.value} - {row.codiceRegione.value}'} for row in res]
    return l_elt


def query_get_lost_object_with_conditions(path: str, nature: str, regione: str, hasRecoveredDate: str):
    graph = start_queries(path)
    condition_query1 = """
    SELECT ?type ?fDate ?rDate ?regione ?lat ?long ?citta ?nomeStazione
    WHERE {
    """
    condition_query2 = f"""
        ns:{nature} rdfs:subClassOf ns:Object . 
        ?obj rdf:type ns:{nature}.
        ?obj ns:foundDate ?fDate.
        ?obj ns:recoveredDate ?rDate.
        ?obj ns:typeObject ?type.
    """

    if hasRecoveredDate == "Si":
        condition_query_optional = f"""
            FILTER(?rDate != "nan")
            ?obj ns:hasBeenFoundHere ?place.
            ?place ns:regione ?regione.
        """
    else:
        condition_query_optional = f"""
            FILTER(?rDate = "nan")
            ?obj ns:hasBeenFoundHere ?place.
            ?place ns:regione ?regione.
        """

    if regione != 'regione':
        condition_query_optional2 = f'    FILTER(?regione = "{regione}")\n'
    else:
        condition_query_optional2 = ''

    condition_query3 = f"""
        ?place ns:latitudine ?lat.
        ?place ns:longitudine ?long.
        ?place ns:citta ?citta.
    """
    condition_query4 = """
    }
    ORDER BY DESC(?fDate)
    """
    res = graph.query(prefix + '\n' + condition_query1 + condition_query2 + condition_query_optional + condition_query_optional2 + condition_query3 + condition_query4)
    # print(prefix + '\n' + condition_query1 + condition_query2 + condition_query_optional + condition_query_optional2 + condition_query3 + condition_query4)
    l_elt = [[nature, row.type.value, row.fDate.value, row.rDate.value, row.regione.value, row.lat.value, row.long.value, row.citta.value] for row in res]
    df = convert_list_queries_to_df(l_queries=l_elt,
                                    l_cols=['Oggetto', 'Tipo', 'Trovato', 'Consegnato',
                                            'Regione', 'Latitudine', 'Longitudine', 'Città'])
    return df


def query_get_all_lost_object_with_conditions(path: str, regione: str, hasRecoveredDate: str):
    graph = start_queries(path)
    condition_query1 = """
    SELECT ?nature ?type ?fDate ?rDate ?regione ?lat ?long ?citta ?nomeStazione
    WHERE {
    """
    condition_query2 = f"""
        ?nature rdfs:subClassOf ns:Object .
        ?obj rdf:type ?nature.
        ?obj ns:foundDate ?fDate.
        ?obj ns:recoveredDate ?rDate.
        ?obj ns:typeObject ?type.
    """

    if hasRecoveredDate == "Si":
        condition_query_optional = f"""
            FILTER(?rDate != "nan")
            ?obj ns:hasBeenFoundHere ?place.
            ?place ns:regione ?regione.
        """
    else:
        condition_query_optional = f"""
            FILTER(?rDate = "nan")
            ?obj ns:hasBeenFoundHere ?place.
            ?place ns:nomeStazione ?nomeStazione.
            ?place ns:regione ?regione.
        """

    if regione != 'regione':
        condition_query_optional2 = f'    FILTER(?regione = "{regione}")\n'
    else:
        condition_query_optional2 = ''

    condition_query3 = f"""
        ?place ns:latitudine ?lat.
        ?place ns:longitudine ?long.
        ?place ns:citta ?citta.
    """
    condition_query4 = """
    }
    ORDER BY DESC(?fDate)
    """
    res = graph.query(prefix + '\n' + condition_query1 + condition_query2 + condition_query_optional + condition_query_optional2 + condition_query3 + condition_query4)
    #print(prefix + '\n' + condition_query1 + condition_query2 + condition_query_optional + condition_query_optional2 + condition_query3 + condition_query4)
    l_elt = [[row.nature.split('#')[1], row.type.value, row.fDate.value, row.rDate.value, row.regione.value, row.lat.value, row.long.value, row.citta.value] for row in res]
    df = convert_list_queries_to_df(l_queries=l_elt,
                                    l_cols=['Oggetto', 'Tipo', 'Trovato', 'Consegnato',
                                            'Regione', 'Latitudine', 'Longitudine', 'Città'])
    return df


def query_get_number_filterobject_most_lost(path: str):
    graph = start_queries(path)
    condition_query1 = """
        SELECT DISTINCT ?oggetto ?place (COUNT(?oggetto) as ?total)
        WHERE {
            ?obj ns:typeObject ?oggetto .
            ?obj ns:hasBeenFoundHere ?place .
            FILTER(?oggetto = "Bagagli: borse, valigie, cartelle")
            }
        GROUP BY ?place
        ORDER BY DESC(?total)
    """
    res = graph.query(prefix + '\n' + condition_query1)
    elt = [[row.place.split('#')[1], row.total.value] for row in res]
    return elt

def query_get_number_object_station(path: str):
    graph = start_queries(path)
    condition_query1 = """
        SELECT DISTINCT ?place ?nature (COUNT(?nature) as ?total)
        WHERE {
            ?obj rdf:type ?nature.
            ?obj ns:hasBeenFoundHere ?place .
            }
        GROUP BY ?nature
    """
    res = graph.query(prefix + '\n' + condition_query1)
    elt = [[row.place.split('#')[1],row.nature.split('#')[1], row.total.value] for row in res]
    df = convert_list_queries_to_df(l_queries=elt,
                                    l_cols=['Stazione', 'Oggetto', 'Numero di volte perso'])

    return df

def query_get_number_object_lost(path: str):
    graph = start_queries(path)
    condition_query1 = """
        SELECT DISTINCT ?oggetto (COUNT(?oggetto) as ?total)
        WHERE {
            ?obj ns:typeObject ?oggetto .
            }
        GROUP BY  ?oggetto
        ORDER BY DESC(?total)
    """
    res = graph.query(prefix + '\n' + condition_query1)
    elt = [[row.total.value,row.oggetto.value] for row in res]
    df = convert_list_queries_to_df(l_queries=elt,
                                    l_cols=['Numero di Oggetti Persi', 'Tipo'])
    return df

if __name__ == "__main__":
    path_owl_file = './data/output_context.owl'
    print(query_get_number_object_station(path_owl_file))



