import numpy as np

import web.CRUD as CRUD


def parsing_data(df):
    headings = df.columns.ravel()
    result_JSON = []
    df = df.replace(np.nan, None)

    for count in df.index:
        form = {}
        for head in headings:
            form[head] = df[head][count]
        result_JSON.append(form)
    return result_JSON


def get_name(name_from_db=CRUD.get_name()):
    list_names = []

    for name in name_from_db:
        name_str = str(name)
        name_str = name_str.replace('(', '')
        name_str = name_str.replace(')', '')
        name_str = name_str.replace(',', '')
        name_str = name_str.replace("'", '')
        list_names.append(name_str)
    return list_names
