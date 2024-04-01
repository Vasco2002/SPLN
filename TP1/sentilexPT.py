#!/usr/bin/python3
'''
Name 
    sentilexPT - Calculates words polarity in a text

SYNOPSIS
    sentilexPT [options]
    option: 
        -a: Total number of words
        -n: Number of words with negative polarity
        -p: Number of words with positive polarity
        -f [file_directory]: Calculates polarity of the file introduced
        -t [phrase]: Calculates polarity of the phrase introduced

DESCRIPTIONS

'''

from jjcli import *
import csv
import unicodedata
import spacy
import sys
import os
from spacy import displacy

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
    if second == -1:
        return substring[second+ 1:third]

    return substring[first + 1:second] + " " + substring[second+ 1:third]

def remover_pontuacao(lista_palavras):
    return [palavra for palavra in lista_palavras if palavra.isalpha()]


def main():
    cl = clfilter("anpf:t:", doc=__doc__) ## Option values in cl.opt dictionary

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

    if "-f" in cl.opt and "-t" in cl.opt:
        print("Por favor insira apenas uma das opções: '-f' ou '-t'.")
        sys.exit()
    elif "-f" in cl.opt:
        path = cl.opt["-f"]     
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                pharse = f.read()
        else:
            print("A diretoria introduzida é inválida.")
            sys.exit()
    elif "-t" in cl.opt:
        pharse = cl.opt["-t"]
    else:
        pharse = "nao quero sorrir." #"muito adoravel, Ele não ser muito adoravel" #"Eu sou incrivelmente muito adoravel"
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
                            print("Palavra: " + before + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade)) 
                        elif previous_word in db["NEG"].keys() and previous_word not in negtermos:
                            nr_pol += 2
                            polaridade = pals[pal]["Polaridade"] * -1
                            pol += polaridade
                            print("Palavra: " + previous_word + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade)) 
                        elif before in db["INCR"].keys() or previous_word in db["INCR"].keys():
                            nr_pol += 2
                            polaridade = pals[pal]["Polaridade"] * 2
                            pol += polaridade
                            if before in db["INCR"].keys():
                                print("Palavra: " + before + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade))
                            else: 
                                print("Palavra: " + previous_word + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade))
                        elif before in db["DECR"].keys() or previous_word in db["DECR"].keys():
                            nr_pol = 2
                            polaridade = pals[pal]["Polaridade"] / 2
                            pol += polaridade
                            if before in db["INCR"].keys():
                                print("Palavra: " + before + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade))
                            else: 
                                print("Palavra: " + previous_word + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade))
                        else:
                            nr_pol = 1
                            polaridade = pals[pal]["Polaridade"]
                            pol += polaridade
                            print("Palavra: " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade)) 
                        
                        if polaridade > 0:
                            nr_plus += 1
                        elif polaridade < 0:
                            nr_minus += 1

        elif key == "EMOJI":
            print("\nEmojis:\n")
            for pal in pals.keys():
                if pal in pharse:
                    occr = pharse.count(pal)
                    polaridade = (pals[pal]["Polaridade"] * occr)
                    pol += polaridade
                    print("Emoji: " + pal + " NºOcorrência:" + str(occr) + " Polaridade:" + str(polaridade))
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
                        split = before.split()
                        if len(split) > 1:
                            previous_word = split[1]
                        else:
                            if before == " ":
                                previous_word = ""
                            else:
                                previous_word = before
                        if previous_word + " " + pal not in termos and previous_word + " " + pal not in negtermos or before + " " + pal not in termos:
                            if before in db["NEGT"].keys():
                                nr_pol += 2
                                polaridade = pals[pal]["Polaridade"] * -1
                                pol += polaridade
                                print("Palavra: " + before + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade)) 
                            elif previous_word in db["NEG"].keys() and previous_word not in negtermos:
                                nr_pol += 2
                                polaridade = pals[pal]["Polaridade"] * -1
                                pol += polaridade
                                print("Palavra: " + previous_word + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade)) 
                            elif before in db["INCR"].keys() or previous_word in db["INCR"].keys():
                                nr_pol += 2
                                polaridade = pals[pal]["Polaridade"] * 2
                                pol += polaridade
                                if before in db["INCR"].keys():
                                    print("Palavra: " + before + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade))
                                else: 
                                    print("Palavra: " + previous_word + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade)) 
                            elif before in db["DECR"].keys() or previous_word in db["DECR"].keys():
                                nr_pol += 2
                                polaridade = pals[pal]["Polaridade"] / 2
                                pol += polaridade
                                if before in db["INCR"].keys():
                                    print("Palavra: " + before + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade))
                                else: 
                                    print("Palavra: " + previous_word + " " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade))
                            else:
                                nr_pol += 1
                                polaridade = pals[pal]["Polaridade"]
                                pol += polaridade
                                print("Palavra: " + pal + " Posição:" + str(pos) + " Polaridade:" + str(polaridade))

                            if polaridade > 0:
                                nr_plus += 1
                            elif polaridade < 0:
                                nr_minus += 1
                        
    result = pol / nr_pol

    if "-a" in cl.opt:
        print("\nNúmero de Palavras: " + str(len(remover_pontuacao(words_list))))

    if "-p" in cl.opt:
        print("\nNúmero de Elementos Positivos: " + str(nr_plus))

    if "-n" in cl.opt:
        print("\nNúmero de Elementos Negativos: " + str(nr_minus))

    print("\nPolaridade do Texto: " + str(result))

    #Um elemento é um conjunto de tipo especial(NEG, NEGT, INCR, DECR) + palavra/termo ou Emoji que altera a polaridade do texto

if __name__ == "__main__":
    main()