import graph as g # grafo e funcoes
import time
import statistics as st


vertices, arcos = g.preenche_listas()

grafo = g.gera_grafo(vertices, arcos);

nos_explorados = []
tempo_total = []

initial_Node = "Loja-SUPREMA"

with open('./files/permutacoes.txt', 'r') as f:
    
    for linha in f:
        destinos = linha.strip().split(',')

        tic = time.time()
        resultados = g.resultados_DFS(start=initial_Node, destinos=destinos, grafo=grafo)
        tac = time.time()

        nos_explorados.append(resultados['explored'])
        tempo_total.append(tac - tic)

print("\n\nDFS")
print(f"Media de nós explorados: {round(st.mean(nos_explorados), 3)}")
print(f"Desvio padrao da qtd de nós explorados: {round(st.stdev(nos_explorados), 3)}")
print(f"Media de tempo: {st.mean(tempo_total):.8f}")
print(f"Desvio padrao de tempo: {st.stdev(tempo_total):.8f}\n\n")

        