import pandas as pd
import pandas.errors as pderrors
import numpy as np
from tkinter import messagebox

PLATE_IDX = [x for x in range(25)]
DNA_PLATE_IDX = [x for x in range(24, 49)]

class FileFinder:
    def __init__(self, proj_data):
        # self.all_main_data = pd.DataFrame()
        # self.all_rep_data = pd.DataFrame()
        # self.main_alpha_data = pd.DataFrame()
        # self.main_dna_data = pd.DataFrame()
        # self.rep_alpha_data = pd.DataFrame()
        # self.rep_dna_data = pd.DataFrame()
        self.plates = proj_data["plates"]
        self.input_raw_path = proj_data["raw_file"]
        self.df_package = dict()
        self.alpha_data = pd.DataFrame()
        self.dna_data = pd.DataFrame()

    def data_finder(self):
        # rep = False
        for plate in self.plates:
            # if "-" in plate:
            #     if int(plate.split("-")[1]) > 1:
            #         rep = True
            plate_idx = self.plates.index(plate)
            self.alpha_data = self.file_import("alpha", plate_idx)
            self.dna_data = self.file_import("dna", plate_idx)
            if self.alpha_data.empty or self.dna_data.empty:
                messagebox.showinfo(
                    title="Hang on...",
                    message="The raw file may be empty, or raw path was not indicated."
                )
                return False
            else:
                combined_df = self.concat_alpha_dna()
                self.df_package[plate] = combined_df
                # if rep:
                #     self.rep_alpha_data = pd.concat([self.rep_alpha_data, alpha_data])
                #     self.rep_dna_data = pd.concat([self.rep_dna_data, dna_data])
                # else:
                #     self.main_alpha_data = pd.concat([self.main_alpha_data, alpha_data])
                #     self.main_dna_data = pd.concat([self.main_dna_data, dna_data])

        # return self.concat_alpha_dna()
        return self.df_package

    def concat_alpha_dna(self):
        combined_df = pd.concat([self.alpha_data, self.dna_data], axis=1)
        # self.all_main_data = pd.concat([self.main_alpha_data, self.main_dna_data], axis=1)
        # self.all_rep_data = pd.concat([self.rep_alpha_data, self.rep_dna_data], axis=1)
        # df_package = dict(
        #     main=self.all_main_data,
        #     rep=self.all_rep_data
        # )

        # return df_package
        return combined_df

    def file_import(self, section, count):
        if section == "alpha":
            row_skip = 7
            index = PLATE_IDX
        else:
            row_skip = 31
            index = DNA_PLATE_IDX
        try:
            plate_df = pd.read_csv(
                self.input_raw_path,
                header=None,
                index_col=0,
                names=index,
                usecols=np.arange(0, 25),
                skiprows=row_skip + count * 48,
                nrows=16,
                encoding='unicode_escape'
            )
        except pderrors.ParserError:
            messagebox.showinfo(title="Hang on...", message="Raw file is not in typical format. Please check.")
        else:
            return plate_df

if __name__ == "__main__":
    test_data = dict(
        plates=["1", "2"],
        raw_file="./test/single_project_test/SSF00test_raw.csv"
    )
    test_data_rep = dict(
        plates=["1-1", "1-2"],
        raw_file="./test/single_project_test/SSF00test_raw.csv"
    )
    returned_data = FileFinder(test_data).data_finder()
    print(returned_data)

    returned_data = FileFinder(test_data_rep).data_finder()
    print(returned_data)
