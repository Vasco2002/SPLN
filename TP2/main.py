import json

from ir import search
from data_fetch import dataFetch
from format_info import formatInfo
from qa import answer

# Loop para permitir que o usuário faça perguntas
while True:
    # Input da pergunta
    pergunta = input("Faça uma pergunta (ou 'sair' para terminar): ")

    # Verificar se o usuário quer sair
    if pergunta.lower() == 'sair':
        print("Saindo do programa...")
        break

    results = search(pergunta)
    
    """
    for result in results:
        print(f"Similarity: {result['similarity']}")
        print(f"Document: {result['notes']}\n")
    """

    dataFetch(pergunta)

    formatInfo(pergunta)

    resposta = answer(pergunta)

    # Write question and answer to a JSON file
    output_file = "respostas.json"
    with open(output_file, "a+") as file:
        file_data = json.load(file) if file.readable() else []
        file_data.append({"pergunta": pergunta, "resposta": resposta})
        file.seek(0)
        json.dump(file_data, file, indent=4)