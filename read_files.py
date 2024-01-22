import pandas as pd
import matplotlib.pyplot as plt


def read_spectrum(filepath):
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
    return data_df


path = './test_w_czasie/2023_12_22/SP_5.csv'

file_sections = {'up': {'parameters': {'skiprows': 80, 'skipfooter': 2129 - 243}, 'axis': [1, 5]},
               'bottom': {'parameters': {'skiprows': 242, 'skipfooter': 2129 - 2064}, 'axis': [5, 9]},
               'down': {'parameters': {'skiprows': 2063, 'skipfooter': 0}, 'axis': [1, 5]}
                 }

df_list = []

for section in file_sections:

    df = pd.read_csv(path, sep=',', header=None, engine='python', **file_sections[section]['parameters'])

    df = df.iloc[:, [-7, -8]]

    df.columns = 'raman shift', 'intensity'
    df.set_index('raman shift', inplace=True)

    df_list.append(df)

dat = pd.concat(df_list)

old_df = read_spectrum('../data/2023-08-21/PMBA/A/SP_4.txt')


plt.plot(dat)
plt.show()

plt.plot(old_df)
