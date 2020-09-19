from ypstruct import structure
import random
import numpy as np
import operator


# Função que calcula o fitness de um cromossomo somando todas as distancias do percurso
def calc_fitness(cities, chromosome):
    res = 0
    for i in range(len(chromosome) - 1):
        res += cities.distances[chromosome[i]][chromosome[i + 1]]
    return res


# Cria a polupação inicial e ja insere os genes de BsB no inicio e fim do cromossomo
# Ela recebe uma matriz com todas as distancias entre as cidades e partir dela cria uma lista aleatória
def create_initial_population(cities, config):
    initial_population = structure()
    initial_population.cost = 0
    initial_population.chromosome = list(range(0, 9))
    initial_population = initial_population.repeat(config.population_size)
    min_cost = structure()
    min_cost.cost = float('inf')
    for i in range(config.population_size):
        random.shuffle(initial_population[i].chromosome)
        initial_population[i].chromosome.insert(0, 9)
        initial_population[i].chromosome.insert(10, 9)
        initial_population[i].cost = calc_fitness(cities, initial_population[i].chromosome)
        if initial_population[i].cost < min_cost.cost:
            min_cost = initial_population[i]

    return initial_population, min_cost


# Recebe um cromossomo e uma probabilidade onde a cada gene terá x por cento de chances de ser
# alterado pelo valor de outro gene no mesmo chromossomo
def mutation(offspring, mutation_probability):
    x = offspring.copy()
    for i in range(1, len(x) - 1):
        prob = np.random.randint(1, 100)
        if prob <= mutation_probability and i != 0 and i != 10:
            index = np.random.randint(1, 9)
            aux = x[index]
            x[index] = x[i]
            x[i] = aux
    return x


# Reprodução onde um intervalo do cromossomo é sorteado aleatóriamente e é feita o crossover onde é
# pego um intervalo do parent 1 e outros dois intervalos do parent 2 e assim se cria um novo filho
# A função se baseia em pegar cada gene no intervalo escolhido e procula-lo no segundo gene onde os
# mesmos são trocados de modo a nunca existir um cromossomo com dois ou mais genes indenticos
def crossover_two_cut(parent1, parent2):
    cut_index1 = np.random.randint(2, 8)
    cut_index2 = np.random.randint(2, 8)

    if cut_index1 > cut_index2:
        aux = cut_index1
        cut_index1 = cut_index2
        cut_index2 = aux

    first = parent1.chromosome
    first2 = parent2.chromosome.copy()
    for i in range(cut_index1, cut_index2):
        index = get_index_gene(first2, first[i])
        aux = first2[i]
        first2[i] = first[i]
        first2[index] = aux

    return first2


# Recebe um cromossomo e um número de cidade que irá procurar e retorna o index da mesma no cromossomo
def get_index_gene(chromosome, x):
    for i in range(len(chromosome)):
        if chromosome[i] == x:
            return i
    return -1


# Reprodução onde o cromossomo parent1 e parent2 é cortado em um indice escolhido aleatóriamente para que se
# possa criar um filho com uma parte do cromossomo de cada pai
# A função se baseia em pegar cada gene no anterior ao corte no parent1 e procula-lo no segundo gene onde os
# mesmos são trocados de modo a nunca existir um cromossomo com dois ou mais genes indenticos no mesmo lado
# do corte no parent1 e no parent2
def crossover_one_cut(parent1, parent2):
    cut_index = np.random.randint(2, 8)
    first = parent1.chromosome[0:cut_index]
    first2 = parent2.chromosome.copy()
    for i in range(1, cut_index):
        index = get_index_gene(first2, first[i])
        aux = first2[i]
        first2[i] = first[i]
        first2[index] = aux

    return first2


# Funcao que cuida da reproducao do cromossomo
# Esta disponivel a reproducao por corte em um ponto e em multi pontos onde cada tipo de reproducao tem
# 50% de chances de ocorrer
# Apos a reproducao é feita a mutacao e em seguida e gerado um novo filho com o seu fitness ja calculado
def crossover(cities, parent1, parent2, config):
    probability = np.random.randint(0, 100)
    offspring = structure()

    if probability < 50:
        chromosome = crossover_one_cut(parent1, parent2)
    else:
        chromosome = crossover_two_cut(parent1, parent2)

    chromosome = mutation(chromosome, config.mutation_probability)
    offspring.cost = calc_fitness(cities, chromosome)
    offspring.chromosome = chromosome

    return offspring


# Dada uma lista de cidades, duas sao selecionadas ao acaso de forma que numca sera retornado duas cidades
# identicas
def selection(p):
    a = np.random.randint(0, len(p))
    b = np.random.randint(0, len(p))
    while a == b:
        b = np.random.randint(0, len(p))

    return a, b


# Funcao que faz um corte na populacao e representa a selecao natural
# A populacao é ranekada do mais propenso (com menor custo) para o menos propenso (maior custo)
# Aqui e utilizado o parametro cut_randomness onde e responsavel por tornar a lista ordenada mais
# aleatoria possivelmente salvando assim cromossomos que pela selecao seriam menos propensos a dar
# se reproduzirem
def cut_population(population, config):
    population = sorted(population, key=operator.attrgetter('cost'))
    for i in range(int(config.cut_randomness)):
        a, b = selection(population)
        aux = population[a]
        population[a] = population[b]
        population[b] = aux
    population = population[0:config.population_size]

    return population


# Funcao que exibe os nomes das cidades de um dado cromossomo
def print_way(cities, chromosome):
    print("{} -> {} -> {} -> {} -> {} -> {} -> {} -> {} -> {} -> {} -> {}".format(
        cities.name[chromosome[0]],
        cities.name[chromosome[1]],
        cities.name[chromosome[2]],
        cities.name[chromosome[3]],
        cities.name[chromosome[4]],
        cities.name[chromosome[5]],
        cities.name[chromosome[6]],
        cities.name[chromosome[7]],
        cities.name[chromosome[8]],
        cities.name[chromosome[9]],
        cities.name[chromosome[10]]
    ))


# Funcao principal que executa o algoritmo genetico
# Ela gera a populacao inicial
# Em seguida inicia um loop com o numero de interacoes
# Dentro dele existe o loop responsavel por gerar cada novo integrante da nova populacao
# onde dois cromossomos serao escolhidos aleatoriamente para serem os pais e gerarem um novo filho
# Apos a gerancao da populacao, a populacao antiga e a nova sao enviadas a funcao
# cut_population onde sera decidido quem continuara na populacao e quem sera removido
def run(cities, config):
    population, min_cost = create_initial_population(cities, config)
    for i in range(config.number_iterations):
        for x in population:
            if min_cost.cost > x.cost:
                min_cost.cost = x.cost
                min_cost.chromosome = x.chromosome

        new_population = []
        for i in range(config.population_size):
            parent1, parent2 = selection(population)
            new_chromosome = crossover(cities, population[parent1], population[parent2], config)
            new_population.append(new_chromosome)
            print_way(cities, new_chromosome.chromosome)
        population = cut_population(population + new_population, config)

    print("------------------------First population-------------------------")
    for x in population:
        print(x.chromosome)

    print("|------------ Result --------------|")
    print_way(cities, min_cost.chromosome)
    print("Min cost = {}".format(min_cost.chromosome))
    print("Fitness min cost = {}".format(calc_fitness(cities, min_cost.chromosome)))
