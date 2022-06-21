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


#FUNZIONA
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
            SELECT ?nature ?fDate ?rDate ?uic ?lat ?long
            WHERE {
                ?nature rdfs:subClassOf ns:Object .
                ?obj rdf:type ?nature .
                ?obj ns:foundDate ?fDate .
                ?obj ns:recoveredDate ?rDate . 
                ?obj ns:eStatoTrovato ?place .
                ?place ns:name ?name .
                ?place ns:codeUIC ?uic .
                ?place ns:latitude ?lat .
                ?place ns:longitude ?long .
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
            ?obj ns:eStatoTrovato ns:{place}.
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
            ?obj ns:eStatoTrovato ns:{place}.
            FILTER(?rDate = "nan")
    """
    condition_query3 = """
    }
    """
    res = graph.query(prefix + '\n' + condition_query1 + condition_query2 + condition_query3)
    l_elt = [[row.obj.split('#')[1], row.fDate.value, row.rDate.value] for row in res]
    return l_elt


def query_get_train_station_by_CAP(path: str, CAP: str):
    graph = start_queries(path)
    condition_query1 = """
        SELECT DISTINCT ?place ?CAP
        WHERE{
    """
    condition_query2 = f"""
            ?nature rdfs:subClassOf ns:Object .
            ?obj rdf:type ?nature .
            ?obj ns:eStatoTrovato ?place.
            ?place ns:CAP ?CAP.
            FILTER(?CAP = "{CAP}")
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
    for row in res:
        print(row)
    l_elt = [[row.nature.split('#')[1], row.fDate.value, row.nomeStazione.value] for row in res][0]
    return l_elt


def query_get_lat_long_name_train_station(path: str):
    graph = start_queries(path)
    condition_query = """
        SELECT ?lat ?long ?name ?city ?CAP ?dep
        WHERE{
            ?nature rdfs:subClassOf ns:Object .
            ?obj rdf:type ?nature .
            ?obj ns:eStatoTrovato ?place.
            ?place ns:latitude ?lat.
            ?place ns:longitude ?long.
            ?place ns:name ?name.
            ?place ns:city ?city.
            ?place ns:CAP ?CAP.
            ?place ns:department ?dep.
    }
    """
    res = graph.query(prefix + '\n' + condition_query)
    l_elt = [{'lat': row.lat.value, 'lon': row.long.value, 'popup': f'{row.name.value} - {row.city.value} {row.CAP.value} {row.dep.value}'} for row in res]
    return l_elt


def query_get_lost_object_with_conditions(path: str, nature: str, CAP: str, hasRecoveredDate: str):
    graph = start_queries(path)
    condition_query1 = """
    SELECT ?type ?fDate ?rDate ?CAP ?lat ?long ?city ?name
    WHERE {
    """
    condition_query2 = f"""
        ns:{nature} rdfs:subClassOf ns:Object . 
        ?obj rdf:type ns:{nature}.
        ?obj ns:foundDate ?fDate.
        ?obj ns:recoveredDate ?rDate.
        ?obj ns:typeObject ?type.
    """

    if hasRecoveredDate == "Oui":
        condition_query_optional = f"""
            FILTER(?rDate != "nan")
            ?obj ns:eStatoTrovato ?place.
            ?place ns:CAP ?CAP.
        """
    else:
        condition_query_optional = f"""
            FILTER(?rDate = "nan")
            ?obj ns:eStatoTrovato ?place.
            ?place ns:CAP ?CAP.
        """

    if CAP != 'CAP':
        condition_query_optional2 = f'    FILTER(?CAP = "{CAP}")\n'
    else:
        condition_query_optional2 = ''

    condition_query3 = f"""
        ?place ns:latitude ?lat.
        ?place ns:longitude ?long.
        ?place ns:city ?city.
    """
    condition_query4 = """
    }
    ORDER BY DESC(?fDate)
    """
    res = graph.query(prefix + '\n' + condition_query1 + condition_query2 + condition_query_optional + condition_query_optional2 + condition_query3 + condition_query4)
    # print(prefix + '\n' + condition_query1 + condition_query2 + condition_query_optional + condition_query_optional2 + condition_query3 + condition_query4)
    l_elt = [[nature, row.type.value, row.fDate.value, row.rDate.value, row.CAP.value, row.lat.value, row.long.value, row.city.value] for row in res]
    df = convert_list_queries_to_df(l_queries=l_elt,
                                    l_cols=['Nature of the Object', 'Type of the Object', 'Found Date', 'Recovered Date',
                                            'CAP of the Station', 'Latitude', 'longitude', 'City of the Station'])
    return df


def query_get_all_lost_object_with_conditions(path: str, CAP: str, hasRecoveredDate: str):
    graph = start_queries(path)
    condition_query1 = """
    SELECT ?nature ?type ?fDate ?rDate ?CAP ?lat ?long ?city ?name
    WHERE {
    """
    condition_query2 = f"""
        ?nature rdfs:subClassOf ns:Object .
        ?obj rdf:type ?nature.
        ?obj ns:foundDate ?fDate.
        ?obj ns:recoveredDate ?rDate.
        ?obj ns:typeObject ?type.
    """

    if hasRecoveredDate == "Oui":
        condition_query_optional = f"""
            FILTER(?rDate != "nan")
            ?obj ns:eStatoTrovato ?place.
            ?place ns:CAP ?CAP.
        """
    else:
        condition_query_optional = f"""
            FILTER(?rDate = "nan")
            ?obj ns:eStatoTrovato ?place.
            ?place ns:name ?name.
            ?place ns:CAP ?CAP.
        """

    if CAP != 'CAP':
        condition_query_optional2 = f'    FILTER(?CAP = "{CAP}")\n'
    else:
        condition_query_optional2 = ''

    condition_query3 = f"""
        ?place ns:latitude ?lat.
        ?place ns:longitude ?long.
        ?place ns:city ?city.
    """
    condition_query4 = """
    }
    ORDER BY DESC(?fDate)
    """
    res = graph.query(prefix + '\n' + condition_query1 + condition_query2 + condition_query_optional + condition_query_optional2 + condition_query3 + condition_query4)
    # print(prefix + '\n' + condition_query1 + condition_query2 + condition_query_optional + condition_query_optional2 + condition_query3 + condition_query4)
    l_elt = [[row.nature.split('#')[1], row.type.value, row.fDate.value, row.rDate.value, row.CAP.value, row.lat.value, row.long.value, row.city.value] for row in res]
    df = convert_list_queries_to_df(l_queries=l_elt,
                                    l_cols=['Nature of the Object', 'Type of the Object', 'Found Date', 'Recovered Date',
                                            'CAP of the Station', 'Latitude', 'longitude', 'City of the Station'])
    return df


if __name__ == "__main__":
    path_owl_file = './data/output_context.owl'

    #q = query_get_lost_object_with_conditions(path_owl_file, 'Carte_d_identite_passeport_permis_de_conduire', 'CAP', 'Oui')
    # q = query_get_lost_object_with_conditions(path_owl_file, 'Carte_d_identite_passeport_permis_de_conduire', '75015', 'Oui')
    # q = query_get_lost_object_with_conditions(path_owl_file, 'All', 'CAP', 'Oui')
    # q = query_get_lost_object_with_conditions(path_owl_file, 'All', '75015', 'Oui')
    # q = query_get_all_nature(path_owl_file)
    # q = query_get_last_date_of_lost_objects(path_owl_file)
    # q = query_get_lat_long_name_train_station(path_owl_file)
    print(q)
