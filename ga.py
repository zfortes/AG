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

    for i in range(len(x.chromosome)):
        prob = np.random.randint(1, 100)
        if prob <= mutation_probability and i != 0 and i != 10:
            index = np.random.randint(0, 8)
            for i in range

            aux = x.chromosome[index]
            x.chromosome[index] = x.chromosome[i]
            x.chromosome[i] = aux
    print("Mutation of {} in {}".format(offspring.chromosome, x.chromosome))
    return x


def crossover_two_cut(parent1, parent2):
    print("two pontin")


def crossover_one_cut(parent1, parent2):
    cut_index = np.random.randint(2, 8)
    # print("Cut index = {}".format(cut_index))
    # print("parent1 = {}  parente2 = {}".format(parent1.chromosome, parent2.chromosome))
    # print("childrem = {}".format(parent1.chromosome[0:cut_index] + parent2.chromosome[cut_index:11]))
    return parent1.chromosome[0:cut_index] + parent2.chromosome[cut_index:11]


def crossover(cities, parent1, parent2):
    probability = np.random.randint(0, 10)
    offspring = structure()

    if probability < 11:
        chromosome = crossover_one_cut(parent1, parent2)
    else:
        chromosome = crossover_two_cut(parent1, parent2)

    offspring.cost = calc_fitness(cities, chromosome)
    offspring.chromosome = chromosome
    return offspring

def selection(p):
    c = np.cumsum(p)
    r = sum(p) * np.random.rand()
    ind = np.argwhere(r <= c)
    return ind[0][0]


def verify_chromosome(chromosome):
    find = [11]
    print("Chromosome = {}".format(chromosome[0]))
    for i in range(len(chromosome)):
        if find[i] != True:
            print("Chromosome = {}".format(chromosome[i]))
            find.insert(chromosome[i], True)
        else:
            return False
    return True


def run(cities, config):
    population, min_cost = create_initial_population(cities, config)
    costs = np.array([x.cost for x in population])

    print(population)

    for i in range(config.number_iterations):
        avg_cost = np.mean(costs)
        if avg_cost != 0:
            costs = costs / avg_cost
        probs = np.exp(-1 * costs)

        new_population = []
        for i in range(config.population_size):
            parent1 = selection(probs)
            parent2 = selection(probs)
            new_cromosome = crossover(cities, population[parent1], population[parent2])
            # print(population[0].cost)
            #
            # print("New chromosome cost = {}".format(calc_fitness(cities, new_cromosome)))
            # fitness_offspring = calc_fitness(cities, new_cromosome)
            if min_cost.cost > new_cromosome.cost and verify_chromosome(new_cromosome.chromosome):
                min_cost.cost = new_cromosome.cost
                min_cost.chromosome = new_cromosome.chromosome
                print(min_cost)
            new_population.append(mutation(new_cromosome))
        population = new_population
        # mutation()
    print("Custo minimo = {}".format(min_cost))
    print("Custo minimo valor = {}".format(calc_fitness(cities, min_cost.chromosome)))
