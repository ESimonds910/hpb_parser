import pandas as pd
import xlrd
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

class ODImport:
    def __init__(self, proj_data):
        self.od_df = pd.DataFrame()
        self.proj_data = proj_data
        self.od_data = self.proj_data["od_file"]
        self.input_od_path = None

    def format_od(self):
        if self.od_data == "test":
            self.input_od_path = self.proj_data["test_file"]
        elif self.od_data:
            self.get_file()
        else:
            return False

        if self.input_od_path:
            self.import_od()
        else:
            return False

        if self.od_df.empty:
            messagebox.showinfo(title="Uh oh...", message="The OD file may be empty...")
            return False
        else:
            header_check = self.check_col_headers()
        
        if header_check:
            self.structure_data()
            return self.od_df
        else:
            return False

    def get_file(self):
        self.input_od_path = askopenfilename(title="Choose OD file.")

    def import_od(self):
        try:
            self.od_df = pd.read_excel(self.input_od_path)
        except FileNotFoundError:
            messagebox.showinfo(title="Uh oh...", message="Something's wrong. The OD file wasn't found.")
            pass
        except ValueError:
            try:
                self.od_df = pd.read_csv(self.input_od_path)
            except FileNotFoundError:
                messagebox.showinfo(title="Uh oh...", message="Something's wrong. The OD file wasn't found.")
                pass
        except xlrd.XLRDError:
            try:
                self.od_df = pd.read_excel(self.input_od_path)
            except xlrd.XLRDError:
                self.od_df = pd.read_csv(self.input_od_path)
            except FileNotFoundError:
                messagebox.showinfo(title="Uh oh...", message="Something's wrong. The OD file wasn't found.")


    def check_col_headers(self):
        false_cols = []
        true_col_headers = [
            "Strain ID", 
            "Strain Lot", 
            "SSF Experiment", 
            "Plate", 
            "Well Coordinates", 
            "Sample Type", 
            "Screening Intermediate", 
            "OD 600 (AU)"
            ]
        true_col_len = len(true_col_headers)
        actual_col_len = len(self.od_df.columns)

        if true_col_len != actual_col_len:
            messagebox.showinfo(title="Uh oh...", message=f"{actual_col_len} columns were given, expected {true_col_len} columns...")
            return False

        for column in self.od_df.columns:
            if column not in true_col_headers:
                false_cols.append(column)
            
        if false_cols:
            for false_col in false_cols:
                messagebox.showinfo(title="Uh oh...", message=f"'{false_col}' does not match required column headers for Benchling.")
                
            return False
        else:
            return True

    def structure_data(self):
        # self.od_df["OD 600 (AU)"] = self.od_df["OD 600 (AU)"].replace(" ", "0.0")
        self.od_df.insert(4, "Plate Num", self.od_df["Plate"].apply(lambda x: str(int(x[-3:]))))
        self.od_df.insert(0, "Identifier", self.od_df["SSF Experiment"] + "-" + self.od_df["Plate Num"] + "-" + self.od_df["Well Coordinates"])
        self.od_df.set_index("Identifier", drop=True, inplace=True)

if __name__ == "__main__":
    test_data = dict(
        od_file="test",
        test_file="./test/single_project_test/SSF00test_OD.csv"
    )
    test_data_empty = dict(
        od_file="test",
        test_file="./test/single_project_test/SSF00test_OD_empty.csv"
    )
    test_data_badheader = dict(
        od_file="test",
        test_file="./test/single_project_test/SSF00test_OD_badheader.csv"
    )
    select_data_check = dict(
        od_file=True
    )
    od_check = ODImport(test_data).format_od()
    if isinstance(od_check, pd.DataFrame):
        print("Check 1: Pass")
    
    od_check = ODImport(test_data_empty).format_od()
    if not od_check:
        print("Check 2: Pass")
    
    od_check = ODImport(test_data_badheader).format_od()
    if not od_check:
        print("Check 3: Pass")

    select_file_check = ODImport(select_data_check).format_od()
    if isinstance(select_file_check, pd.DataFrame):
        print("Check 4: Pass")