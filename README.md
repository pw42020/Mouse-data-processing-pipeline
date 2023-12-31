### MedPC File Parser
By Patrick Walsh

Python module that takes command line arguments or a graphical user interface and an automated data entry file generated by MedPC and turns it into a *.json or *.mat file with the same file title formatting as the initial text file

---
### Installation Guide
Download the repository using

```sh
git clone https://github.com/pw42020/Mouse-data-processing-pipeline
```
Once the repository is downloaded, you should see the repository copied over, with a file_parser folder and a setup.py specifically.

To set up the module, type:
```sh
cd Mouse-data-processing-pipeline; pip install -e .
```
This will enter your current working directory as the GitHub repository you just copied, and then install the FileParser module using pip into Python.

Now, you should be able to run the command and see something like this:
```sh
PS C:\Users\User> python -m parse_medpc_file -h

usage: MED-PC data file converter [-h] --data-number DATA_NUMBER [--date DATE] [--time TIME] [--mat | --json] --gui

Convert MED-PC data files for Moorman/Vazey lab

options:
  -h, --help            show this help message and exit
  --data-number DATA_NUMBER
  --date DATE
  --time TIME
  --mat
  --json
  --gui

HELLO THERE!!
```

### Using the ParseMedPCFile module

There are five total options for input to parse the file, three describing the file you are inputting, and one describing the format you want your file to be on completion of the file parsing (either `*.mat` or `*.json`)

1. --data-number: int
   - number, like 136, 137, ... for the data
2. --date: str
   - formatted yr-mo-date (i.e. 2023-07-21)
3. --time: str
   - formatted hr:min (i.e. 11:04)
4. --mat: bool
   - format the file as a .mat
5. --json: bool
   - format the file as a .json
6. --gui: bool
   - use the gui functionality of the program instead of the command-line interface

- `--mat` and `--json` are mutually exclusive, cannot use them at the
    same time
        - if you want to use them both, run the program twice

These are all executed from the command line, all writing `python -m parse_medpc_file` before writing as command line arguments

Note: To use `--gui` you must still input `--mat` or `--json` to use the module

An example command is shown below:

```sh
python -m parse_medpc_file --data-number=138 --date=2023-07-12 --time=11:05 --json
```

And here is an example of using the GUI:
```sh
python -m parse_medpc_file --gui --json
```

Happy coding!
