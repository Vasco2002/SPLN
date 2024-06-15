from transformers import pipeline

# Função para ler o contexto de um arquivo
def ler_contexto(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def answer(tema):
    # Caminho para o arquivo de contexto
    file_path = f'information/{tema.replace(" ","_")}_info.txt'

    # Ler o contexto do arquivo
    context = ler_contexto(file_path)

    # Inicializar o modelo de perguntas e respostas em português
    question_answerer = pipeline("question-answering", model="lfcc/bert-portuguese-squad")

    # Obter e imprimir a resposta
    result = question_answerer(question=tema, context=context)
    print(f"Resposta: {result['answer']} | Score: {round(result['score']*100,2)}")
    return result['answer']