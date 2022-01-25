import csv
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
import tkinter.messagebox as messagebox


class ProjectSplit:
    def __init__(self, proj_data):
        self.proj_data = proj_data

    def split_projects(self):
        copy_start_row = 0
        copy_end_row = 0

        file_path_raw = askopenfilename(title='Select raw file to copy', initialdir="L:/Assay Development/Enspire")

        if file_path_raw:
            for proj, inner_dict in self.proj_data.items():
                proj_name = proj
                plate_num = len(inner_dict["plates"])
                try:
                    folder_path_raw = askdirectory(
                        title="Choose Raw folder from Project folder to place file for " + proj_name,
                    )
                except FileNotFoundError:
                    pass
                else:
                    if folder_path_raw:
                        with open(file_path_raw) as csv_file:
                            reader = csv.reader(csv_file)
                            copy_end_row += int(plate_num) * 48
                            plate_rows = [row for idx, row in enumerate(reader) if idx in range(copy_start_row, copy_end_row)]
                            copy_start_row = copy_end_row

                            raw_output = f"{folder_path_raw}/{proj_name}_raw.csv"
                            with open(raw_output, 'w', newline="") as newFile:
                                csv_writer = csv.writer(newFile)
                                for row in plate_rows:
                                    csv_writer.writerow(row)

                        inner_dict["raw_file"] = raw_output

                    else:
                        return False

            messagebox.showinfo(title="Congrats!", message="File has been moved!")

            return self.proj_data
        else:
            return False


if __name__ == "__main__":
    test_data = {
        "SSF00test1": {
            "plates": ["1"]
        },
        "SSF00test2": {
            "plates": ["1"]
        }
    }
    
    returned_data = ProjectSplit(test_data).split_projects()
    if returned_data:
        print(returned_data)
        print("Pass")