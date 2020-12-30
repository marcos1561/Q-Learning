import random

class QLearn(object):
    def __init__(self, actions, epsilon, alpha, gamma):
        # Dicionário para receber os valores de q
        self.q = {}
        
        # Constante de Exploração
        self.epsilon = epsilon  
        
        # Constante de aprendizado
        self.alpha = alpha  
        
        # Fator de Desconto
        self.gamma = gamma  
        
        # Ações
        self.actions = actions


    def getQ(self, state, action):
        '''
            Retorna o valor q para o determinado stado-ação. Caso essa par não exista, retorna 0.0
        '''
        return self.q.get((state, action), 0.0)


    def choose_action(self, state, constraints):
        '''
            Escolhe qual ação deve ser tomada no estado atual
        '''

        # Ações possíveis de serem executadas
        possible_actions = [a for a in self.actions if a not in constraints] 
        
        # Lista com oos valore que para cada ação possícel nesse estado
        q = [self.getQ(state, a) for a in possible_actions]

        max_q = max(q)

        # Randomiza os valore q. Essa parte é reponsável pela exploração
        if random.random() < self.epsilon:
            min_q = min(q)
            mag = max(abs(min_q), abs(max_q))

            q = [q_value + random.random() * mag - 0.5 * mag for q_value in q]
            max_q = max(q)

        # Caso tenha mais que um valor q máximo, escolhe algum de forma aleatória
        if q.count(max_q) > 1:
            bests = [i for i in range(len(q)) if q[i] == max_q]
            i = random.choice(bests)
        else:
            i = q.index(max_q)

        action = possible_actions[i]
        return action

    def learnQ(self, state, action, reward, max_q_new):
        '''
            Atualiza o valor q para ação que foi tomada
        '''
        q_update = self.q.get((state, action), None)

        if q_update is None:
            self.q[(state, action)] = reward
        else:
            self.q[(state, action)] = (1-self.alpha)*q_update + self.alpha * reward + self.alpha*self.gamma*max_q_new


    def aprendizado(self, state1, action1, reward, state2, constraints):
        # Máximo valor q para o próximo estado
        max_q_new = max([self.getQ(state2, a) for a in self.actions if a not in constraints])
        
        self.learnQ(state1, action1, reward, max_q_new)