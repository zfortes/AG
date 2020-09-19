from ga import run
from ypstruct import structure


# Cria uma estrutura com o nome de todas as cidades e suas respectivas distancias armazenada em uma matriz
def initialize():
    cities = structure()
    cities.name = ["SP", "BA", "RJ", "Lima", "Bog.", "Sant.", "Carac.", "BH", "PoA", "BsB"]
    cities.distances = [[0, 17, 3, 35, 43, 26, 44, 5, 8, 9],
                        [17, 0, 20, 31, 47, 11, 51, 22, 8, 23],
                        [3, 20, 0, 38, 45, 29, 45, 3, 11, 9],
                        [35, 31, 38, 0, 19, 25, 27, 36, 33, 32],
                        [43, 47, 45, 19, 0, 43, 10, 43, 46, 37],
                        [26, 11, 29, 25, 43, 0, 49, 30, 19, 30],
                        [44, 51, 45, 27, 10, 49, 0, 42, 48, 35],
                        [5, 22, 3, 36, 43, 30, 42, 0, 13, 6],
                        [8, 8, 11, 33, 46, 19, 48, 13, 0, 16],
                        [9, 23, 9, 32, 37, 30, 35, 6, 16, 0]]
    return cities


# Iniicializa a estrutura das cidades
cities = initialize()

# Parametros do algoritmo
config = structure()
#Tamanho da populacao
config.population_size = 20
# Numero de iteracoes que iram ser repetidas
config.number_iterations = 500
# Probabilidade de ocorrer uma mutacao em um dado gene dos cromossomos filhos
# (0 a 100)
config.mutation_probability = 5
# Numero que representa o total de ocorrencias aleatorios que ocorreram durante
# a selecao de quem ira ou nao continuar na populacao
# Quanto maior for o valor, mais eventos aleatorios aconteceram e em decorrencia
# disso mais aleatorio sera o resultado
# Quanto menor ele for definido maior sera as chances das novas populacoes serem
# escolhidas na selecao dos mais fortes e propensos a continuar a reproducao
config.cut_randomness = 30

#Inicia o GA
run(cities, config)
