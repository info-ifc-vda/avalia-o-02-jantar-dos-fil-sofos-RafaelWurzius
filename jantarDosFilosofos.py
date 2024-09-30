import tkinter as tk
import math
import threading
import time
import random

# Função para alternar a cor do círculo entre vermelho e verde
def alternar_cor(index):
    cor_atual = canvas.itemcget(circulos[index], 'fill')
    if cor_atual == 'red' or cor_atual == 'orange':
        nova_cor = 'green'
    elif cor_atual == 'green' or cor_atual == 'yellow':
        nova_cor = 'red'
    canvas.itemconfig(circulos[index], fill=nova_cor)

# Criação da janela principal
janela = tk.Tk()
janela.title("Jantar dos Filósofos")

# Criação do canvas onde os círculos serão desenhados
canvas = tk.Canvas(janela, width=400, height=400)
canvas.pack()

# Lista para armazenar as referências dos círculos
circulos = []

# Definindo o centro e o raio para desenhar os círculos em formato circular
centro_x, centro_y = 200, 200
raio = 100
numero_circulos = 5

# Desenhando 5 círculos em disposição circular
for i in range(numero_circulos):
    # Calcula o ângulo de cada círculo em uma disposição circular
    angulo = 2 * math.pi * i / numero_circulos
    x = centro_x + raio * math.cos(angulo) - 25  # Ajusta a posição X
    y = centro_y + raio * math.sin(angulo) - 25  # Ajusta a posição Y
    circulo = canvas.create_oval(x, y, x + 50, y + 50, fill='red')
    circulos.append(circulo)

# Resolução do problema ----------------------------------------------------------------------------------------------------------------------

class Philosopher(threading.Thread):
    def __init__(self, index, left_fork, right_fork, eat_time, death_time):
        threading.Thread.__init__(self)
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.eat_time = eat_time
        self.death_time = death_time  # Tempo até o filósofo morrer de fome
        self.last_meal_time = time.time() * 1000  # Última vez que o filósofo comeu
        self.alive = True
        self.lock = threading.Lock()  # Lock para proteger o acesso ao tempo de morte

    def run(self):
        while self.alive:
            self.think()
            self.try_to_eat()

    def think(self):
        print(f"Filósofo {self.index} está pensando.")
        alternar_cor(self.index)
        time.sleep(random.uniform(5, 10))  # Pensando por um tempo aleatório

    def time_until_death(self):
        # Retorna o tempo restante até o filósofo morrer de fome
        with self.lock:
            return self.death_time - (time.time() - self.last_meal_time)

    def try_to_eat(self):
        with self.lock:
            self.last_meal_time = time.time()  # Resetar o tempo de fome

        while True:
            time_remaining = self.time_until_death()

            if time_remaining <= 0:
                self.alive = False
                print(f"Filósofo {self.index} morreu de fome.")
                canvas.itemconfig(circulos[self.index], fill='black')
                return  # Filósofo morreu, sair da função

            canvas.itemconfig(circulos[self.index], fill='yellow')  # Tentando pegar os garfos
            # Tentar pegar os garfos com controle de prioridade
            if self.try_acquire_forks():
                self.eat()
                return  # Filósofo comeu, volta a pensar

    def try_acquire_forks(self):
        left_priority = neighbors[self.index].time_until_death()
        right_priority = neighbors[(self.index + 1) % num_philosophers].time_until_death()

        # Filósofo tem prioridade se o seu tempo restante for menor
        if self.time_until_death() < left_priority:
            left_acquired = self.left_fork.acquire(timeout=self.time_until_death())
        else:
            left_acquired = self.left_fork.acquire(timeout=left_priority)

        if not left_acquired:
            return False  # Não conseguiu o garfo esquerdo

        if self.time_until_death() < right_priority:
            right_acquired = self.right_fork.acquire(timeout=self.time_until_death())
        else:
            right_acquired = self.right_fork.acquire(timeout=right_priority)

        if not right_acquired:
            self.left_fork.release()
            return False  # Não conseguiu o garfo direito

        return True  # Conseguiu ambos os garfos

    def eat(self):
        print(f"Filósofo {self.index} está comendo.")
        alternar_cor(self.index)
        time.sleep(self.eat_time)  # Tempo para comer
        print(f"Filósofo {self.index} terminou de comer.")
        self.left_fork.release()
        self.right_fork.release()


num_philosophers = 5
forks = [threading.Semaphore(1) for _ in range(num_philosophers)]
philosophers = []
neighbors = []  # Lista para armazenar os vizinhos (outros filósofos)

# Criando filósofos com tempos de alimentação variados
for i in range(num_philosophers):
    eat_time = random.uniform(5, 10)  # Cada filósofo leva um tempo aleatório para comer
    death_time = 20  # Cada filósofo morre de fome após esse tempo sem comer
    left_fork = forks[i]
    right_fork = forks[(i + 1) % num_philosophers]  # O garfo à direita é o próximo na lista
    philosopher = Philosopher(i, left_fork, right_fork, eat_time, death_time)
    philosophers.append(philosopher)
    neighbors.append(philosopher)
    philosopher.start()

# Fim da resolução do problema ------------------------------------------------------------------------------------------------------------------

# Executando a janela
janela.mainloop()
