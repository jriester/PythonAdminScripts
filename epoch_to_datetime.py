import argparse
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description="CSV Parser")
    parser.add_argument('-f', dest="file_path", required=True,
                        help="/path/to/file")
    return parser.parse_args()


def epoch_replacement(file):
    file_contents = []
    print(f"Replacing epoch timestamps in {file}")
    with open(file, "r") as f:
        for line in f:
            if "|" in line and "%" in line:
                split = line.split('|')[1]
                date_time = datetime.utcfromtimestamp(float(split)).isoformat(timespec='milliseconds')
                file_contents.append(line.replace(split, str(date_time)))
            else:
                file_contents.append(line)
        
    with open(file + ".new.log", "w") as file:
        for line in file_contents:
            file.write(line)
    print(f"Finished replacing epoch timestamps in {file.name}")


if __name__ == '__main__':
    file_path = parse_args().file_path
    epoch_replacement(file_path)
