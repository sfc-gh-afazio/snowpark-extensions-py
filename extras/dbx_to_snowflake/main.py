import argparse, os
from dbc_to_jupyter import DbcToJupyter
from source_to_jupyter import SourceToJupyter
from constants import Constants

# Parse the arguments
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Script to convert a Python, Sql or Scala notebook to a Jupyter Notebook.')
    parser.add_argument("-i", "--input", metavar="\b", type=str, required=True, help="The notebook file path to convert.")
    parser.add_argument("-o", "--output", metavar="\b", type=str, required=True, help="Path where the .ipynb file will be created.")

    return parser.parse_args()

SOURCE_EXTENSIONS = [Constants.PY_EXTENSION, Constants.SQL_EXTENSION, Constants.SCALA_EXTENSION, Constants.R_EXTENSION]

if __name__ == "__main__":
    args = parse_args()
    input_folder = args.input
    output_folder = args.output
    
    for path, _, files in os.walk(input_folder):
        for file in files:
            file_absolute_path = os.path.join(path, file)

            try:
                file_relative_path = os.path.relpath(file_absolute_path, input_folder)

                if file.lower().endswith(Constants.DBC_EXTENSION):
                    DbcToJupyter().main(input_folder, file_absolute_path, output_folder)

                elif file.lower().endswith(tuple(SOURCE_EXTENSIONS)):
                    SourceToJupyter().main(file_absolute_path, file_relative_path, output_folder)

                else:
                    print(f"\033[93mWarning: File not supported: {file_absolute_path}\033[0m")
                    continue

            except Exception as e:
                print(f"\033[91mError: Converting the notebook: {file_absolute_path}")
                print(f"Error: {e}\033[0m")
                continue