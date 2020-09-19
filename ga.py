from ypstruct import structure
import random
import numpy as np
import operator


# Função que calcula o fitness de um cromossomo
def calc_fitness(cities, chromosome):
    res = 0
    for i in range(len(chromosome) - 1):
        res += cities.distances[chromosome[i]][chromosome[i + 1]]
    return res


# Cria a polupação inicial e ja insere os genes de BsB no inicio e fim do cromossomo
def create_initial_population(cities, config):
    initial_population = structure()
    initial_population.cost = 0
    initial_population.chromosome = list(range(0, 9))
    initial_population = initial_population.repeat(config.population_size)
    min_cost = structure()
    min_cost.cost = 999999999
    # print("Initial population")
    total = 0
    for i in range(config.population_size):
        random.shuffle(initial_population[i].chromosome)
        initial_population[i].chromosome.insert(0, 9)
        initial_population[i].chromosome.insert(10, 9)
        initial_population[i].cost = calc_fitness(cities, initial_population[i].chromosome)
        if initial_population[i].cost < min_cost.cost:
            min_cost = initial_population[i]

    #     print("Gene = {}".format(initial_population[i].chromossome))
    #     print(initial_population[i].cost)
    #     total += initial_population[i].cost
    # print("Total = {}".format(total))
    # print(min_cost)
    return initial_population, min_cost


def mutation(offspring, mutation_probability=3):
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
    print("two pontin")


def get_index_gene(chromosome, x):
    for i in range(len(chromosome)):
        if chromosome[i] == x:
            return i
    return -1



def crossover_one_cut(parent1, parent2):
    cut_index = np.random.randint(2, 8)
    # print("MParent 1 e 2 {} in {}".format(parent1, parent2))
    # child = parent1.chromosome[0:cut_index]
    first = parent1.chromosome[0:cut_index]
    first2 = parent2.chromosome.copy()
    # print("Cut = {}".format(cut_index))
    for i in range(1, cut_index):
        index = get_index_gene(first2, first[i])
        aux = first2[i]
        first2[i] = first[i]
        first2[index] = aux
    # print("MParent 1 {}".format(parent1.chromosome))
    # print("MParent 2 {}".format(parent2.chromosome))
    # print("Mchild    {}".format(first2))

    return first2

def crossover(cities, parent1, parent2):
    probability = np.random.randint(0, 9)
    offspring = structure()

    if probability < 11:
        chromosome = crossover_one_cut(parent1, parent2)
    else:
        chromosome = crossover_two_cut(parent1, parent2)

    chromosome = mutation(chromosome)
    offspring.cost = calc_fitness(cities, chromosome)
    offspring.chromosome = chromosome
    return offspring

def selection(p):
    a = np.random.randint(0, len(p))
    b = np.random.randint(0, len(p))
    return a, b

def cut_population(population, config):
    min = float('-inf')
    index = 0
    # for i in range(len(population)):
    #     print("{} - {}".format(i, population[i].cost))
    population = sorted(population, key=operator.attrgetter('cost'))
    population = population[0:config.population_size]

    # print("outra ==============")
    # for i in range(len(population)):
    #     print("{} - {}".format(i, population[i].cost))

    # for i in range(len(population)):
    #     if population[i].cost < min:
    #         min = population[i].cost
    #         index = i
    # population.pop(index)
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

    print(population)

    for i in range(config.number_iterations):
        costs = np.array([x.cost for x in population])
        avg_cost = np.mean(costs)
        if avg_cost != 0:
            costs = costs / avg_cost
        probs = np.exp(-1 * costs)
        print("Interation number = {}".format(i))
        print("Min value = {}".format(min_cost))
        new_population = []
        # for i in range(config.population_size):
        for i in range(20):
            parent1, parent2 = selection(population)
            # = selection(population)
            new_cromosome = crossover(cities, population[parent1], population[parent2])
            # print(population[0].cost)
            #
            # print("New chromosome cost = {}".format(calc_fitness(cities, new_cromosome)))
            # fitness_offspring = calc_fitness(cities, new_cromosome)
            if min_cost.cost > new_cromosome.cost:
                min_cost.cost = new_cromosome.cost
                min_cost.chromosome = new_cromosome.chromosome
            #     print(min_cost)
            # print(new_population)
            #
            # print(new_population)
            new_population.append(new_cromosome)
        population = cut_population(population + new_population, config)
    print_way(cities, min_cost.chromosome)
    print("Custo minimo = {}".format(min_cost))
    print("Custo minimo valor = {}".format(calc_fitness(cities, min_cost.chromosome)))
