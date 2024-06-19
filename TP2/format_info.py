import json
import re

def extract_text(query):
    match = re.findall(r"INSERT INTO public\.\w+ VALUES \(\d+, \d+, .*, .*,", query)

    if match:
        start_index = query.find(match[0])
        
        if start_index != -1:
            result = query[start_index + len(match[0]):]
            return result.replace("'", "").replace(")", "").replace(";", "").replace("(", "").replace("<div>", "").replace("</div>", "").replace("<p>","").replace("</p>"," ").replace("<a href=","").replace("<div id=","").replace('\"doc_texto\"> ','').replace("</a>","").replace("\n","").replace("</span>","").replace("<span>","").replace("<br/>","").replace("<span class=\"bold\">","").replace("\"doc_texto\">","") + "\n"
        else:           
            print("Match not found in the query string.")
    else:
        print("No match found.")

def formatInfo(file_name):
    with open(f'prepared_data/{file_name.replace(" ","_")}_attributes.json', 'r') as file:
        data = json.load(file)

    extracted_info = []

    for key, queries in data.items():
        for query in queries:

            if query.startswith("INSERT INTO public.dreapp_document VALUES ("):
                pass
            elif query.startswith("INSERT INTO public.dreapp_documenttext VALUES ("):
                extracted_info.append(extract_text(query))

    with open(f'information/{file_name.replace(" ","_")}_info.txt', 'w') as file:
        for info in extracted_info:
            file.write(info + '\n')

