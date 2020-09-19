from ypstruct import structure
import random
import numpy as np
import operator


# Função que calcula o fitness de um cromossomo somando todas as diantancias do percurso
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
    min_cost.cost = 999999999
    for i in range(config.population_size):
        random.shuffle(initial_population[i].chromosome)
        initial_population[i].chromosome.insert(0, 9)
        initial_population[i].chromosome.insert(10, 9)
        initial_population[i].cost = calc_fitness(cities, initial_population[i].chromosome)
        if initial_population[i].cost < min_cost.cost:
            min_cost = initial_population[i]

    return initial_population, min_cost


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


def get_index_gene(chromosome, x):
    for i in range(len(chromosome)):
        if chromosome[i] == x:
            return i
    return -1


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


def selection(p):
    a = np.random.randint(0, len(p))
    b = np.random.randint(0, len(p))
    while a == b:
        b = np.random.randint(0, len(p))

    return a, b


def cut_population(population, config):
    population = sorted(population, key=operator.attrgetter('cost'))
    for i in range(int(config.cut_randomness)):
        a, b = selection(population)
        aux = population[a]
        population[a] = population[b]
        population[b] = aux
    population = population[0:config.population_size]

    return population


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


def run(cities, config):
    population, min_cost = create_initial_population(cities, config)

    # for x in population:
    #     print(x.chromosome)
    cpoy = population.copy()

    for i in range(config.number_iterations):
        costs = np.array([x.cost for x in population])
        avg_cost = np.mean(costs)
        if avg_cost != 0:
            costs = costs / avg_cost
        probs = np.exp(-1 * costs)
        # print("Interation number = {}".format(i))
        # print("Min value = {}".format(min_cost))
        for x in population:
            if min_cost.cost > x.cost:
                min_cost.cost = x.cost
                min_cost.chromosome = x.chromosome

        new_population = []
        # for i in range(config.population_size):
        for i in range(config.population_size):
            parent1, parent2 = selection(population)
            # = selection(population)
            new_chromosome = crossover(cities, population[parent1], population[parent2], config)
            # print(population[0].cost)
            #
            # print("New chromosome cost = {}".format(calc_fitness(cities, new_cromosome)))
            # fitness_offspring = calc_fitness(cities, new_cromosome)

            #     print(min_cost)
            # print(new_population)
            #
            # print(new_population)
            new_population.append(new_chromosome)
            print_way(cities, new_chromosome.chromosome)
        population = cut_population(population + new_population, config)
    print_way(cities, min_cost.chromosome)
    print("Custo minimo = {}".format(min_cost))
    print("Custo minimo valor = {}".format(calc_fitness(cities, min_cost.chromosome)))

    print("------------------------Firts population-------------------------")
    for x in population:
        print(x.chromosome)