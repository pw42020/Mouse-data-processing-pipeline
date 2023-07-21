"""Main meat of file where file processing takes place
"""
# pylint: disable=invalid-name
import os  # to verify file is file before I do anything
from typing import Any, TextIO, Final
from dataclasses import dataclass
import json
from scipy.io import savemat


@staticmethod
def is_float(string: str) -> bool:
    """Returns whether a str is a float or not

    Parameters
    ----------
    string: str
        string in question that is being checked if float

    Returns
    -------
    bool
        true if float is float, false if not float
    """
    try:
        float(string)
        return True
    except ValueError:
        return False


@dataclass
class MedPCFileParser:
    """Class that parses a MedPC file

    Attributes
    ----------
    mat: bool
        if the file is a .mat file
    json: bool
        if the file is a .json file
    filename: str
        name of file that is being interpreted

    Notes
    -----
    - `mat` and `json` are mutually exclusive, cannot use them at the
    same time
    """

    filename: str
    mat: bool
    json: bool

    def __post_init__(self) -> None:
        """Post-initialization of class"""
        if self.mat and self.json:
            raise ValueError("Cannot use both --mat and --json at the same time")

        if not self.mat and not self.json:
            raise AttributeError("Must use either --mat or --json")

    def parse_file(self) -> None:
        """Parse file self.filename

        Raises
        -------
        OSError
            If file not found
        """
        txt_file: str = self.filename + ".txt"
        if not os.path.isfile(txt_file):
            raise OSError(f"File {txt_file} not found")

        mapped_values: dict[str, Any] = {}
        with open(txt_file, "r", encoding="utf-8") as file:
            mapped_values = self.parse_file_contents(file=file)

        if self.mat:
            self.save_file_mat(mapped_values=mapped_values)
        if self.json:
            self.save_file_json(mapped_values=mapped_values)

    def save_file_mat(self, mapped_values: dict[str, Any]) -> None:
        """Saving the mapped values as .mat file

        Parameters
        ----------
        mapped_values: dict[str, Any]
            the mapped values in question
        """
        savemat(self.filename + ".mat", mapped_values)

    def save_file_json(self, mapped_values: dict[str, Any]) -> None:
        """Saving the mapped values as .json file

        Parameters
        ----------
        mapped_values: dict[str, Any]
            the mapped values in question
        """
        with open(self.filename + ".json", "w", encoding="utf-8") as file:
            json.dump(mapped_values, file, indent=4)

    def parse_file_contents(self, file: TextIO) -> dict[str, Any]:
        """Parse the file contents of the file opened

        Parameters
        ----------
        file: TextIO
            file opened

        Returns
        -------
        dict[str, Any]
            dictionary of values mapped to their respective keys

        Notes
        -----
        ### Three Scenarios
        1. Line input is a one line key-value pair
            - i.e. Start-date: 7/21/2023
        2. Line input has nothing
            - i.e. blank line
        3. Line input is a multi-line key-values pair
            - i.e. F:
                0: 0.000 1.000 2.000 3.000 7.000
                5: ...
                ...
        """

        mapped_values: dict[str, Any] = {}

        file_lines: Final[list[str]] = file.readlines()

        i = 0
        while i <= len(file_lines) - 1:
            line = file_lines[i]
            split_line: Final[list[str]] = line.split(
                ":", 1
            )  # splitting at first occurence of :

            # will split via : and if there is no : in the line, then it will
            # only have one object, and we continue
            # else, if the only argument after : is \n, then it is a multi-line key-value

            if len(split_line) == 1:
                i+= 1
                continue

            if split_line[1] == "\n":
                # multi-line key-value pair
                i, mapped_values[split_line[0]] = self.find_key_value(
                    file=file_lines, i=i+1
                )
                # print(f"Added {mapped_values[split_line[0]]} in position {split_line[0]}")
                continue

            # print(f"Adding {split_line[1]} to mapped_values")
            # one line key-value pair
            mapped_values[split_line[0]] = (
                float(split_line[1]) if is_float(split_line[1]) else split_line[1]
            )
            i += 1
            continue

        return mapped_values

    def find_key_value(self, file: list[str], i: int) -> tuple[int, list[Any]]:
        """Find the multi-line key-value pair in the file

        Parameters
        ----------
        file: list[str]
            file.readlines() from above
        i: int
            current position of i in the file.readlines() list

        Returns
        -------
        tuple[int, list[Any]]
            tuple of the new position of i and the list of values
        """
        ret_list: list[Any] = []
        try:
            while not (line_lis := file[i].split(":"))[0].isalpha():
                # print(f"Adding {line_lis[1]} to ret_list")
                ret_list.extend(
                    [float(x) if is_float(x) else x for x in line_lis[1].split()]
                )
                i += 1
        except IndexError:
            # If IndexError, then we have reached the end of the file
            return i, ret_list
        return i, ret_list
