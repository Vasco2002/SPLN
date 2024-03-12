import csv
import os
import re

output_file_path = 'outputfile.txt'

#Lê o ficheiro "Siglas, acrónimos e abreviaturas.csv" e adiciona a informação dele ao ficheiro output
def csvAdd():
    csv_file_path = 'Data/Siglas, acrónimos e abreviaturas.csv'
    

    with open(csv_file_path, 'r', encoding='latin-1') as csv_file:
        # Caracteres nulos passam a ser uma string vazia
        csv_reader = csv.reader((line.replace('\0', '') for line in csv_file))
        
        # Passa à frente a primeira linha
        next(csv_reader)
        
        #Se o ficheiro output for vazio ou não existir cria um novo
        mode = 'a' if os.path.exists(output_file_path) and os.path.getsize(output_file_path) > 0 else 'w'
        
        with open(output_file_path, mode, encoding='utf-8') as txt_file:
            if txt_file.tell() != 0:
                txt_file.write('\n')

            for line in csv_reader:
                if len(line) >= 3:

                    designacao = line[1]
                    extenso = line[2]
                    
                    txt_file.write(f"{designacao} : {extenso}\n")

    print(f"A informação do ficheiro {csv_file_path} foi adicionada ao ficheiro {output_file_path}.\n")

#Adiciona a informação de ficheiros txt já traduzidos no fim do ficheiro output
def txtAddPT(txt_file_path):
    with open(output_file_path, 'a', encoding='utf-8') as output:
        try:
            with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
                output.write(txt_file.read())
                output.write('\n')
        except FileNotFoundError:
            print(f"Warning: Ficheiro não encontrado - {txt_file_path}")
        except Exception as e:
            print(f"Erro ao processar o ficheiro {txt_file_path}: {e}")

    print(f"A informação do ficheiro {txt_file_path} foi adicionada ao ficheiro {output_file_path}.\n")

#Adiciona a informação de ficheiros txt com a tradução no fim de cada acrónimo, no fim do ficheiro output
def txtAddEG(txt_file_path):
    with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
        with open(output_file_path, 'a', encoding='utf-8') as output:
            for line in txt_file:
                match = re.search(r'(\w+)\s*:\s*([^(]+)\s*\(([^)]+)\)', line)
                if match:
                    acronym, description, translation = match.groups()
                    output.write(f"{acronym.strip()} : {translation.strip()}\n")

    print(f"A informação do ficheiro {txt_file_path} foi adicionada ao ficheiro {output_file_path}.\n")

#Limpa o ficheiro output
def clearOutput():
    with open(output_file_path, 'w', encoding='utf-8') as output:
        output.truncate(0)
    
    print(f"O ficheiro {output_file_path} foi limpo.\n")

# Carrega as palavras comuns a partir do ficheiro criado por parseWords
def load_common_words():
    
    with open("out.txt", 'r', encoding='utf-8') as common_words_file:
        common_words = set(common_words_file.read().split())
    return common_words

#Colca os acrónimosde uma frase por extenso
def swapAcronyms(frase):
    with open(output_file_path, 'r', encoding='utf-8') as output:
        acronyms_info = output.read()

    # Obtém uma lista de tuplas (acrônimo, significado) a partir do conteúdo do arquivo
    acronyms_list = [line.split(' : ') for line in acronyms_info.strip().split('\n')]

    # Carrega as palavras comuns
    common_words = load_common_words()

    # Substitui os acrônimos na frase pelos seus significados
    for acronym, meaning in acronyms_list:
        # Garante que o acrônimo esteja isolado por espaços ou pontuações
        pattern = rf'\b{re.escape(acronym)}\b'
        # Verifica se a palavra correspondente ao acrônimo não está na lista de palavras comuns
        if acronym.lower() not in common_words:
            frase = re.sub(pattern, meaning.strip(), frase, flags=re.IGNORECASE)

    return frase

clearOutput()
csvAdd()
txtAddEG("Data/eg.txt")
txtAddPT("Data/pt.txt")
print(swapAcronyms("Hoje não me sinto muito bem tbh!"))
