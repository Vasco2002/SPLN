import csv
import spacy

# Carregar o modelo do SpaCy para o idioma português
nlp = spacy.load("pt_core_news_lg")

def ler_csv(nome_arquivo):
    with open(nome_arquivo, 'r', newline='', encoding='utf-8') as arquivo:
        return list(csv.reader(arquivo))

def escrever_csv(nome_arquivo, dados):
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
        escritor_csv = csv.writer(arquivo)
        escritor_csv.writerows(dados)

# Processamento e Tipagem dos Dados já existentes no arquivo CSV
def processar_dados(data, boosters, negadores):
    resultado = []
    for linha in data:
        elemento = linha[0]
        intensidade = linha[1] if len(linha) > 1 else "0"  #caso não tenha intensidade passa a ser 0
        tipo = linha[2] if len(linha) > 2 else ""
        
        # Dar tipo INCR ou DECR aos boosters
        if elemento in boosters:
            tipo = boosters[elemento]
        
        # Dar tipo NEG aos negadores
        elif elemento in negadores:
            tipo = "NEG"
        
        # Dar tipo TERM aos termos e tirar o tipo TBD aos elementos que não têm tipo
        elif tipo == "":
            if len(elemento.split()) > 1:
                tipo = "TERM"
            else:
                tipo = ""
        
        elif tipo == "EMOJI":
            tipo = "EMOJI"
            
        linha_processada = [elemento, intensidade, tipo]
        resultado.append(linha_processada)
    
    return resultado

data = ler_csv('sentiment.csv')

# Processar negadores
negate = ler_csv('datasets/negate.txt')
elementos_negativos = set(linha[0] for linha in negate)
elementos_data = set(linha[0] for linha in data)
# Adicionar elementos de negate.txt que não estão em sentiment.csv
for elemento in elementos_negativos:
    if elemento not in elementos_data:
        data.append([elemento, "0"])

# Processar boosters
booster = ler_csv('datasets/booster.txt')
elementos_booster = {}
for linha in booster:
    partes = linha[0].rsplit(' ', 1)
    elemento = partes[0]
    tipo = partes[1] if len(partes) > 1 else ""
    elementos_booster[elemento] = tipo

# Processar os dados
resultado = processar_dados(data, elementos_booster, elementos_negativos)

# Adicionar elementos de booster.txt que não estão em sentiment.csv
elementos_data = set(linha[0] for linha in data)
for elemento, tipo in elementos_booster.items():
    if elemento not in elementos_data:
        resultado.append([elemento, "0", tipo])

# Escrever o arquivo final.csv
escrever_csv('final.csv', resultado)

# Lematizar os verbos no arquivo final.csv
for linha in resultado:
    frase = nlp(linha[0])
    lema_frase = ' '.join([token.lemma_ for token in frase])
    linha[0] = lema_frase

# Escrever o arquivo final_lematizado.csv
escrever_csv('final_lema.csv', resultado)
