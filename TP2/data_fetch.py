import re
import json
from icecream import ic

def dataFetch(query):
    with open(f"similares/{query.replace(' ','_')}.json", "r", encoding='utf-8') as file:
        content = json.load(file)

    file = open("data/2024-04-07-DRE_dump.sql", "r", encoding='utf-8')

    irs = [ir["id"] for ir in content]

    sql_data = {}

    for ir in irs:
        sql_data[ir] = []

    flag = False
    atual_ir = None

    temp = ""

    for line in file:
        if len(line) != 0:
            if not flag: 
                regex = r'INSERT INTO .* VALUES \((\d+), (\d+), .*\);'
                sql_parser = re.compile(regex)
                queries = sql_parser.findall(line)
                if len(queries) > 0:
                    ir = int(queries[0][0])
                    if ir in irs:
                        sql_data[ir].append(line)
                else:
                    regex = r'INSERT INTO .* VALUES \((\d+), (\d+), .*'
                    sql_parser = re.compile(regex)
                    queries = sql_parser.findall(line)
                    if len(queries) > 0:
                        ir = int(queries[0][1])
                        if ir in irs:
                            temp = line
                            flag = True
                            atual_ir = ir
                
            else:
                regex = r'.*\);'
                sql_parser = re.compile(regex)
                queries = sql_parser.findall(line)
                temp = temp + line
                if len(queries) > 0:
                    flag = False
                    sql_data[atual_ir].append(temp)
                    temp = ""

    with open(f"prepared_data/{query.replace(' ','_')}_attributes.json", "w", encoding='utf-8') as file:
        file.write(json.dumps(sql_data, ensure_ascii=False))
   
