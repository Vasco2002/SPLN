import os
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

analyzer = SentimentIntensityAnalyzer()

pasta_capitulos = "chapters"

sentimentos = []

for capitulo in range(1, 18):
    nome_arquivo = f"{capitulo}.txt"
    
    path = os.path.join(pasta_capitulos, nome_arquivo)
    
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            texto = f.read()
        
        scores = analyzer.polarity_scores(texto)
        
        sentimentos.append(scores['compound'])

# Definir cores :)
norm = Normalize(vmin=-1, vmax=1)
cores = [plt.cm.RdYlGn(norm(sentimento)) for sentimento in sentimentos]

# Gráfico com as cores :D
plt.bar(range(1, 18), sentimentos, color=cores, edgecolor='black')

# Rótulos :P
plt.title('Sentimento por Capítulo')
plt.xlabel('Capítulo')
plt.ylabel('Sentimento')
plt.ylim(-1, 1)

# Barra com a escala das cores :3
sm = ScalarMappable(cmap=plt.cm.RdYlGn, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm)
cbar.set_label('Sentimento')

# Mostrar o Histograma :O
plt.grid(axis='y')
plt.show()
