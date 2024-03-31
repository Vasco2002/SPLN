
import csv
import unicodedata
import spacy
from spacy import displacy

nlp = spacy.load("pt_core_news_lg")

db = {}
pol = 0

with open("final_lema.csv", encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["tipo"] not in db.keys():
            db[row["tipo"]] = {}
        if row["palavra"] not in db[row["tipo"]].keys():
            db[row["tipo"]][row["palavra"]] = {"Polaridade": float(row["polaridade"]), "occr": 1}
        else:
            db[row["tipo"]][row["palavra"]]["Polaridade"] += float(row["polaridade"])
            db[row["tipo"]][row["palavra"]]["occr"] += 1 

for key in db.keys():
    for pal in db[key].keys():
        db[key][pal]["Polaridade"] = db[key][pal]["Polaridade"]/db[key][pal]["occr"] 




pharse = """Foi um jogo difícil, mas no final, fiquei contente por o Famalicão ter ganho! Mais 3 pontos 💪💪💪

Hoje está um calor descomunal, e não tenho forma nenhuma de ir à praia :-((((((((

Esta semana estreia o novo filme do Homem-Aranha, já nem consigo dormir com o entusiasmo 😩

Acabei de ouvir uma das piores músicas que já ouvi na minha vida... Que coisa horrorosa

Ontem fui sair com os meus amigos. Estava mesmo a precisar, adoro aquela malta! 😍😍"""


normalized_str = unicodedata.normalize('NFD', pharse)
noAccentPharse = normalized_str.encode('ascii', 'ignore').decode('utf-8')

for key in db.keys():
    pals = db[key]
    if key == "TERM":
         for pal in pals.keys():
            if pal in noAccentPharse:
                occr = noAccentPharse.count(pal.lower())
                print(f"{pal} {occr} {pals[pal]["Polaridade"]}")
                pol += (pals[pal]["Polaridade"] * occr)

    elif key == "NEG":
        for pal in pals.keys():
            if pal in noAccentPharse:
                occr = noAccentPharse.count(pal.lower())
                print(f"{pal} {occr} {pals[pal]["Polaridade"]}")
                pol += (pals[pal]["Polaridade"] * occr)

    elif key == "INCR":
        for pal in pals.keys():
            if pal in noAccentPharse:
                occr = noAccentPharse.count(pal.lower())
                print(f"{pal} {occr} {pals[pal]["Polaridade"]}")
                pol += (pals[pal]["Polaridade"] * occr)

    elif key == "EMOJI":
        for pal in pals.keys():
            if pal in pharse:
                occr = pharse.count(pal)
                print(f"{pal} {occr} {pals[pal]["Polaridade"]}")
                pol += (pals[pal]["Polaridade"] * occr)

    elif key == "DECR":
        for pal in pals.keys():
            if pal in noAccentPharse:
                occr = noAccentPharse.count(pal.lower())
                print(f"{pal} {occr} {pals[pal]["Polaridade"]}")
                pol += (pals[pal]["Polaridade"] * occr)

    else:
        for pal in pals.keys():
            words_list = noAccentPharse.split(" ")
            if pal in words_list:
                occr = words_list.count(pal.lower())
                print(f"{pal} {occr}  {pals[pal]["Polaridade"]}")
                pol += (pals[pal]["Polaridade"] * occr)

# 1.6 

print(pol)




# Verificar tipo da palavra e criar tratamento adequado 
# Transformar verbos na versão lema
# Testar com mais frases
# Testar com os capitulos
#
# Tipos => ['', 'TERM', 'INCR', 'EMOJI', 'NEG', 'DECR']
#
#



# Ler o ficheiro
# Usar o spacy para obter forma lema dos verbos
# Usar dataset com polaridades para verificar a polaridade do capitulo
# Varios valores => Termo -> Decr -> Incr -> NEG
# Correr o texto todo, ou apenas correr o dataset final 
#