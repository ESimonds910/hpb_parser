import pandas as pd
import json
import numpy as np
from time import time
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilename, askdirectory
from string import ascii_uppercase as upstr

# from hiprbind_analysis import data_analysis
# from analysis import main

from modules.multiproject_split import ProjectSplit as mps
from modules.raw_import import FileFinder as ri
from modules.od_import import ODImport as oi
from modules.raw_restructure import RawRestructure as rr
from modules.raw_od_stitch import StitchRawOD as ros
from modules.add_standard import AddStandard as ast
from modules.calculations import Calculations as calc


class RunParser:
    def __init__(self, data_package, app=None):
        self.window = Tk()
        self.window.withdraw()
        self.ended = False
        self.data_package = data_package
        self.proj_dates = []
        self.flask_app = app

    def run_main(self):
        if self.data_package:
            self.data_package = mps(self.data_package).split_projects()

        if self.data_package:
            for proj, data in self.data_package.items():
                self.proj_dates.append(data['date'])
                proj_df = ri(data).data_finder()

                if not proj_df:
                    self.window.destroy()
                    return False
                
                df_package = rr(proj, data, proj_df).data_format()

                if not df_package:
                    self.window.destroy()
                    return False
                
                if data["od_file"]:
                    od_data = oi(data).format_od()
                    if not isinstance(od_data, pd.DataFrame):
                        self.window.destroy()
                        return False

                    df_package = ros(df_package, od_data, data).stitch_dfs()
                    if not df_package:
                        self.window.destroy()
                        return False

                if "std_conc" in data:
                    df_package = ast(df_package, data).add_standard()
                
                df_package = calc(df_package, data).make_calculations()

                    # self.window.withdraw()
                output_path = askdirectory(
                    title="Choose folder to place output file for " + proj,
                    initialdir='L:/Molecular Sciences/Small Scale Runs'
                )

                if not output_path:
                    self.window.destroy()
                    return False

                final_out_path = f"{output_path}/{proj}_output.xlsx"
                data["out_path"] = final_out_path
                with pd.ExcelWriter(final_out_path) as writer:
                    df_package["main_df"].to_excel(writer, sheet_name="Calculations")
                    df_package["display_df"].to_excel(writer, sheet_name="Display_Ready")
                    df_package["main_df_rep"].to_excel(writer, sheet_name="Rep_Calculations")
                    df_package["display_df_rep"].to_excel(writer, sheet_name="Rep_Display_Ready")

                    messagebox.showinfo(title="Congratulations!", message=f"Project {proj} has been output.")

                self.window.destroy()
        else:
            self.window.destroy()
            return False

        for run_date in self.proj_dates:
            try:
                with open("archived_data.json", 'r') as arc_file:
                    archived_data = json.load(arc_file)
            except FileNotFoundError:
                break

            for idx, run in enumerate(archived_data['projects']):
                try:
                    if run['date'] == run_date:
                        del archived_data['projects'][idx]
                except KeyError:
                    pass     
                else:
                    with open("archived_data.json", "w") as updated_arc_file:
                        json.dump(archived_data, updated_arc_file, indent=4)


        return self.data_package
        # with open("parser_data.json", "w") as update_parser_file:
        #     json.dump(self.data_package, update_parser_file, indent=4)

        # main.BuildDashboard(self.proj_data_dict, self.flask_app)


if __name__ == "__main__":
    test_data = {
        "SSF007-LS": dict(
            plates=["38", "39"],
            date="00/00/0000",
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
    }

    test_data_rep = {
        "SSF007-LS": dict(
            plates=["38-1", "38-2"],
            date="00/00/0000",
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
    }
    RunParser(test_data).run_main()
    RunParser(test_data_rep).run_main()
    
