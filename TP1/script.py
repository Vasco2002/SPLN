
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

pharse = "nao quero sorrir." #"muito adoravel, Ele não ser muito adoravel" 
#"muito adoravel" <- é um TERM
#"nao querer" e "nao ser" <- é um NEGT
#"sorrir" <- Palavra normal

"""Finalmente estreou a minha série favorita na Netflix! 😄

Sinceramente, não gosto muito de ir para eventos sociais muito movimentados, o barulho todo deixa-me desorientado.

Adoro dias de chuva, faz com que eu não tenha de regar o jardim :D

Alguém deixou uma caixa fechada à porta da minha casa, eu estou com um bocado de receio da abrir 💀

Wow, olha para o sol! Realmente hoje está um bom dia. 

Foi um jogo difícil, mas no final, fiquei contente por o Famalicão ter ganho! Mais 3 pontos 💪💪💪

Hoje está um calor descomunal, e não tenho forma nenhuma de ir à praia :-((((((((

Esta semana estreia o novo filme do Homem-Aranha, já nem consigo dormir com o entusiasmo 😩

Acabei de ouvir uma das piores músicas que já ouvi na minha vida... Que coisa horrorosa

Ontem fui sair com os meus amigos. Estava mesmo a precisar, adoro aquela malta! 😍😍"""

#Pôr os verbos das frases com o seu lema
doc = nlp(pharse)

phrase_lema = " ".join(token.lemma_ if token.pos_ == "VERB" else token.text for token in doc)

normalized_str = unicodedata.normalize('NFD', phrase_lema)

noAccentPharse = normalized_str.encode('ascii', 'ignore').decode('utf-8')

#print(noAccentPharse)

#Devolve uma lista das posições onde essa palavra foi ocorrida no mesmo texto
def find_pos(word, text):
    posicoes = []
    inicio = 0
    while True:
        pos = text.find(word, inicio)
        if pos == -1:
            break
        posicoes.append(pos)
        inicio = pos + 1
    return posicoes

#Dado uma determenida posição devolve as duas palavras antes dessa posição
def words_before(posicao, texto):
    substring = texto[:posicao]

    third = substring.rfind(" ", 0, posicao)
    second = substring.rfind(" ", 0, third)
    first = substring.rfind(" ", 0, second)

    if third == -1:
        return substring[:posicao]

    return substring[first + 1:second] + " " + substring[second+ 1:third]


#String com todos os termos dentro do texto
termos = ""

for pal in db["TERM"].keys():
    if pal in noAccentPharse:
        termos += pal + " "

#String com todos as negações que são termos dentro do texto
negtermos = ""

for pal in db["NEGT"].keys():
    if pal in noAccentPharse:
        negtermos += pal + " "

#Lista de palavras dentro do texto
words_list = noAccentPharse.split(" ")

#Contador de elementos que alteram a polaridade
nr_pol = 0

#Contador de elementos que alteram a polaridade positivamente
nr_plus = 0

#Contador de elementos que alteram a polaridade negativamente
nr_minus = 0

for key in ["TERM","EMOJI",""]:
    
    pals = db[key]

    if key == "TERM":
         print("\nTermos:\n")
         for pal in pals.keys():
            if pal in noAccentPharse:
                occurrences = find_pos(pal, noAccentPharse)
                for pos in occurrences:
                    before = words_before(pos, noAccentPharse)
                    if before in db["NEGT"].keys():
                        nr_pol += 2
                        polaridade = pals[pal]["Polaridade"] * -1
                        pol += polaridade
                        print("Palavra: " + before + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(pals[pal]["Polaridade"] * -1)) 
                    elif before in db["NEG"].keys() and before not in negtermos:
                        nr_pol += 2
                        polaridade = pals[pal]["Polaridade"] * -1
                        pol += polaridade
                        print("Palavra: " + before + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(pals[pal]["Polaridade"] * -1)) 
                    elif before in db["INCR"].keys():
                        nr_pol += 2
                        polaridade = pals[pal]["Polaridade"] * 2
                        pol += polaridade
                        print("Palavra: " + before + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(pals[pal]["Polaridade"] * 2)) 
                    elif before in db["DECR"].keys():
                        nr_pol = 2
                        polaridade = pals[pal]["Polaridade"] / 2
                        pol += polaridade
                        print("Palavra: " + before + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(pals[pal]["Polaridade"] / 2)) 
                    else:
                        nr_pol = 1
                        polaridade = pals[pal]["Polaridade"]
                        pol += polaridade
                        print("Palavra: " + pal + " Posição:" + str(pos) + " Polaridade:" + str(pals[pal]["Polaridade"])) 
                    
                    if polaridade > 0:
                        nr_plus += 1
                    elif polaridade < 0:
                        nr_minus += 1

    elif key == "EMOJI":
        print("\nEmojis:\n")
        for pal in pals.keys():
            if pal in pharse:
                occr = pharse.count(pal)
                #print(f"{pal} {occr} {pals[pal]["Polaridade"]}")
                print("Emoji: " + pal + " NºOcorrência:" + str(occr) + " Polaridade:" + str(pals[pal]["Polaridade"]))
                polaridade = (pals[pal]["Polaridade"] * occr)
                pol += polaridade

                if polaridade > 0:
                    nr_plus += occr
                elif polaridade < 0:
                    nr_minus += occr

    elif key == "":
        print("\nPalavras:\n")
        for pal in pals.keys():
            if pal in words_list:
                occurrences = find_pos(pal, noAccentPharse)
                for pos in occurrences:
                    before = words_before(pos, noAccentPharse)
                    split = before.split()  # Pegar a última palavra da string 'before' após dividi-la
                    if len(split) > 1:
                        previous_word = split[1]
                    else:
                        if before == " ":
                            previous_word = ""
                        else:
                            previous_word = before
                    if previous_word + " " + pal not in termos and previous_word + " " + pal not in negtermos:
                        if before in db["NEGT"].keys():
                            nr_pol += 2
                            polaridade = pals[pal]["Polaridade"] * -1
                            pol += polaridade
                            print("Palavra: " + before + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(pals[pal]["Polaridade"] * -1)) 
                        elif before in db["NEG"].keys() and before not in negtermos:
                            nr_pol += 2
                            polaridade = pals[pal]["Polaridade"] * -1
                            pol += polaridade
                            print("Palavra: " + before + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(pals[pal]["Polaridade"] * -1)) 
                        elif before in db["INCR"].keys():
                            nr_pol += 2
                            polaridade = pals[pal]["Polaridade"] * 2
                            pol += polaridade
                            print("Palavra: " + before + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(pals[pal]["Polaridade"] * 2)) 
                        elif before in db["DECR"].keys():
                            nr_pol += 2
                            polaridade = pals[pal]["Polaridade"] / 2
                            pol += polaridade
                            print("Palavra: " + before + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(pals[pal]["Polaridade"] / 2)) 
                        else:
                            nr_pol += 1
                            polaridade = pals[pal]["Polaridade"]
                            pol += polaridade
                            print("Palavra: " + pal + " Posição:" + str(pos) + " Polaridade:" + str(pals[pal]["Polaridade"]))

                        if polaridade > 0:
                            nr_plus += 1
                        elif polaridade < 0:
                            nr_minus += 1
                    
result = pol / nr_pol

def remover_pontuacao(lista_palavras):
    return [palavra for palavra in lista_palavras if palavra.isalpha()]

print("\nNúmero de Palavras: " + str(len(remover_pontuacao(words_list))))

print("\nNúmero de Elementos Positivos: " + str(nr_plus))

print("\nNúmero de Elementos Negativos: " + str(nr_minus))

print("\nPolaridade do Texto: " + str(result))

#Um elemento é um conjunto de tipo especial(NEG, NEGT, INCR, DECR) + palavra/termo ou Emoji que altera a polaridade do texto

