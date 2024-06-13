from transformers import pipeline

tema = "IRS"

# Função para ler o contexto de um arquivo
def ler_contexto(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Caminho para o arquivo de contexto
file_path = 'information/IRS_info.txt'

# Ler o contexto do arquivo
context = ler_contexto(file_path)

# Inicializar o modelo de perguntas e respostas em português
question_answerer = pipeline("question-answering", model="lfcc/bert-portuguese-squad")

# Imprimir o contexto
print("Tema:")
print(tema)
print("--------------------------")

# Loop para permitir que o usuário faça perguntas
while True:
    # Input da pergunta
    pergunta = input("Faça uma pergunta (ou 'sair' para terminar): ")

    # Verificar se o usuário quer sair
    if pergunta.lower() == 'sair':
        print("Saindo do programa...")
        break

    # Obter e imprimir a resposta
    result = question_answerer(question=pergunta, context=context)
    print(f"Resposta: {result['answer']} | Score: {result['score']}")
