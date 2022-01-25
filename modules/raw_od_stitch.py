import pandas as pd
import numpy as np

class StitchRawOD:
    def __init__(self, df_package, od_data, proj_data):
        self.df_package = df_package
        self.od_data = od_data
        self.proj_data = proj_data
        self.stitched_df = pd.DataFrame()

    def stitch_dfs(self):
        for df, data in self.df_package.items():
            try:
                data.set_index("Identifier", drop=False, inplace=True)
            except KeyError:
                print(f"{df} empty and skipped")

            self.stitched_df = self.od_data.join(data, how="right")
            self.stitched_df.set_index("Screening Intermediate", drop=True, inplace=True)
            # try:
            #     self.stitched_df.sort_values(by="Col", inplace=True)
            # except KeyError:
            #     pass

            self.df_package[df] = self.stitched_df

        return self.df_package
    



if __name__ == "__main__":
    from raw_import import FileFinder
    from od_import import ODImport
    from raw_restructure import RawRestructure

    test_data = dict(
        proj_name="SSF007-LS",
        plates=["38", "39"],
        points=4,
        std_conc={
            "A1": 60,
            "B1": 30,
            "C1": 10,
            "D1": 3.33,
            "E1": 1.11,
            "F1": 0.33
        },
        od_file="test",
        test_file="./test/single_project_test/SSF00test_OD.csv",
        volumes=[1, 0.75, 0.5, 0.25],
        raw_file="./test/single_project_test/SSF00test_raw.csv"
    )
    test_data_rep = dict(
        proj_name="SSF007-LS",
        plates=["38-1", "38-2"],
        points=4,
        std_conc={
            "A1": 60,
            "B1": 30,
            "C1": 10,
            "D1": 3.33,
            "E1": 1.11,
            "F1": 0.33
        },
        od_file="test",
        test_file="./test/single_project_test/SSF00test_OD.csv",
        volumes=[1, 0.75, 0.5, 0.25],
        raw_file="./test/single_project_test/SSF00test_raw.csv"
    )
    source_data = FileFinder(test_data).data_finder()
    proj_name = test_data["proj_name"]
    restructured_data = RawRestructure(proj_name, test_data, source_data).data_format()
    od_data = ODImport(test_data).format_od()
    stitched_data = StitchRawOD(restructured_data, od_data, test_data).stitch_dfs()
    with pd.ExcelWriter("./test/single_project_test/test_outputs/test_data.xlsx") as writer:
        stitched_data["main_df"].to_excel(writer, sheet_name="Calculations")
        stitched_data["display_df"].to_excel(writer, sheet_name="Display_Ready")
        stitched_data["main_df_rep"].to_excel(writer, sheet_name="Rep_Calculations")
        stitched_data["display_df_rep"].to_excel(writer, sheet_name="Rep_Display_Ready")

    source_data = FileFinder(test_data_rep).data_finder()
    proj_name = test_data_rep["proj_name"]
    restructured_data = RawRestructure(proj_name, test_data_rep, source_data).data_format()
    od_data = ODImport(test_data_rep).format_od()
    stitched_data = StitchRawOD(restructured_data, od_data, test_data_rep).stitch_dfs()
    with pd.ExcelWriter("./test/single_project_test/test_outputs/test_data_reps.xlsx") as writer:
        stitched_data["main_df"].to_excel(writer, sheet_name="Calculations")
        stitched_data["display_df"].to_excel(writer, sheet_name="Display_Ready")
        stitched_data["main_df_rep"].to_excel(writer, sheet_name="Rep_Calculations")
        stitched_data["display_df_rep"].to_excel(writer, sheet_name="Rep_Display_Ready")