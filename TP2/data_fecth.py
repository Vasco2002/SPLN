import re
import json
from icecream import ic

with open("prepared_data/IRS_completo.json", "r", encoding='utf-8') as file:
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
            for ir in irs:
                regex = r'INSERT INTO .* VALUES .+ ' + f"{ir}" + r', .+;'
                sql_parser = re.compile(regex)
                queries = sql_parser.findall(line)
                if len(queries) > 0:
                    for sq in queries:
                        sql_data[ir].append(sq)
                        ic(sq)
                    break
                else:
                    regex = r'INSERT INTO .* VALUES .+ ' + f"{ir}" + r', .+'
                    sql_parser = re.compile(regex)
                    queries = sql_parser.findall(line)
                    if len(queries) > 0:
                        temp = queries[0]
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
               ic(temp)
               temp = ""


ic(sql_data)


with open("IRS_attributes.json", "w", encoding='utf-8') as file:
    file.write(json.dumps(sql_data, ensure_ascii=False))
   
