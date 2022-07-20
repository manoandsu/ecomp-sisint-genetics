"""
Autor: Anderson Andrade Cardoso e Victor Aury Freitas
Adaptado de genetic2022.py
Trabalho 1 - Galeria """

from random import randint, random, getrandbits
from operator import add
from functools import reduce
from bitstring import BitArray

def individual(length , rand=True):
    # Cria um membro da populacao, array de bits aleatorios
    return BitArray(uint=getrandbits(length), length=length) if rand else BitArray(length)

def population(count, length):
    # Cria a populacao
    return [ individual(length) for x in range(count) ]

def fitness(individual, photos, MAX_TAG):
    """
        O fitness do individuo sera a soma de curtidas das fotos escolhidas ou ZERO, caso ultrapasse o MAX_TAG (limite de marcações).
    """

    taggings, likes = 0, 0

    # Para cada bit
    for idx, chosen in enumerate(individual):
        # Se a foto for escolhida para a galeria, incrementa marcações e curtidas com o valor da foto
        if chosen:
            taggings += photos[idx][0]
            likes += photos[idx][1]

            # Se exceder o limite de marcações fornecido, retorna fitness 0
            if taggings > MAX_TAG:
                return 0

    return likes

def taggings(individual, photos):
    taggings = 0

    for idx, chosen in enumerate(individual):
        if chosen:
            taggings += photos[idx][0]

    return taggings


def media_fitness(pop, photos, MAX_TAG):
    # Media de fitness da populacao
    summed = reduce(add, (fitness(x, photos, MAX_TAG) for x in pop))
    sum_peso = 10*reduce(add, (taggings(x, photos) for x in pop))
    len_ = len(pop)*1.0
    return (summed/len_, sum_peso/len_)

def best_fitness(pop, photos, MAX_TAG):
    #Melhor fitness da populacao
    graded = [(x, fitness(x, photos, MAX_TAG)) for x in pop]
    best = max(graded, key=lambda graded:graded[1])

    return (best[1], 10 * taggings(best[0], photos))

def stalin_select(fit_pop):
    max_fitness = max(max(fp[0] for fp in fit_pop), 1)
    
    return [ ind for (fit, ind) in fit_pop if fit/max_fitness <= random() ]


def evolve(pop, photos, MAX_TAG, elite=5, r_parents=0.4, mutate=0.01, selection="roleta", crossover='mask'):
    # Tabula cada individuo e o seu fitness
    graded = [(fitness(x, photos, MAX_TAG), x) for x in pop]

    # Ordena for fitness
    graded = sorted(graded, key=lambda graded: graded[0], reverse=True)

    # Pais
    parents_length = int(len(graded)*r_parents)

    # Elitismo
    if elite:
        parents = [x[1] for x in graded][0:elite]
    else:
        parents = []

    # seleção
    if selection == "roleta":
        sum_fit = sum(fp[0] for fp in graded) # soma de todos fitness da população

        while len(parents) < parents_length:
            pick = random() 
            acum_fit = 0
            for i, (fit, individual) in enumerate(graded):
                acum_fit += fit/max(1, sum_fit) # Distribuicao acumulativa normalizada
                
                if acum_fit > pick:
                    parents.append(individual)
                    break
    elif selection == 'stalin':
        selected = stalin_select(graded)
        parents += selected[:min(len(selected), parents_length)]
    
    
    parents_length = len(parents)

    # descobre quantos filhos terao que ser gerados alem da elite e aleatorios
    desired_length = len(pop) - parents_length
    
    children = []
    # geração de filhos
    while len(children) < desired_length:

        #escolhe pai e mae no conjunto de pais
        male = randint(0, parents_length -1)
        female = randint(0, parents_length -1)
        
        if male != female:
            male = parents[male]
            female = parents[female]

            # crossover
            if crossover == 'mask':
                # gera filho usando uma máscara aleatória que
                # define se o gene vem da mãe ou do pai
                mask = BitArray(uint=getrandbits(len(male)), length=len(male))
                child = BitArray(male[i] if mask[i] else female[i] for i in range(len(mask)))
            elif crossover == 'singlepoint':
                # gera filho metade de cada
                half = randint(2, len(male))
                child = male[:half] + female[half:]
            else:
                raise NotImplementedError("Unimplemented crossover method")
        
            # adiciona novo filho a lista de filhos
            children.append(child)

    # Adiciona lista de filhos na nova populacao
    parents.extend(children)
    # mutate some individuals
    for i, individual in enumerate(parents):
        if mutate > random():
            pos_to_mutate = randint(0, len(individual)-1)
            individual.invert(pos_to_mutate)
    return parents
