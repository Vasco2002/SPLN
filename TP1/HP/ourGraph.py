from jjcli import *
import csv
import unicodedata
import spacy
import sys
import os
from spacy import displacy
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

#Devolve uma lista das posições onde essa palavra foi ocorrida no mesmo texto
def find_pos(word, text):
    posicoes = []
    inicio = 0
    word = " " + word + " "
    while True:
        pos = text.find(word, inicio)
        if pos == -1:
            break
        posicoes.append(pos + 1)
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
    if second == -1:
        return substring[second+ 1:third]

    return substring[first + 1:second] + " " + substring[second+ 1:third]

def remover_pontuacao(lista_palavras):
    return [palavra for palavra in lista_palavras if palavra.isalpha()]

def calcPol(pharse,db):
    pol = 0

    nlp = spacy.load("pt_core_news_lg")
    
    #Pôr os verbos das frases com o seu lema
    doc = nlp(pharse)

    phrase_lema = " ".join(token.lemma_ if token.pos_ == "VERB" else token.text for token in doc)

    normalized_str = unicodedata.normalize('NFD', phrase_lema)

    noAccentPharse = normalized_str.encode('ascii', 'ignore').decode('utf-8')

    #print(noAccentPharse)

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
    #print("Words_List: " + str(words_list))
    #Contador de elementos que alteram a polaridade
    nr_pol = 0

    #Contador de elementos que alteram a polaridade positivamente
    nr_plus = 0

    #Contador de elementos que alteram a polaridade negativamente
    nr_minus = 0

    for key in ["TERM","EMOJI",""]:
        
        pals = db[key]

        if key == "TERM":
            #print("\nTermos:\n")
            for pal in pals.keys():
                if pal in noAccentPharse:
                    occurrences = find_pos(pal, noAccentPharse)
                    for pos in occurrences:
                        before = words_before(pos, noAccentPharse)
                        split = before.split() # Pegar a última palavra da string 'before' após dividi-la
                        if len(split) > 1:
                            previous_word = split[1]
                        else:
                            if before == " ":
                                previous_word = ""
                            else:
                                previous_word = before
                        if before in db["NEGT"].keys():
                            nr_pol += 2
                            polaridade = pals[pal]["Polaridade"] * -1
                            pol += polaridade
                            #print("Palavra: " + before + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade)) 
                        elif previous_word in db["NEG"].keys() and previous_word not in negtermos:
                            nr_pol += 2
                            polaridade = pals[pal]["Polaridade"] * -1
                            pol += polaridade
                            #print("Palavra: " + previous_word + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade)) 
                        elif before in db["INCR"].keys() or previous_word in db["INCR"].keys():
                            nr_pol += 2
                            polaridade = pals[pal]["Polaridade"] * 2
                            pol += polaridade
                            #if before in db["INCR"].keys():
                                #print("Palavra: " + before + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade))
                            #else: 
                                #print("Palavra: " + previous_word + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade))
                        elif before in db["DECR"].keys() or previous_word in db["DECR"].keys():
                            nr_pol = 2
                            polaridade = pals[pal]["Polaridade"] / 2
                            pol += polaridade
                            #if before in db["INCR"].keys():
                                #print("Palavra: " + before + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade))
                            #else: 
                                #print("Palavra: " + previous_word + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade))
                        else:
                            nr_pol = 1
                            polaridade = pals[pal]["Polaridade"]
                            pol += polaridade
                            #print("Palavra: " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade)) 
                        
                        if polaridade > 0:
                            nr_plus += 1
                        elif polaridade < 0:
                            nr_minus += 1

        elif key == "EMOJI":
            #print("\nEmojis:\n")
            for pal in pals.keys():
                if pal in pharse:
                    occr = pharse.count(pal)
                    polaridade = (pals[pal]["Polaridade"] * occr)
                    pol += polaridade
                    #print("Emoji: " + pal + " NºOcorrência:" + str(occr) + " Polaridade:" + str(polaridade))
                    if polaridade > 0:
                        nr_plus += occr
                    elif polaridade < 0:
                        nr_minus += occr

        elif key == "":
            #print("\nPalavras:\n")
            for pal in pals.keys():
                if pal in words_list:
                    occurrences = find_pos(pal, noAccentPharse)
                    for pos in occurrences:
                        before = words_before(pos, noAccentPharse)
                        split = before.split()
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
                                #print("Palavra: " + before + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade)) 
                            elif previous_word in db["NEG"].keys() and previous_word not in negtermos:
                                nr_pol += 2
                                polaridade = pals[pal]["Polaridade"] * -1
                                pol += polaridade
                                #print("Palavra: " + previous_word + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade)) 
                            elif before in db["INCR"].keys() or previous_word in db["INCR"].keys():
                                nr_pol += 2
                                polaridade = pals[pal]["Polaridade"] * 2
                                pol += polaridade
                                #if before in db["INCR"].keys():
                                    #print("Palavra: " + before + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade))
                                #else: 
                                    #print("Palavra: " + previous_word + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade)) 
                            elif before in db["DECR"].keys() or previous_word in db["DECR"].keys():
                                nr_pol += 2
                                polaridade = pals[pal]["Polaridade"] / 2
                                pol += polaridade
                                #if before in db["INCR"].keys():
                                #    print("Palavra: " + before + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade))
                                #else: 
                                #    print("Palavra: " + previous_word + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade))
                            else:
                                nr_pol += 1
                                polaridade = pals[pal]["Polaridade"]
                                pol += polaridade
                                #print("Palavra: " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade))

                            if polaridade > 0:
                                nr_plus += 1
                            elif polaridade < 0:
                                nr_minus += 1
    if nr_pol == 0:
        result = 0
    else:                    
        result = pol / nr_pol
    return result

db = {}

with open("../final_lema.csv", encoding='utf-8') as csvfile:
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

pasta_capitulos = "capitulos"

sentimentos = []

for capitulo in range(1, 18):
    nome_arquivo = f"{capitulo}.txt"
    
    path = os.path.join(pasta_capitulos, nome_arquivo)
    
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            phrase = f.read()
        
        score = calcPol(phrase,db)
        
        sentimentos.append(score)

# Definir cores :)
norm = Normalize(vmin=-1, vmax=1)
cores = [plt.cm.RdYlGn(norm(sentimento)) for sentimento in sentimentos]

# Gráfico com as cores :D
plt.bar(range(1, 18), sentimentos, color=cores, edgecolor='black')

# Rótulos :P
plt.title('Sentimento por Capítulo (Nossa Versão)')
plt.xlabel('Capítulo')
plt.ylabel('Sentimento')
plt.ylim(-1, 1)

# Barra com a escala das cores :3
sm = ScalarMappable(cmap=plt.cm.RdYlGn, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm)
cbar.set_label('Sentimento')

# Mostrar o Histograma :O
plt.grid(axis='y')
#plt.show()

plt.savefig('ourHP.png', dpi=300)