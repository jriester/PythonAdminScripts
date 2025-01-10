from datetime import datetime

file = '<path to file here>'
file_contents = []
with open(file, "r") as f:
    for line in f:
        if "|" in line:
            date_time = datetime.utcfromtimestamp(float(line.split('|')[1])).isoformat(timespec='milliseconds')
            file_contents.append(line.replace(line.split('|')[1], str(date_time)))
        else:
            file_contents.append(line)

with open(file + ".new.log", "w") as file:
    for line in file_contents:
        file.write(line)
