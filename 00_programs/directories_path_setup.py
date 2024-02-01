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
