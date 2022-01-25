import pandas as pd
import numpy as np

class Calculations:
    def __init__(self, df_package, proj_data):
        self.df_package = df_package
        self.proj_data = proj_data
        self.dv = proj_data["volumes"]
        self.points = proj_data["points"]
        self.signals = ["Alpha", "DNA"]

    def make_calculations(self):
        for df, data in self.df_package.items():
            if (df == "main_df" or df == "main_df_rep") and not data.empty:
                for signal in self.signals:
                    for n in range(1, int(self.points)):
                        numerator = (data[f"{signal}_{n + 1}"] - data[f"{signal}_{n}"])
                        denominator = (self.dv[n] - self.dv[n - 1])
                        calced_slope = f"{signal}_slope_{n}"
                        data[calced_slope] = round(numerator / denominator, 2)

                    if self.points == 8:
                        last_slope = 4
                    else:
                        last_slope = 3

                    data[f"{signal}.Max.Slope"] = data.loc[:, f"{signal}_slope_1": f"{signal}_slope_{last_slope}"].max(axis=1)

                # data["HPB_DNA"] = round(data["Alpha.Max.Slope"] / data["DNA.Max.Slope"], 2)

                # if self.proj_data["od_file"]:
                #     data["OD 600 (AU)"] = data["OD 600 (AU)"].apply(lambda x: round(float(x), 2) if x != "" else "0.0")
                #     data["HPB_OD"] = round(data["Alpha.Max.Slope"] / data["OD 600 (AU)"], 2)

                self.df_package[df] = data
        return self.df_package


if __name__ == "__main__":
    from raw_import import FileFinder
    from od_import import ODImport
    from raw_restructure import RawRestructure
    from raw_od_stitch import StitchRawOD

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
    restructured_data = RawRestructure(test_data, source_data).data_format()
    od_data = ODImport(test_data).format_od()
    stitched_data = StitchRawOD(restructured_data, od_data, test_data).stitch_dfs()
    calced_data = Calculations(stitched_data, test_data).make_calculations()

    with pd.ExcelWriter("./test/single_project_test/test_outputs/test_calced_data.xlsx") as writer:
        calced_data["main_df"].to_excel(writer, sheet_name="Calculations")
        calced_data["display_df"].to_excel(writer, sheet_name="Display_Ready")
        calced_data["main_df_rep"].to_excel(writer, sheet_name="Rep_Calculations")
        calced_data["display_df_rep"].to_excel(writer, sheet_name="Rep_Display_Ready")

    source_data = FileFinder(test_data_rep).data_finder()
    restructured_data = RawRestructure(test_data_rep, source_data).data_format()
    od_data = ODImport(test_data_rep).format_od()
    stitched_data = StitchRawOD(restructured_data, od_data, test_data_rep).stitch_dfs()
    calced_data = Calculations(stitched_data, test_data_rep).make_calculations()


    with pd.ExcelWriter("./test/single_project_test/test_outputs/test_calced_data_reps.xlsx") as writer:
        calced_data["main_df"].to_excel(writer, sheet_name="Calculations")
        calced_data["display_df"].to_excel(writer, sheet_name="Display_Ready")
        calced_data["main_df_rep"].to_excel(writer, sheet_name="Rep_Calculations")
        calced_data["display_df_rep"].to_excel(writer, sheet_name="Rep_Display_Ready")