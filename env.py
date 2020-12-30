import numpy as np

class Maze(object):
    '''
        Ambiente no qual o agente será treinado
    '''

    def __init__(self):
        '''
            self.agent_pos: np.Array
                Posição inicial do agente. O primeiro elemento informa a linha e o segundo a coluna do labirinto, em que
                o agente está.
            
            self.actions: Dict
                Dicionário contendo todas as ações possíveis que o agente pode tomar. (Andar para direta, cima, esquerda e baixo)
                Cada ação é representada por um vetor, por exemplo, o vetor = (0, 1) representa ficar na mesma linha e ir para a próxima coluna, o vator = (-1, 0) representa descer uma linha e ficar na mesma coluna, etc.

                Assim a nova posição do agente após realizar uma ação é self.agent_pos + self.action[i]

            self.maze: List 2-D
                Lista contendo o labirinto. O labirinto fica armazenado em um arquvo.txt e cada caractere desse arquivo é um elemento
                dessa lista. É preenchida de tal forma que o canto esquerdo inferior do labirinto possua o índice [0][0].
                O labirinto possui 4 ícones diferentes:
                    "#": Parede
                    "X": Armadilha
                    "O": Chegada
                    "A": Agente
            
            self.width: int
                Largura do labirinto, sem contar as paredes
        '''

        self.agent_pos = np.array([1,1])
        self.actions = {0: np.array((0, 1)), 1: np.array((1, 0)), 2: np.array((0, -1)), 3:np.array((-1, 0))}

        self.maze = []
        with open("maze.txt", "r") as f:
            [self.maze.insert(0, list(line.strip())) for line in f.readlines()]

        self.maze_width = len(self.maze[0]) - 2


    def current_state(self):
        '''
            Retorna o estado atual em que o agente se encontra. O estado do agene é uma função de sua posição ( s = (linha, coluna) ) e a
            largura do labirinto, não contando as paredes (L)
            Estado(s, L) = (s - (1,1)) * (L, 1)
        '''

        return np.dot((self.agent_pos - np.array([1,1])), np.array([self.maze_width, 1])) 
        # return (self.agent_pos[0]-1)*28 + self.agent_pos[1]-1


    def reset(self):
        '''
            Reseta o ambiente.
            Constraints contém uma lista das ações que não possíveis de serem executadas no estado atual
        '''

        self.agent_pos = np.array([1,1])
        constraints = [2, 3]

        self.maze = []
        with open("maze.txt", "r") as f:
            [self.maze.insert(0, list(line.strip())) for line in f.readlines()]

        return self.current_state(), constraints


    def step(self, action, step_count, show_step=False):
        '''
            Executa a ação e retorna o novo estado, constraints e a recompença que essa ação gerou

            * Constraints contém uma lista das ações que não possíveis de serem executadas no novo estado
        '''

        self.maze[self.agent_pos[0]][self.agent_pos[1]] = " "
        
        self.agent_pos += self.actions[action]
        
        local_now = self.maze[self.agent_pos[0]][self.agent_pos[1]]
        self.maze[self.agent_pos[0]][self.agent_pos[1]] =  "A"

        contraints = []
        for action_i in range(4):
            '''
                A seguinte função 

                    f(x) = (cos(x), sen(x))

                Retorna os vetores que representam as ações, a cada pi/2, se começar em x = pi/2
            '''

            angle = np.pi/2 - np.pi/2*action_i

            # Posição após executar a ação i
            line_pos = self.agent_pos[0] + int(np.cos(angle))
            column_pos = self.agent_pos[1] + int(np.sin(angle))

            # Caso essa posição possua uma parede, a ação é inválida
            if self.maze[line_pos][column_pos] == "#":
                contraints.append(action_i)

        '''
            Calcula a recompença da ação:

            Caso a ação proveque o agene de bater: 
                -> em uma armadilha: recompença = -1
                -> No final: recompença = 1
                -> Em local vazio: recompença = 0

            Quando o agente completa o labirinto, um benifício extra é dado na recompença, 
            que aumenta conforme o número de passos necessários diminui.     
        '''
        reward = 0
        done = False
        if local_now == "O":
            reward = 1 + 0.7**(step_count-55)
            # reward = 1
            done = True

            self.agent_pos -= self.actions[action]
            print(self.current_state())
            self.agent_pos += self.actions[action]


        elif local_now == "X":
            reward = -1
            done = True

        if show_step:
            self.print_maze()

        return self.current_state(), contraints, reward, done


    def print_maze(self):
        '''
            Printa o labirinto no console
        '''

        self.maze.reverse()
        for line in self.maze:
            line_str = ""
            for carac in line:
                line_str += carac
            print(line_str)
        self.maze.reverse()
