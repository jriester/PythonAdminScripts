import pandas as pd
import re
import os
import argparse


# Parse the initial arguments and return arguments as an object
# Possible args:
#     -f <file_path>
#      r (this does not take an actual argument, it serves as a flag only)
# Example: python3 ReadCSV.py -f /my/file/path -r
def parse_args():
    parser = argparse.ArgumentParser(description="CSV Parser")
    parser.add_argument('-f', dest="file_path", required=True,
                        help="/path/to/csv/file")
    parser.add_argument('-r', dest="raw", required=False, action='store_true',
                        help="Whether to parse the file as a RAW CSV and skip the first row (header)")
    return parser.parse_args()


# Check that the index requested by the user is greater than 0 and less than the highest column index
def check_bad_edges(user_data: list, columns_len: int) -> bool:
    for num in user_data:
        if int(num) < 0 or int(num) > columns_len:
            print(f"You entered an invalid number: {num} | Largest possible index: {columns_len}")
            exit()
        else:
            return True


# Check user is putting in valid characters
def check_characters(value_list: list) -> bool:
    for s in value_list:
        for c in s:
            if c.isdigit() or c == ',' or c == '-':
                continue
            else:
                print(f"Invalid character {c}, expecting: positive integers, comma, or hyphen.")
                exit()
    return True


# Show the user all the column indexes and names, ask them which they want
# Take the list, strip all whitespace, split on comma, remove all empty strings
# Check for bad edge cases
def column_menu(column_len: int) -> list:
    print("Printing a list of column index and names")
    print("Create a list of indexes (ex: 1-5,7,12-15) and this script will output only data for those columns")
    print(*tuple_list, sep='\n')

    column_string = input("Enter the column indexes you'd like to grab. (ex: 1-5,7,12-15)\n")
    clean_col_list = [x for x in column_string.replace(" ", "").split(',') if x]
    character_list = re.split(",|-", ",".join(clean_col_list))
    if check_characters(character_list):
        if check_bad_edges(character_list, column_len):
            return clean_col_list


# Take list of user input, parse ranges and individual indexes, append to list, return list
def parse_user_list(user_indexes: list) -> list:
    output_list = []

    for x in user_indexes:
        if '-' in x:
            s = x.split("-")
            if int(s[-1]) == int(s[0]):
                continue
            if int(s[-1]) > int(s[0]):
                for n in range(int(s[0]), int(s[-1]) + 1):
                    output_list.append(n)
            else:
                for n in reversed(range(int(s[-1]), int(s[0]) + 1)):
                    output_list.append(n)
        else:
            output_list.append(int(x))

    return output_list


def raw_csv_to_dataframe(path: str) -> pd.DataFrame:
    data = pd.read_csv(path, sep='","', quotechar='"', quoting=3, engine='python', on_bad_lines='warn', skiprows=[0])
    return pd.DataFrame(data)


# Convert the input CSV file to a Pandas dataframe
def csv_to_dataframe(path: str) -> pd.DataFrame:
    data = pd.read_csv(path, sep=",")
    return pd.DataFrame(data)


# From the dataframe return a list of the columns
def get_columns(dataframe: pd.DataFrame) -> list:
    return dataframe.columns.values.tolist()


# Take in user's requested indexes, grab those from the dataframe, write the dataframe to a CSV at the input file destination with _dataframe.csv postfix
def list_to_dataframe(in_list: list, dataf: pd.DataFrame, path: str):
    try:
        dataf = dataf[dataf.columns[in_list]]
    except IndexError as e:
        print(f"Invalid index: {e}")
        exit()
    data_frame_file_path = f"{path}_dataframe.csv"
    if os.path.exists(data_frame_file_path):
        os.remove(data_frame_file_path)
    else:
        dataf.to_csv(data_frame_file_path, sep=' ', index=False)
    if os.path.exists(data_frame_file_path):
        print(f"Created file: {data_frame_file_path}")
    else:
        print(f"Could not create file: {data_frame_file_path}")


# Main
if __name__ == '__main__':
    args = parse_args()
    input_path = args.file_path
    r_flag = args.raw
    if r_flag:
        df = raw_csv_to_dataframe(input_path)
    else:
        df = csv_to_dataframe(input_path)
    columns = get_columns(df)
    tuple_list = tuple(((columns.index(x), x) for x in columns))
    user_indices = column_menu(len(columns) - 1)
    out_list = parse_user_list(user_indices)
    list_to_dataframe(out_list, df, input_path)
