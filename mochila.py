# Autor: Anderson Andrade Cardoso e Victor Aury Freitas. 
# Adaptado de mochila.py de Victor Barros Coch
# Trabalho 1 - Problema do Álbum

from matplotlib import pyplot as plt
from genetic2022_galeria import *
from bruteforce import *
import time

# Métodos de Seleção
selection_methods = ('roleta', 'stalin')

# Métodos de Crossover
crossover_methods = ('mask', 'singlepoint')

# Conjunto de fotos (taggings, likes)
itens = [
    (12, 24), (84, 51), (11, 92), (77, 39), (93, 57), (28, 88), (96, 82), (11, 82), (10, 70), (4, 110),
    (7, 21), (3, 84), (2, 30), (7, 81), (9, 99), (10, 69), (24, 55), (11, 30), (2, 40), (17, 83)
]

# Numero de fotos
n_photos = len(itens)

# Limite de taggings na galeria
MAX_TAG = 350           

print(f'Numero de Fotos: {n_photos}')

# Número de Gerações para Testar
epochs = 800

# Tamanho da População
p_count = 100

# Taxa de Mutação
mutation_rate = .1

# Nùmero de Indivíduos Selecionados no Elitismo
elite_amount = 50

# Taxa de Pais Usadas no Crossover
parent_rate = .8


# Inicializa os Plots
plt1 = plt.figure()
ax1 = plt.axes()
plt.title("Maior Fitness")
plt1.text(0.05, 0.9,
    f"Epochs: {epochs}, População: {p_count}\nNúmero de fotos: {n_photos}\nMax Taggings: {MAX_TAG}"
)
plt1.text(0.6, 0.9,
    f"Taxa de Mutação: {mutation_rate}\nElitismo: {elite_amount}\nTaxa de pais: {parent_rate}"
)

plt2 = plt.figure()
ax2 = plt.axes()
plt.title("Fitness Média")
plt2.text(0.05, 0.9,
    f"Epochs: {epochs}, População: {p_count}\nNúmero de fotos: {n_photos}\nMax Taggings: {MAX_TAG}"
)
plt2.text(0.6, 0.9,
    f"Taxa de Mutação: {mutation_rate}\nElitismo: {elite_amount}\nTaxa de pais: {parent_rate}"
)


# Computa a Solução Ótima por Força Bruta
t0 = time.time()
best = run_bruteforce(itens, MAX_TAG)
t1 = time.time()
print("Tempo Brute force: " + str(t1-t0))
ax1.plot([best[0]]*epochs)
ax2.plot([best[0]]*epochs)

# Testa Todas as Combinações dos Métodos de Crossover e Seleção
for sel in selection_methods:
    for cros in crossover_methods:

        # Criando a populacao
        p = population(p_count, n_photos)
        fitness_history = []


        t0 = time.time()
        for i in range(epochs):
            media_fit, media_peso = media_fitness(p, itens, MAX_TAG)
            best_fit, weight = best_fitness(p, itens, MAX_TAG)

            p = evolve(p, itens, MAX_TAG, elite_amount, parent_rate, mutation_rate, selection=sel, crossover=cros)

            fitness_history.append([best_fit, media_fit])

        t1 = time.time()

        print(f"Tempo AG({sel, cros}): "+str(t1-t0))

        print(f"Individuo AG: { sorted(p, key=lambda p:p[0])[-1] }, Valor: { fitness_history[-1][0] }\n" )

        ax1.plot([f[0] for f in fitness_history])
        ax2.plot([f[1] for f in fitness_history])

ax1.legend( [ "Força Bruta" ] + [ f"{sel}, {cros}" for sel in selection_methods for cros in crossover_methods] )
ax2.legend( [ "Força Bruta" ] + [ f"{sel}, {cros}" for sel in selection_methods for cros in crossover_methods] )

ax1.grid(True)
ax2.grid(True)

plt.show()
