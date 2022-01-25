from msilib.schema import File
import pandas as pd
import numpy as np
from string import ascii_uppercase as letters


class RawRestructure:
    def __init__(self, proj, proj_data, df_package):
        # self.plates = proj_data["plates"]
        self.points = proj_data["points"]
        self.proj_name = proj
        self.volumes = proj_data["volumes"]
        self.hpb_scheme = proj_data["ab_name"]
        self.df_package = df_package
        self.display_formatted_df = pd.DataFrame()
        self.main_formatted_df = pd.DataFrame()
        self.rep_main_formatted_df = pd.DataFrame()
        self.rep_display_formatted_df = pd.DataFrame()

    def data_format(self):
        start_row = 0
        if self.points == 8:
            end_row = 8
        else:
            end_row = 16

        for plate, data in self.df_package.items():
            rep = False
            if "-" in plate:
                source_plate = plate.split("-")[0]
                if int(plate.split("-")[1]) > 1:
                    rep = True
            else:
                source_plate = plate
            well_index = 0
            for row in range(start_row, end_row, 2):
                row_2 = row + 1

                end_col = int(data.shape[1] / 2)
                for col in range(1, end_col, 2):
                    col_2 = col + 1
                    dna_col = col + 24
                    dna_col_2 = dna_col + 1

                    # alpha_quad = list(source.iloc[row][[col, col_2]]) + list(source.iloc[row_2][[col, col_2]])
                    #This 'quad' represents the 4 data points on plate in a square area
                    alpha_quad = [
                        data.iloc[row][col],
                        data.iloc[row_2][col],
                        data.iloc[row][col_2],
                        data.iloc[row_2][col_2]
                    ]
                    # dna_quad = list(source.iloc[row][[dna_col, dna_col_2]]) + list(source.iloc[row_2][[dna_col, dna_col_2]])
                    dna_quad = [
                        data.iloc[row][dna_col],
                        data.iloc[row_2][dna_col],
                        data.iloc[row][dna_col_2],
                        data.iloc[row_2][dna_col_2]
                    ]

                    main_df_columns = [f"Alpha_{n}" for n in range(1, 5)] + [f"DNA_{n}" for n in range(1, 5)]

                    if self.points == 8:
                        row_3 = row + 8
                        row_4 = row + 9
                        alpha_quad_2 = list(data.iloc[row_3][[col, col_2]]) + list(data.iloc[row_4][[col, col_2]])
                        alpha_quad += alpha_quad_2
                        dna_quad_2 = list(data.iloc[row_3][[dna_col, dna_col_2]]) + \
                                    list(data.iloc[row_4][[dna_col, dna_col_2]])
                        dna_quad += dna_quad_2
                        main_df_columns = [f"Alpha_{n}" for n in range(1, 9)] + [f"DNA_{n}" for n in range(1, 9)]

                    main_df = pd.DataFrame([alpha_quad + dna_quad], columns=main_df_columns)
                    display_df = pd.DataFrame([alpha_quad, dna_quad], index=["Alpha", "DNA"]).transpose()

                    main_df = self.build_columns(main_df, plate, source_plate, well_index)
                    display_df = self.build_columns(display_df, plate, source_plate, well_index, df_id="display")
                    
                    if rep:
                        self.rep_main_formatted_df = pd.concat([self.rep_main_formatted_df, main_df])
                        self.rep_display_formatted_df = pd.concat([self.rep_display_formatted_df, display_df])
                    else:
                        self.main_formatted_df = pd.concat([self.main_formatted_df, main_df])
                        self.display_formatted_df = pd.concat([self.display_formatted_df, display_df])
                    well_index += 1
            # start_row += 16
            # end_row += 16
        df_package = dict(
            main_df=self.main_formatted_df,
            main_df_rep=self.rep_main_formatted_df,
            display_df=self.display_formatted_df,
            display_df_rep=self.rep_display_formatted_df
        )
        # df_list = [self.main_formatted_df, self.rep_main_formatted_df, self.display_formatted_df, self.rep_display_formatted_df]

        return df_package

    def build_columns(self, df, plate, source_plate, w_idx, df_id="main"):
        
        if df.shape[1] == 16 or df.shape[0] == 8:
            row_len = 4
        else:
            row_len = 8
        well_ids = [letter + str(num) for letter in letters[:row_len] for num in range(1, 13)]

        if df_id == "display":
            df.insert(0, "Volumes", self.volumes)
            df.insert(0, "Col", int(well_ids[w_idx][1:]))
            df.insert(0, "Row", well_ids[w_idx][:1])
            # df.insert(0, "Plate-Well", f"{plate}-{well_ids[w_idx]}")
            df.insert(0, "Original Plate", plate)
            df.insert(0, "HPB_Scheme", self.hpb_scheme)
            # df.insert(1, "Well_Id", well_ids[w_idx])
            # df.insert(0, "Id", plate.split("-")[0] + "-" + df["Well_Id"])
            df.insert(0, "Identifier", self.proj_name + "-" + source_plate + "-" + well_ids[w_idx])
            return df

        
        df.insert(0, "Volume_4", self.volumes[3])
        df.insert(0, "Volume_3", self.volumes[2])
        df.insert(0, "Volume_2", self.volumes[1])
        df.insert(0, "Volume_1", self.volumes[0])
        df.insert(0, "Original Plate", plate)
        df.insert(0, "HPB_Scheme", self.hpb_scheme)
        # df.insert(1, "Well_Id", well_ids[w_idx])
        
        
        
        
        # df.insert(0, "Id", plate.split("-")[0] + "-" + df["Well_Id"])
        df.insert(0, "Identifier", self.proj_name + "-" + source_plate + "-" + well_ids[w_idx])
        return df


if __name__ == "__main__":
    from raw_import import FileFinder

    test_data = dict(
        proj_name="SSF007-LS",
        plates=["1", "2"],
        ab_name="test_scheme",
        points=4,
        volumes=[1, 0.75, 0.5, 0.25],
        raw_file="./test/single_project_test/SSF00test_raw.csv"
    )
    test_data_rep = dict(
        proj_name="SSF007-LS",
        plates=["1-1", "1-2"],
        ab_name="",
        points=4,
        volumes=[1, 0.75, 0.5, 0.25],
        raw_file="./test/single_project_test/SSF00test_raw.csv"
    )
    source_data = FileFinder(test_data).data_finder()
    restructured_data = RawRestructure(test_data["proj_name"], test_data, source_data).data_format()
    print(restructured_data)

    source_data = FileFinder(test_data_rep).data_finder()
    restructured_data = RawRestructure(test_data["proj_name"], test_data_rep, source_data).data_format()
    print(restructured_data)

