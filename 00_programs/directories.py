import os
import glob
import pandas as pd


def directories_path_setup(_project_name, _root):
    """
    function is making directories (in case of it is not done):
        - 00_programs
        - 01_input
        - 02_output
        - 03_temporary
    input:
        - _project_name (string): (snake_case_convection)
        - _root (string): path where to put the project input output etc.


    returns:
        - directories (dictionary: {string: string}): name of folder and path
    """
    _project_name_join = str(_project_name + "/")
    directories = {
        "00_programs": os.path.join(_root, _project_name_join, "00_programs"),
        "01_input": os.path.join(_root, _project_name_join, "01_input"),
        "02_output": os.path.join(_root, _project_name_join, "02_output"),
        "03_temporary": os.path.join(_root, _project_name_join, "03_temporary"),
    }

    # Create directories if they don't exist
    for directory in directories.values():
        if os.path.exists(directory):
            print(f"The {directory} exists already.")
        elif not os.path.exists(directory):
            print(f"The {directory} has been made.")
            os.makedirs(directory)

    return directories


def update_gitignore(directories, _project_name, _root):
    with open(str(_root + "/" + _project_name + "/" + ".gitignore"), "a") as f:
        f.write(
            str("\n#" + _project_name + "\n")
            + f'\n{directories["01_input"]}\n{directories["02_output"]}\n{directories["03_temporary"]}'
        )
        f.close()
    print(" .gitignore updated with input output ")


def reading_files(directories):
    """
    - input:
        - directories (dict):
            - keys: manes of directories
            - values: path to the folders
    - return: dict of files stored in input folder
        - keys: dataframe name (string)
        - values: dataframes
    """
    input_files = glob.glob(directories["01_input"] + "/*.csv")
    print(input_files)
    for i in range(len(input_files)):
        input_files[i] = input_files[i].removeprefix(directories["01_input"])

        input_files[i] = input_files[i].removesuffix(".csv")
    files_dict = {}
    for i in input_files:
        i = i.removeprefix("/")
        files_dict[i] = pd.read_csv(str(directories["01_input"] + "/" + i + ".csv"))
    return files_dict
