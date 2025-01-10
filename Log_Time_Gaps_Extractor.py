from datetime import timedelta
from Helper_Functions import *

# This script should parse the timestamps in the specified log file and report any events where the time between two
# log messages was greater than a configurable number of seconds (in this case, 60 seconds). Note that you will need
# to replace "path/to/log/file.log" with the actual path to your log file.


loadedConfigs = load_config()

# Define the maximum number of seconds between log messages
#  TODO make this load in from configs
max_seconds_between_messages = 10

# Read the file into log_contents after verifying its encoding
log_content = read_input_file()

outFile = create_output_log_overwrite("Time_Differences_Found.TimeGaps")
write_to_file(outFile, "Report of Time Gaps found in {}\n".format(get_input_file))

# TODO: give an option to detect and switch between Java and LibrdKafka Time Stamps
results = string_pattern_search(log_content, clean_string(loadedConfigs.get("Timestamps", "librd_regex_ts")))

for i in range(len(results)):
    if i + 1 < len(results):
        time_difference = difference_in_str_ts(results[i].match.group(2), results[i + 1].match.group(2), clean_string(
            loadedConfigs.get("Timestamps", "librd_datetime_ts")), clean_string(
            loadedConfigs.get("Timestamps", "librd_datetime_ts")))

        if time_difference > timedelta(seconds=max_seconds_between_messages):
            if time_difference > timedelta(seconds=max_seconds_between_messages):
                print(f"Time difference between log messages is greater than {max_seconds_between_messages} "
                              "seconds. Gap of " + str(
                                  time_difference) + " was found:\n")
                write_to_file(outFile,
                              "Time difference between log messages is greater than {max_seconds_between_messages} "
                              "seconds. Gap of " + str(
                                  time_difference) + " was found:\n")
                print(f"\t" + str(log_content[i].strip()) + "\n\t" + str(log_content[i + 1].strip()) + "\n")
                write_to_file(outFile,
                              "\t" + str(log_content[i].strip()) + "\n\t" + str(log_content[i + 1].strip()) + "\n")

# log_message(loadedConfigs, "Created output file " + outFile)
# Close the output file
outFile.close()
