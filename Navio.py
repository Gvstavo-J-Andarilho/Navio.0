import pygame
import sys
import random

# Configuração inicial
pygame.init()

# Configuração da janela do jogo
largura, altura = 1266, 568
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo de Combinação de Navios e Portos")

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)

# Variáveis de tempo
tempo_inicial = 8000
tempo_corrente = tempo_inicial
tempo_espera_porto = 0
tempo_validade_carga = 8000
decrescente_validade_carga = tempo_validade_carga

# Outras variáveis
pontos = 0

tipos_de_navios = [
    {"imagem": pygame.image.load("C:/Users/Gustavo/PycharmProjects/Navio/JogoNavio/navio1.png"), "tempo_descarga": 1},
    {"imagem": pygame.image.load("C:/Users/Gustavo/PycharmProjects/Navio/JogoNavio/navio2.png"), "tempo_descarga": 2},
    {"imagem": pygame.image.load("C:/Users/Gustavo/PycharmProjects/Navio/JogoNavio/navio3.png"), "tempo_descarga": 3},
    {"imagem": pygame.image.load("C:/Users/Gustavo/PycharmProjects/Navio/JogoNavio/navio4.png"), "tempo_descarga": 4}
]
# Eficácia dos berços
eficacia_bercos = {
    "Berço A": 0.5,
    "Berço B": 0.75,
    "Berço C": 1.2,
    "Berço D": 2
}

# Classe Navio
class Navio(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        tipo_navio = random.choice(tipos_de_navios)
        self.image = tipo_navio["imagem"]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidade = 0
        self.tempo_descarga = tipo_navio["tempo_descarga"]
        self.descarregado = False
        self.arrastando = False
        self.offset_x = 0
        self.offset_y = 0

    def update(self):
        if not self.arrastando:
            self.rect.x += self.velocidade

    def iniciar_arraste(self, pos_mouse):
        if self.rect.collidepoint(pos_mouse):
            self.arrastando = True
            self.offset_x = self.rect.x - pos_mouse[0]
            self.offset_y = self.rect.y - pos_mouse[1]

    def parar_arraste(self):
        self.arrastando = False

# Classes dos Portos
class Porto(pygame.sprite.Sprite):
    def __init__(self, x, nome, imagem):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = altura - 500
        self.nome = nome

# Inicialização dos grupos de sprites
navios_esperando = pygame.sprite.Group()
navios_em_porto = pygame.sprite.Group()
portos = pygame.sprite.Group()

# Função para criar portos
def criar_portos():
    nomes_portos = ["Berço A", "Berço B", "Berço C", "Berço D"]
    espaco_entre_portos = largura // (len(nomes_portos) + 1)
    for i, nome in enumerate(nomes_portos):
        x_porto = (i + 1) * espaco_entre_portos - 25
        imagem_porto = pygame.image.load(f"porto{i + 1}.png")
        porto = Porto(x_porto, nome, imagem_porto)
        portos.add(porto)
def Movimentar_Navios():
    global x_chegada, y_chegada
    for i, navio in enumerate(navios_esperando):
        i = i % len(destino)
        destino_x, destino_y = destino[i]

        atual_x, atual_y = navio.rect.center
        dx = destino_x - atual_x
        dy = destino_y - atual_y
        distancia = ((dx ** 2) + (dy ** 2)) ** 0.5

        if distancia > 0:
            move_x = dx / distancia * navio_velocidade
            move_y = dy / distancia * navio_velocidade

            x_chegada[i] = atual_x + move_x
            y_chegada = atual_y + move_y

            for porto in portos:
                if navio.rect.colliderect(porto.rect):
                    return True
            navio.rect.center = (x_chegada[i], y_chegada)

    return None


#variáveis para criação e movimentação dos navios
destino = [(228, 450), (481, 450), (734, 450), (986, 450)] #coordenadas de x dos portos
x_chegada = [destino_x for destino_x, _ in destino]
origem = [(largura-300, 450), (largura-250, 450), (largura-200, 450), (largura-150, 450)]
navio_velocidade = 2
# Função para repor as posições disponíveis
def repor_posicoes_disponiveis():
    global posicoes_disponiveis
    posicoes_disponiveis = origem.copy()

# Função para criar um novo navio
posicoes_disponiveis = origem.copy()
# Criar portos
criar_portos()
tempo_para_novo_navio = 1  # Ajuste esse valor para controlar a frequência de criação
# Função para criar um novo navio
posicoes_disponiveis = origem.copy()
tempo_para_nova_geracao = 300  # Intervalo de tempo para criar uma nova geração de navios
tempo_para_novo_navio = tempo_para_nova_geracao  # Inicializa o temporizador

# Função para criar um novo navio
# Função para criar um novo navio
def criar_navios():
    global tempo_para_novo_navio

    if tempo_para_novo_navio <= 0:
        if not posicoes_disponiveis:
            repor_posicoes_disponiveis()
        numero_de_navios = random.randint(1, min(4, len(posicoes_disponiveis)))  # Gera entre 1 e 4 navios ou o número de posições disponíveis
        for _ in range(numero_de_navios):
            x, y = random.choice(posicoes_disponiveis)
            cargo = random.choice(tipos_de_navios)
            novo_navio = Navio(x, y)

            # Verifique se o novo navio colide com outros navios
            colide = False
            for navio_existente in navios_esperando:
                if novo_navio.rect.colliderect(navio_existente.rect):
                    colide = True
                    break

            # Se não houver colisão, adicione o novo navio
            if not colide:
                navios_esperando.add(novo_navio)
                if (x, y) in posicoes_disponiveis:
                    posicoes_disponiveis.remove((x, y))

        tempo_para_novo_navio = tempo_para_nova_geracao  # Redefina o temporizador
    tempo_para_novo_navio -= 1

# Loop Principal do Jogo
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                for navio in navios_esperando:
                    if navio.rect.collidepoint(evento.pos):
                        navio.iniciar_arraste(evento.pos)
        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1:
                for navio in navios_esperando:
                    if navio.arrastando:
                        navio.parar_arraste()
                        for porto in portos:
                            if porto.rect.collidepoint(evento.pos):
                                pontos += 1
                                bonificacao = 1000
                                tempo_corrente += bonificacao
                                decrescente_validade_carga += bonificacao
                                navio.rect.x = porto.rect.x + 10
                                navio.rect.y = porto.rect.y - 20
                                navio.descarregado = False
                                navios_em_porto.add(navio)
                                navios_esperando.remove(navio)

    tempo_corrente -= 1
    decrescente_validade_carga -= 1

    # Controle da criação de novos navios
    criar_navios()  # Crie um novo navio

    tempo_corrente -= 1
    Movimentar_Navios()
    decrescente_validade_carga -= 1
    Movimentar_Navios()

    if tempo_corrente <= 0:
        pygame.quit()
        sys.exit()
    tempo_espera_porto += 1
    if tempo_espera_porto >= tempo_validade_carga:
        # A carga expirou
        pygame.quit()
        sys.exit()
    if decrescente_validade_carga <= 0:
        pygame.quit()
        sys.exit()
    if tempo_espera_porto >= tempo_validade_carga:
        # A carga expirou
        pygame.quit()
        sys.exit()

    # Atualizar posição do navio enquanto está sendo arrastado
    for navio in navios_esperando:
        if navio.arrastando:
            pos_mouse = pygame.mouse.get_pos()
            navio.rect.x = pos_mouse[0] + navio.offset_x
            navio.rect.y = pos_mouse[1] + navio.offset_y

    # Atualizar sprites
    navios_esperando.update()
    navios_em_porto.update()

    # Remover navios após descarga
    for navio in navios_em_porto:
        if not navio.arrastando and not navio.descarregado:
            navio.tempo_descarga -= 1
            if navio.tempo_descarga <= 0:
                navios_em_porto.remove(navio)
                # Define o status do navio como descarregado para que ele não seja processado novamente
                navio.descarregado = True
                if navio.descarregado:
                    tempo_espera_porto=0

    # Renderizar
    janela.fill(preto)
    navios_esperando.draw(janela)
    navios_em_porto.draw(janela)
    portos.draw(janela)

    # Renderize a contagem regressiva na parte superior direita da tela:
    contagem = pygame.font.Font(None,36)
    texto_contagem = contagem.render(f"Tempo restante: {tempo_corrente/1000}s", True, branco)
    janela.blit(texto_contagem, (largura - 300, 10))

    # Exibir pontos na tela
    fonte = pygame.font.Font(None, 36)
    texto_pontos = fonte.render(f"Pontos: {pontos}", True, branco)
    janela.blit(texto_pontos, (10, 10))

    # Exibir pontos na tela
    validade = pygame.font.Font(None, 18)
    texto_validade = fonte.render(f"Validade: {decrescente_validade_carga/1000}s", True, vermelho)
    janela.blit(texto_validade, (10, 50))

    pygame.display.flip()

'''destino = aonde o navio vai parar = 
espaco_entre_portos

tela:
	lar=1266 (x)
	altura=568 (y)
destino = [(228, 450), (481, 450), (734, 450), (986, 450)] #coordenadas de x dos portos
origem = [(largura-300, 450), (largura-250, 450), (largura-200, 450), (largura-150, 450)]'''
