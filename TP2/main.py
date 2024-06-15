import json
import os  # For checking if file exists

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
    
    # Read existing data from file, or initialize as empty list
    file_data = []
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        with open(output_file, "r") as file:
            try:
                file_data = json.load(file)
            except json.JSONDecodeError:
                print(f"Error loading JSON from {output_file}. Using empty list instead.")

    # Append new question-answer pair
    file_data.append({"pergunta": pergunta, "resposta": resposta})

    # Write back to file
    with open(output_file, "w") as file:
        json.dump(file_data, file, indent=4)


