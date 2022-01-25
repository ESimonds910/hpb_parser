class AddStandard:
    def __init__(self, df_package, proj_data):
        self.df_package = df_package
        self.proj_data = proj_data
        self.stand_dict = self.proj_data['std_conc']
    
    def add_standard(self):
        for df, data in self.df_package.items():
            data.insert(7, "Standard Conc.", "")

            for well, conc in self.stand_dict.items():
                data.loc[(data["Well Coordinates"] == well), 'Sample Type'] = "Standard"
                data.loc[(data["Well Coordinates"] == well), 'Standard Conc.'] = conc
            
            self.df_package[df] = data

        return self.df_package

if __name__ == "__main__":
    import pandas as pd
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
    data_standard = AddStandard(stitched_data, test_data).add_standard()
    with pd.ExcelWriter("./test/single_project_test/test_outputs/test_data_stand.xlsx") as writer:
        data_standard["main_df"].to_excel(writer, sheet_name="Calculations")
        data_standard["display_df"].to_excel(writer, sheet_name="Display_Ready")
        data_standard["main_df_rep"].to_excel(writer, sheet_name="Rep_Calculations")
        data_standard["display_df_rep"].to_excel(writer, sheet_name="Rep_Display_Ready")

    source_data = FileFinder(test_data_rep).data_finder()
    restructured_data = RawRestructure(test_data_rep, source_data).data_format()
    od_data = ODImport(test_data_rep).format_od()
    stitched_data = StitchRawOD(restructured_data, od_data, test_data_rep).stitch_dfs()
    data_standard = AddStandard(stitched_data, test_data).add_standard()
    with pd.ExcelWriter("./test/single_project_test/test_outputs/test_data_reps_stand.xlsx") as writer:
        data_standard["main_df"].to_excel(writer, sheet_name="Calculations")
        data_standard["display_df"].to_excel(writer, sheet_name="Display_Ready")
        data_standard["main_df_rep"].to_excel(writer, sheet_name="Rep_Calculations")
        data_standard["display_df_rep"].to_excel(writer, sheet_name="Rep_Display_Ready")