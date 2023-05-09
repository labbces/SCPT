#open a file in reading mode, and read a single line at the time

# Define the path to the input file and the output file
orthogroupsFile = '/home/diriano/Downloads/orthogroups_with_lengths.test.tsv'
longestTranscripot4Orthogroup='longestTranscript4Orthogroup.tbl'

# Import the defaultdict class from the collections module
from collections import defaultdict

# Create an empty defaultdict object called longestTranscript, which will store the longest transcript for each orthologous group
longestTranscript = defaultdict(dict)

# Open the input file in read mode using a with statement to ensure proper file handling
with open(orthogroupsFile, "r") as file:
    # Loop over each line in the file
    for line in file:
        # Strip trailing whitespace and split the line into fields based on the tab character
        line=line.rstrip()
        fields=line.split('\t')
        og = fields[0]
        transcript_len = int(fields[2])
        transcript_id = fields[1]
        # Check if the current orthologous group (fields[0]) is already in the longestTranscript dictionary
        if og in longestTranscript:
            # Get the current longest transcript length for the orthologous group
            current_longest_len = list(longestTranscript[og].keys())[0]
            # Compare the length of the current transcript to the length of the longest transcript for the orthologous group
            if transcript_len > int(current_longest_len):
                # If the current transcript is longer, update the dictionary with the new longest transcript
                del longestTranscript[og][current_longest_len]
                longestTranscript[og][transcript_len] = transcript_id
        else:
                # If the orthologous group is not in the longestTranscript dictionary, add the current transcript as the longest transcript
                longestTranscript[fields[0]][fields[2]]=fields[1]

# Pre-allocate a list to store the lines to be printed
lines_to_print = []

# Loop over the longestTranscript dictionary and append each orthologous group with its longest transcript to the list
for og in longestTranscript.keys():
    for t in longestTranscript[og].keys():
        line = f'{og}\t{t}\t{longestTranscript[og][t]}'
        lines_to_print.append(line)

# Print all lines at once
with open(longestTranscripot4Orthogroup, 'w') as file:
    file.write('\n'.join(lines_to_print))