import env
import Q_learning
import time

env_maze = env.Maze()

def exec_episode(Q, episodio, show_step, learn, step_time=0.5):
    '''
        Executa um episódio completo realizando o aprendizado
    '''

    done = False
    G, reward = 0, 0

    state, constraints = env_maze.reset()

    step_count = 1
    while not done:
        # Decide qual ação tomar
        action = Q.choose_action(state, constraints)

        # Executa a ação
        state2, constraints, reward, done = env_maze.step(action, step_count, show_step)
        
        if learn:
            # Atualiza a tabela q (Aqui está o aprendizado)
            Q.aprendizado(state, action, reward, state2, constraints)

        if show_step:
            time.sleep(step_time)

        # Atualiza a recompença total
        G += reward

        # Atulaiza o estado atual
        state = state2
        
        # Atualiza o número de passos feitos
        step_count += 1

    print(f"{episodio}: recompença:{round(reward, 2)}| step_count: {step_count}")


actions = list(range(4))
epsilon = 0.3
alpha = 0.618
gamma = 0.9

Q = Q_learning.QLearn(actions, epsilon, alpha, gamma)

# Processo de aprendizado. Treina o agente em 1000 episódios
for episodio in range(1, 1001):
    exec_episode(Q, episodio, show_step=False, learn=True)

for a in Q.actions:
    if (222, a) in Q.q:
        print((222, a), Q.q[(222, a)])

    if(195, a) in Q.q:
        print((195, a), Q.q[(195, a)])
        

input("Press Enter...")
# Ver o agente em ação, após seu treinamento
for episodio in range(1, 11):
    exec_episode(Q, episodio, show_step=True, learn=False, step_time=0.1)
    time.sleep(4)
