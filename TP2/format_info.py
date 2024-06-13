import json
import re

query = "Tribunal"

def extract_text(query):
    match = re.findall(r"INSERT INTO public\.\w+ VALUES \(\d+, \d+, .*, .*,", query)

    # Check if there is at least one match
    if match:
        # Find the index of the first match in the query string
        start_index = query.find(match[0])
        
        # Extract everything past the first match
        if start_index != -1:
            result = query[start_index + len(match[0]):]
            return result.replace("'", "").replace(")", "").replace(";", "").replace("(", "").replace("<div>", "").replace("</div>", "").replace("<p>","").replace("</p>","").replace("<a href=","").replace("</a>","").replace("\n","")
        else:
            print("Match not found in the query string.")
    else:
        print("No match found.")

# Read the JSON file
with open('prepared_data/IRS_attributes.json', 'r') as file:
    data = json.load(file)

# Prepare the list to store extracted information
extracted_info = []

# Iterate over the items in the JSON
for key, queries in data.items():
    for query in queries:
        #print(query)
        if query.startswith("INSERT INTO public.dreapp_document VALUES ("):
            pass
        elif query.startswith("INSERT INTO public.dreapp_documenttext VALUES ("):
            extracted_info.append(extract_text(query))

# Write the extracted information to a new file
with open(f'information/{query.replace("","_")}_info.txt', 'w') as file:
    for info in extracted_info:
        file.write(info + '\n')

print("Information extraction complete. Check the 'information/IRS_info.txt' file.")
