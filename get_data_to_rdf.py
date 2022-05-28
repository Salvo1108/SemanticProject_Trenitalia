# coding: utf-8
import pandas as pd
import unidecode
from utils import syntax_to_owl
from tqdm import tqdm


def get_data_to_rdf_object(input_path_data: str, output_path_data: str):
    """ Get instances from a dynamic dataset and put it into a owl file in rdf/xml syntax """
    # The two links below can be used to get the data (the first one represents data from March 2022 and the
    # second one represents data from April 2020)
    # df_objects = pd.read_csv('https://ressources.data.sncf.com/explore/dataset/objets-trouves-restitution/download/?format=csv&refine.date=2022%2F03&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B', sep=';')
    df_objects = pd.read_csv('https://ressources.data.sncf.com/explore/dataset/objets-trouves-restitution/download/?format=csv&refine.date=2020%2F04&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B', sep=';')

    with open(input_path_data) as f:
        lines = f.readlines()

        for ind in tqdm(df_objects.index.tolist()):
            pos = len(lines) - lines.index("    // General axioms\n") + 4  # -36
            comment = f'    <!-- http://www.semanticweb.org/tinou/ontologies/2022/2/untitled-ontology-38#OBJ{ind + 1} -->\n'
            owl_first_line = f'    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/tinou/ontologies/2022/2/untitled-ontology-38#OBJ{ind + 1}">\n'
            elt_rdf_type = df_objects.loc[ind, "Type d\'objets"]
            elt_rdf_nature = df_objects.loc[ind, "Nature d\'objets"]
            rdf_nature = f'        <rdf:type rdf:resource="http://www.semanticweb.org/tinou/ontologies/2022/2/untitled-ontology-38#{syntax_to_owl(elt_rdf_nature)}"/>\n'
            rdf_property = f'        <hasBeenFoundHere rdf:resource="http://www.semanticweb.org/tinou/ontologies/2022/2/untitled-ontology-38#{(unidecode.unidecode(str(df_objects.loc[ind, "Gare"]))).replace(" ", "_")}"/>\n'
            rdf_type = f'        <typeObject>{unidecode.unidecode(str(elt_rdf_type))}</typeObject>\n'
            found_date = f'        <foundDate>{df_objects.loc[ind, "Date"]}</foundDate>\n'
            if df_objects.loc[ind, 'Date et heure de restitution'] != "nan":
                recovered_date = f'        <recoveredDate>{df_objects.loc[ind, "Date et heure de restitution"]}</recoveredDate>\n'
            else:
                pass
            owl_last_line = '    </owl:NamedIndividual>\n'
            back_slash_n = '    \n'

            lines.insert(-pos, comment)
            lines.insert(-pos, owl_first_line)
            lines.insert(-pos, rdf_type)
            lines.insert(-pos, rdf_nature)
            lines.insert(-pos, rdf_property)
            lines.insert(-pos, found_date)
            lines.insert(-pos, recovered_date)
            lines.insert(-pos, owl_last_line)
            lines.insert(-pos, back_slash_n)
            lines.insert(-pos, back_slash_n)
            lines.insert(-pos, back_slash_n)

        f = open(output_path_data, 'w')
        f.write("".join(lines))
        f.close()


def get_data_to_rdf_train_station(input_path_data: str, output_path_data: str):
    """ Get instances from a static dataset and put it into a owl file in rdf/xml syntax """
    df_place = pd.read_csv(
        'https://ressources.data.sncf.com/explore/dataset/referentiel-gares-voyageurs/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B',
        sep=';')
    df_place = df_place[
        ['Code UIC', 'Code postal', 'Commune', 'Département', 'Longitude', 'Latitude', 'Intitulé gare']]

    with open(input_path_data) as f:
        lines = f.readlines()

        for ind in tqdm(df_place.index.tolist()):
            pos = len(lines) - lines.index("    // General axioms\n") + 4  # -36
            comment = f'    <!-- http://www.semanticweb.org/tinou/ontologies/2022/2/untitled-ontology-38#{syntax_to_owl(unidecode.unidecode(df_place.loc[ind, "Intitulé gare"]))} -->\n'
            owl_first_line = f'    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/tinou/ontologies/2022/2/untitled-ontology-38#{syntax_to_owl(unidecode.unidecode(df_place.loc[ind, "Intitulé gare"]))}">\n'
            rdf_type = f'        <rdf:type rdf:resource="http://www.semanticweb.org/tinou/ontologies/2022/2/untitled-ontology-38#Train_station"/>\n'
            city = f'        <city>{unidecode.unidecode(str(df_place.loc[ind, "Commune"]))}</city>\n'
            codeUIC = f'        <codeUIC>{"00" + str(df_place.loc[ind, "Code UIC"])[:-2]}</codeUIC>\n'
            department = f'        <department>{unidecode.unidecode(str(df_place.loc[ind, "Département"]))}</department>\n'
            latitude = f'        <latitude rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">{df_place.loc[ind, "Latitude"]}</latitude>\n'
            longitude = f'        <longitude rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">{df_place.loc[ind, "Longitude"]}</longitude>\n'
            name = f'        <name>{unidecode.unidecode(str(df_place.loc[ind, "Intitulé gare"]))}</name>\n'
            zipcode = f'        <zipcode>{str(df_place.loc[ind, "Code postal"])[:-2]}</zipcode>\n'
            owl_last_line = '    </owl:NamedIndividual>\n'
            back_slash_n = '    \n'

            lines.insert(-pos, comment)
            lines.insert(-pos, owl_first_line)
            lines.insert(-pos, rdf_type)
            lines.insert(-pos, city)
            lines.insert(-pos, codeUIC)
            lines.insert(-pos, department)
            lines.insert(-pos, latitude)
            lines.insert(-pos, longitude)
            lines.insert(-pos, name)
            lines.insert(-pos, zipcode)
            lines.insert(-pos, owl_last_line)
            lines.insert(-pos, back_slash_n)
            lines.insert(-pos, back_slash_n)
            lines.insert(-pos, back_slash_n)

    f = open(output_path_data, 'w')
    f.write("".join(lines))
    f.close()


if __name__ == '__main__':
    file_rdf = './data/context.owl'
    file_output = './data/train_station_context.owl'
    get_data_to_rdf_train_station(file_rdf, file_output)
    # get_data_to_rdf_object(file_output, './data/output_context.owl')
