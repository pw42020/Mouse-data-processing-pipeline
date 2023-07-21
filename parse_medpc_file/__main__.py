"""Converting Moorman/Vazey MED-PC data files to json data or
.mat file dependent on arguments passed"""
import sys
import argparse
from datetime import date, datetime
from typing import Protocol
from .parse_file import MedPCFileParser


class FilenameArguments(Protocol):
    """Filename arguments exclusively passed into
    create_filename()

    Attributes
    ----------
    data_number: int
        number, like 136, 137, ... for the data
    date: str
        formatted yr-mo-date (i.e. 2023-07-21)
    time: str
        formatted hr:min (i.e. 11:04)
    """

    @property
    def data_number(self) -> int:
        """Data number for the file"""

    @property
    def date(self) -> str:
        """Date for the file"""

    @property
    def time(self) -> str:
        """Time for the file"""


def create_cmd_line_arguments() -> None:
    """Create command line arguments that users will pass in

    Parameters
    ----------
    1. --data-number: int
        number, like 136, 137, ... for the data
    2. --date: str
        formatted yr-mo-date (i.e. 2023-07-21)
    3. --time: str
        formatted hr:min (i.e. 11:04)
    4. --mat: bool
        format the file as a .mat
    5. --json: bool
        format the file as a .json

    Notes
    -----
    - `--mat` and `--json` are mutually exclusive, cannot use them at the
    same time
        - if you want to use them both, run the program twice
    """

    now: datetime = datetime.now()  # create datetime object for now for use
    # in --time

    parser.add_argument("--data-number", type=int, required=True)
    parser.add_argument("--date", type=str, default=date.today())
    parser.add_argument("--time", type=str, default=now.strftime("%H:%M"))
    # create mutually exclusive data
    mutual_exclusion = parser.add_mutually_exclusive_group()
    mutual_exclusion.add_argument("--mat", default=False, action="store_true")
    mutual_exclusion.add_argument("--json", default=False, action="store_true")


def create_filename(*, args: FilenameArguments) -> str:
    """Create filename for the file that will be created

    Parameters
    ----------
    None

    Returns
    -------
    filename: str
        filename for the file that will be created
    """

    time = args.time.split(":")
    args.time = f"{time[0]}h{time[1]}m"

    return f"{args.date}_{args.time}_Subject {args.data_number}"


def main() -> None:
    """Main function for convert_file.py"""
    args = parser.parse_args()
    filename: str = create_filename(args=args)

    MedPCFileParser(filename=filename, mat=args.mat, json=args.json).parse_file()


# create Argument Parser
parser = argparse.ArgumentParser(
    prog="MED-PC data file converter",
    description="Convert MED-PC data files for Moorman/Vazey lab",
    epilog="HELLO THERE!!",
)

create_cmd_line_arguments()

if __name__ == "__main__":
    ret: int = main()
    sys.exit(ret)
