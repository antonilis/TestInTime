import os

import pandas as pd
import matplotlib.pyplot as plt


# TODO There should be only 1 reading function
def read_txt_spectrum(filepath):
    """
    Reads numeric data from file and returns DataFrame
    :param filepath: String
    :return: DataFrame
    """
    read_params = {'sep': ';', 'skiprows': lambda x: x < 79 or x > 1500, 'decimal': ',',
                   'usecols': ['Raman Shift', 'Dark Subtracted #1'],
                   'skipinitialspace': True, 'encoding': "utf-8", 'na_filter': True}

    data_df = pd.read_csv(filepath, **read_params)

    data_df.dropna(axis=0, how="any")

    data_df = data_df[data_df.iloc[:, 0] > 253]

    data_df = data_df.astype({'Raman Shift': 'int'})

    # Solution for files in which there were no values in the column "Raman Shift"
    if data_df.empty:
        return None

    data_df.set_index('Raman Shift', inplace=True)

    data = data_df.T
    # changes col names type from int to str, for .loc
    cols = [str(x) for x in data.columns]
    data.columns = cols

    return data


def read_csv_spectrum(file_path):
    parameters = {'sep': ',', 'header': None, 'engine': 'python', 'skiprows': 242, 'skipfooter': 2129 - 1500}

    data = pd.read_csv(file_path, **parameters).iloc[:, [5, 11]]

    data.columns = 'Raman Shift', 'Dark Subtracted #1'

    data = data[data.iloc[:, 0] > 253]

    data = data.astype({'Raman Shift': 'int'})

    # Solution for files in which there were no values in the column "Raman Shift"
    if data.empty:
        return None

    data.set_index('Raman Shift', inplace=True)

    data = data.T
    # changes col names type from int to str, for .loc
    cols = [str(x) for x in data.columns]
    data.columns = cols

    return data


def read_files(path, date, file_name):
    direction = os.path.join(path, date, file_name)

    extension = os.path.splitext(direction)[1]

    if extension == '.csv':

        df = read_csv_spectrum(direction)

    elif extension == '.txt':

        df = read_txt_spectrum(direction)

    else:
        raise ValueError('Wrong extension of the file')

    return df
