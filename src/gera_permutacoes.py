from graph import preenche_listas
import itertools

vertices, arcos = preenche_listas()

vertices.remove('Loja-SUPREMA')

print(vertices)

permutacoes = itertools.permutations(vertices, 3)

with open('./files/permutacoes.txt', 'w') as f:
    for p in permutacoes:
        f.write(','.join(map(str, p)) + '\n') 
