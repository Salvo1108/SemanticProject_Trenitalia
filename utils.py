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

