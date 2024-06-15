import json
from gensim.utils import tokenize
import nltk
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.similarities import SparseMatrixSimilarity

# Função de pré-processamento
def preprocess(line,stopwords):
    line = line.lower()
    tokens = tokenize(line)
    tokens = [token for token in tokens if token not in stopwords]
    return list(tokens)

def search(query, top_n=5):
    output_file=f'similares/{query.replace(" ","_")}.json'

    # Carregar stopwords em português
    # nltk.download('stopwords')
    stopwords = nltk.corpus.stopwords.words('portuguese')

    # Carregar dados do arquivo JSON
    with open('data/dre.json', 'r', encoding='utf-8') as f:
        documents = json.load(f)

    # Pré-processar os resumos dos documentos
    sentences = []
    notes = [doc['notes'] for doc in documents]
    for line in notes:
        sentences.append(preprocess(line,stopwords))

    # Criar dicionário e corpus BoW
    dictionary = Dictionary(sentences)
    corpus_bow = [dictionary.doc2bow(sent) for sent in sentences]

    # Criar modelo TF-IDF
    tfidf_model = TfidfModel(corpus_bow, normalize=True)

    # Calcular a similaridade
    index = SparseMatrixSimilarity(tfidf_model[corpus_bow], num_docs=len(corpus_bow), num_terms=len(dictionary))

    # Pré-processar a consulta
    query_tokenized = preprocess(query,stopwords)
    
    # Converter a consulta para a representação BoW usando o dicionário
    query_bow = dictionary.doc2bow(query_tokenized)
    
    # Converter a consulta BoW para a representação TF-IDF
    tfidf_query = tfidf_model[query_bow]
    
    # Calcular a similaridade da consulta TF-IDF com todos os documentos
    sims = index[tfidf_query]
    
    # Ordenar os documentos por similaridade em ordem decrescente
    sims_ordered = sorted(enumerate(sims), key=lambda item: item[1], reverse=True)
    
    # Armazenar os resultados mais relevantes
    results = []
    for idx, sim in sims_ordered[:top_n]:
        results.append({
            'similarity': float(sim),
            'id': documents[idx]['id'],
            'date': documents[idx]['date'],
            'notes': documents[idx]['notes']
        })
    
    # Salvar os resultados em um arquivo JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    # Retornar os resultados
    return results