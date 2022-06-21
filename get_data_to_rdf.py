# coding: utf-8
import pandas as pd
import unidecode
from utils import syntax_to_owl
from tqdm import tqdm


def get_data_to_rdf_object(input_path_data: str, output_path_data: str):
    """ Get instances from a dynamic dataset and put it into a owl file in rdf/xml syntax """
    df_objects = pd.read_csv('../OggettiSmarritiTrenitalia.csv', sep=';')

    with open(input_path_data) as f:
        lines = f.readlines()

        for ind in tqdm(df_objects.index.tolist()):
            pos = len(lines) - lines.index("    // General axioms\n") + 4  # -36
            comment = f'    <!-- http://www.semanticweb.org/amivid/ontologies/2022/2/untitled-ontology-38#OBJ{ind + 1} -->\n'
            owl_first_line = f'    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/amivid/ontologies/2022/2/untitled-ontology-38#OBJ{ind + 1}">\n'
            elt_rdf_type = df_objects.loc[ind, "Oggetto"]
            elt_rdf_nature = df_objects.loc[ind, "Categoria"]
            rdf_nature = f'        <rdf:type rdf:resource="http://www.semanticweb.org/amivid/ontologies/2022/2/untitled-ontology-38#{syntax_to_owl(elt_rdf_nature)}"/>\n'
            rdf_property = f'        <hasBeenFoundHere rdf:resource="http://www.semanticweb.org/amivid/ontologies/2022/2/untitled-ontology-38#{(unidecode.unidecode(str(df_objects.loc[ind, "Stazione"]))).replace(" ", "_")}"/>\n'
            rdf_type = f'        <typeObject>{unidecode.unidecode(str(elt_rdf_type))}</typeObject>\n'
            found_date = f'        <foundDate>{df_objects.loc[ind, "Data"]}</foundDate>\n'
            if df_objects.loc[ind, 'Data di restituzione'] != "nan":
                recovered_date = f'        <recoveredDate>{df_objects.loc[ind, "Data di restituzione"]}</recoveredDate>\n'
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
        'Stazioni italiane.csv',
        sep=',')

    df_place = df_place[
        ['CODICE', 'NOME STAZIONE', 'REGIONE', 'CODICE REGIONE', 'LONGITUDINE', 'LATITUDINE', 'CITTA']]

    with open(input_path_data) as f:
        lines = f.readlines()

        for ind in tqdm(df_place.index.tolist()):
            pos = len(lines) - lines.index("    // General axioms\n") + 4  # -36
            owl_first_line = f'    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/amivid/ontologies/2022/2/untitled-ontology-38#{syntax_to_owl(unidecode.unidecode(df_place.loc[ind, "NOME STAZIONE"]))}">\n'
            comment = f'    <!-- http://www.semanticweb.org/amivid/ontologies/2022/2/untitled-ontology-38#{syntax_to_owl(unidecode.unidecode(df_place.loc[ind, "NOME STAZIONE"]))} -->\n'
            rdf_type = f'        <rdf:type rdf:resource="http://www.semanticweb.org/amivid/ontologies/2022/2/untitled-ontology-38#Train_station"/>\n'
            codiceRegione = f'        <codiceRegione>{unidecode.unidecode(str(df_place.loc[ind, "CODICE REGIONE"]))}</codiceRegione>\n'
            codice = f'        <codice>{"00" + str(df_place.loc[ind, "CODICE"])[:-2]}</codice>\n'
            nomeStazione = f'        <nomeStazione>{unidecode.unidecode(str(df_place.loc[ind, "NOME STAZIONE"]))}</nomeStazione>\n'
            latitudine = f'        <latitudine rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">{df_place.loc[ind, "LATITUDINE"]}</latitudine>\n'
            longitudine = f'        <longitudine rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">{df_place.loc[ind, "LONGITUDINE"]}</longitudine>\n'
            regione = f'        <regione>{unidecode.unidecode(str(df_place.loc[ind, "REGIONE"]))}</regione>\n'
            citta = f'        <citta>{unidecode.unidecode(str(df_place.loc[ind, "CITTA"]))}</citta>\n'
            owl_last_line = '    </owl:NamedIndividual>\n'
            back_slash_n = '    \n'

            lines.insert(-pos, comment)
            lines.insert(-pos, owl_first_line)
            lines.insert(-pos, rdf_type)
            lines.insert(-pos, codiceRegione)
            lines.insert(-pos, codice)
            lines.insert(-pos, nomeStazione)
            lines.insert(-pos, latitudine)
            lines.insert(-pos, longitudine)
            lines.insert(-pos, regione)
            lines.insert(-pos, citta)
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
    #get_data_to_rdf_train_station(file_rdf, file_output)
    get_data_to_rdf_object(file_output, './data/output_context.owl')
