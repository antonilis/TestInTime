import pandas as pd
import os
import read_files
import calc_ef


class TimeAnalizer:

    def __init__(self, raw_data_path, pmba_path):
        self.raw_data_path = raw_data_path
        self.files = self.get_files_names()
        self.raman_pmba = read_files.read_txt_spectrum(pmba_path)
        self.peaks = {'p1': ['471', '581'], 'p2': ['1154', '1221'], 'p3': ['1535', '1688'],
                      'p4': ['1154', '1215'], 'p5': ['1453', '1510']}

        self.data = self.get_data()

    def get_files_names(self):
        dates = os.listdir(self.raw_data_path)

        folder_structure = {}

        for date in dates:
            folder_structure[date] = os.listdir(os.path.join(self.raw_data_path, date))

        return folder_structure


    def get_data(self):

        df_list = []
        raman_intensity = calc_ef.get_peak_intensities(self.raman_pmba, self.peaks)

        for date in self.files:

            for file in self.files[date]:
                df = read_files.read_files(self.raw_data_path, date, file)
                sers_intensity = calc_ef.get_peak_intensities(df, self.peaks)

                ef = calc_ef.calculate_ef(sers_intensity, raman_intensity).min(axis=1).values

                df['ef'] = ef
                df['date'] = date
                df['name'] = file
                df_list.append(df)

        dat = pd.concat(df_list)
        dat.dropna(axis=1, inplace=True)
        dat.reset_index(drop = True, inplace=True)

        return dat













