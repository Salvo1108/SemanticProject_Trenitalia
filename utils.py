import pandas as pd
import unidecode
import re


def syntax_to_owl(chn: str):
    """ Get ride of punctuation in a string for owl file"""
    chn = '_'.join(re.findall('\w+', chn))
    chn = unidecode.unidecode(str(chn))
    return chn


def convert_list_queries_to_df(l_queries: list, l_cols: list):
    """ Convert lists of a list into into a pd.DataFrame """
    df = pd.DataFrame(columns=l_cols)
    for q in l_queries:
        df = df.append(pd.DataFrame(data=[q], columns=l_cols))
    return df


if __name__ == '__main__':
    # df_all_objects = pd.read_csv(
    #     'https://ressources.data.sncf.com/explore/dataset/objets-trouves-restitution/download/?format=csv&refine.date=2022&refine.gc_obo_date_heure_restitution_c=2022&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B',
    #     sep=';')

    # df_all_objects["Type d'objets change"] = df_all_objects["Type d'objets"]
    # df_all_objects["Nature d'objets change"] = df_all_objects["Nature d'objets"]

    # for col in ["Type d'objets change", "Nature d'objets change"]:
    #     df_all_objects[col] = df_all_objects[col].apply(lambda x: syntax_to_owl(x))

    # d_type = {k: v for k, v in zip(df_all_objects["Type d'objets"].unique(), df_all_objects["Type d'objets change"].unique())}
    # d_nature = {k: v for k, v in zip(df_all_objects["Nature d'objets"].unique(), df_all_objects["Nature d'objets change"].unique())}

    # print(len(list(d_nature.values())))

    test = [['Bagagerie_sacs_valises_cartables', '2022-03-22T11:53:41+01:00', '2022-03-22T12:50:12+01:00', '74000',
             45.901965, 6.121835, 'Annecy'],
            ['Bagagerie_sacs_valises_cartables', '2022-03-21T16:37:52+01:00', '2022-03-21T17:02:50+01:00', '13232',
             43.302666, 5.380407, 'Marseille']]
    print(convert_list_queries_to_df(test, ['type', 'fDate', 'rDate', 'zipcode', 'lat', 'long', 'city']))
