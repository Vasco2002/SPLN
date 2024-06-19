import json
from gensim.utils import tokenize
import nltk
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.similarities import SparseMatrixSimilarity

# Converte o texto para minúsculas, tokeniza-o e remove stopwords
def preprocess(line,stopwords):
    line = line.lower()
    tokens = tokenize(line)
    tokens = [token for token in tokens if token not in stopwords]
    return list(tokens)

def search(query, top_n=5):
    output_file=f'similares/{query.replace(" ","_")}.json'

    # carrega a lista de stopwords em português.
    stopwords = nltk.corpus.stopwords.words('portuguese')

    with open('data/dre.json', 'r', encoding='utf-8') as f:
        documents = json.load(f)

    # Pré-processa as notas (texto) de cada documento, tokenizando e removendo stopwords.
    sentences = []
    notes = [doc['notes'] for doc in documents]
    for line in notes:
        sentences.append(preprocess(line,stopwords))

    # Cria um dicionário de termos e converte os textos em uma representação bag-of-words (BoW).
    dictionary = Dictionary(sentences)
    corpus_bow = [dictionary.doc2bow(sent) for sent in sentences]

    # Treina um modelo TF-IDF usando o corpus BoW.
    tfidf_model = TfidfModel(corpus_bow, normalize=True)

    # Cria um índice de similaridade esparsa para encontrar similaridades entre os documentos.
    index = SparseMatrixSimilarity(tfidf_model[corpus_bow], num_docs=len(corpus_bow), num_terms=len(dictionary))

    # Pré-processa a consulta, converte-a para BoW e calcula a sua representação TF-IDF, depois calcula a similaridade com todos os documentos.
    query_tokenized = preprocess(query,stopwords)
    query_bow = dictionary.doc2bow(query_tokenized)
    tfidf_query = tfidf_model[query_bow]
    sims = index[tfidf_query]
    
    # Ordena os documentos pela similaridade em ordem decrescente e seleciona os top_n resultados.
    sims_ordered = sorted(enumerate(sims), key=lambda item: item[1], reverse=True)
    results = []
    for idx, sim in sims_ordered[:top_n]:
        results.append({
            'similarity': float(sim),
            'id': documents[idx]['id'],
            'date': documents[idx]['date'],
            'notes': documents[idx]['notes']
        })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    return results