# Information retrieval (IR)

O sistema de recuperação de informação (IR) tem como objetivo encontrar os documentos mais relevantes com base na pergunta desenvolvida pelo o usuário. Para esse efeito criamos a *script* `ir.py` que segue a metodologia seguinte: 

1. **Carregamento e Pré-processamento dos Dados:** 

Iniciamos o processo carregando os dados a partir do ficheiro dre.json, fornecido pelo professor, que contém os resumos, *ids*, e datas de publicação dos documentos do Diário da República. 

Utilizamos a biblioteca *nltk* para carregar e aplicar stopwords em português, removendo palavras comuns que não contribuem significativamente para a diferenciação dos documentos.

Em seguida, definimos uma função de pré-processamento `preprocess` para normalizar o texto, tokenizar e remover stopwords, pré-processassando os resumos dos documentos extraídos dos metadados.

2. **Criação do Modelo TF-IDF:** 

Usamos a biblioteca *gensim* para criar um dicionário e um conjunto de documentos *Bag of Words* (BoW) dos documentos pré-processados, e de seguinda treinamos um modelo TF-IDF com este BoW.

3. **Indexação e Cálculo de Similaridade**

Construímos um índice de similaridade de documentos usando a matriz *SparseMatrixSimilarity* da biblioteca *gensim*. Este índice permite calcular a similaridade entre a consulta e os documentos do conjunto.

4. **Consulta e Recuperação de Documentos**

Implementamos a função de busca `search` que recebe uma consulta, pré-processa a consulta, converte-a para a representação BoW e TF-IDF, e calcula a similaridade com todos os documentos do índice. Os documentos mais relevantes são ordenados e retornados como resultado, guardando o resultado na pasta `similares`.

# Extrair Dados

Após a seleção dos documentos mais relevantes, o próximo passo é recolher os textos relacionados a estes do ficheiro *SQL*. 

A ideia inicial, seria carregar o *script SQL* para um SBD, contudo, devido ao tamanho deste ficheiro, nenhuma das nossas máquinas consegui abrir-lo. Como solução construímos um *script* em *Python* que terá como objetivo recolher os textos associados aos *ids* recolhidos na faze anterior.

O *script* irá ler linha a linha, o ficheiro com as *queries SQL* e posteriormente, utilizando a biblioteca *re* de *python* compara-se o texto com a expressão regular construída. Dessa expressão regular, retiramos o segundo valor que estiver dentro da *query* e verificamos se este pertence aos *ids* dos diplomas que estão a ser procurados.

Se o seu id estiver dentro de um dos de interesse, a sua query será armazenada no ficheiro para ser posteriormente processada. Se não estiver é ignorada.

Contudo, como estamos a ler linha a linha, as queries que são do nosso interesse elas encontra-se em multiplas linhas, por isso foi necessário um cuidado inicial. Como as *queries SQL* apresentam todas o mesmo inicio ( ```INSERT INTO table\_name VALUES (...); ```), capturamos todas as linhas desde da inicial até ser encontrado o padrão que indique que a *query* acabou, neste caso, ```);```. Assim é possível lidar com caso em que as queries de multiplas linhas, sejam totalmente capturadas e processadas.

No final do processamento do ficheiro *SQL*, toda a informação recolhida é armazenada dentro de um fichiero *.json* para sofrer um novo tratamento na fase seguinte, que por sua vez se encontra na pasta `prepared_data`.

# Formatar Dados        

Depois de termos extraído todas as informações dos documentos, formatamos toda a informação extraída na fase anterior através da script `format_info.py`, retirando apenas a informação relevante para o contexto da consulta (o texto dos documentos) e retirando termos desnecessários para o contexto, tais como ```<div>```, ```<a href=```, entre outros.

Para isso usamos *regex* para extraír exclusivamente os textos de cada documento relevante e usamos a função `replace` para remover os tais temas desnecessários para o contexto. O ficheiro de texto onde é guardado esta informação é adicionado à pasta `information`.

# Question and Answering (Q&A)

Depois de termos coletado toda a informação relevante dos documentos e formatado essa informação, passamos para a fase do sistema de Perguntas e Respostas (Q&A).

Para isso utilizamos a biblioteca *transformers* da *Hugging Face* para inicializar uma pipeline de Q&A com um modelo pré-treinado em português. O modelo usado foi "lfcc/bert-portuguese-squad", que é adequado para tarefas de Q&A em português.

Usamos o ficheiro .txt, gerado na fase anterior, como contexto para o sistema e a consulta realizada no ínicio pelo utilizador como a pergunta para o sistema.

No fim o sistema fornece a resposta perante a consulta fornecida pelo o usuário no início. O processo total leva mais ou menos cinco minutos a realizar.

A script qa.py acaba por realizar todas as fazes ao mesmo tempo, acabando por guardar todos os resultados no ficheiro `respostas.json`.

# Instruções de Execução

Correr a script `main.py`, inserir pelo o terminal a pergunta que deseja efetuar e esperar pelos os resultados. Quando desejar sair, basta apenas escrever "sair".