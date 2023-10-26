import pygame
import sys
import random
import pygame.font

# Configuração inicial
pygame.init()

# Configuração de janela do jogo
largura = 1266
altura = 568
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo de Combinação de Navios e Portos")

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)

#fonte da contagem regressiva
tempo_inicial = 8000  # Tempo inicial em segundos
tempo_corrente = tempo_inicial
fonte_contagem = pygame.font.Font(None, 36)

# Variáveis globais
pontos = 0
tempo_espera_navio = 100  # Tempo de espera entre a criação de novos navios (em frames)
tempo_descarga = 200  # Tempo de descarga em frames

# Tipos de navios com diferentes tempos de descarregamento
tipos_de_navios = [
    {"imagem": pygame.image.load("navio1.png"), "tempo_descarga": 3},
    {"imagem": pygame.image.load("navio2.png"), "tempo_descarga": 5},
    {"imagem": pygame.image.load("navio3.png"), "tempo_descarga": 2},
]

# Eficácia dos berços (tempo multiplicador)
eficacia_bercos = {
    "Berço A": 0.75,
    "Berço B": 0.85,
    "Berço C": 1.2,
}

# Classe Navio, isso diz o que ele faz, as caracteristicas e o que é o objeto:
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

# Classe PortoA
class PortoA(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.image.load("porto1.png")  # Imagem específica para Berço A
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = altura - 70  # Mantenha os portos na parte inferior da tela
        self.nome = "Berço A"

# Classe PortoB
class PortoB(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.image.load("porto2.png")  # Imagem específica para Berço B
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = altura - 70  # Mantenha os portos na parte inferior da tela
        self.nome = "Berço B"

# Classe PortoC
class PortoC(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.image.load("porto3.png")  # Imagem específica para Berço C
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = altura - 70  # Mantenha os portos na parte inferior da tela
        self.nome = "Berço C"

# Inicializar os grupos de sprites
navios_esperando = pygame.sprite.Group()
navios_em_porto = pygame.sprite.Group()
portos = pygame.sprite.Group()

# Função para criar portos
def criar_portos():
    nomes_portos = ["Berço A", "Berço B", "Berço C"]
    espaco_entre_portos = largura // (len(nomes_portos) + 1)
    for i, nome in enumerate(nomes_portos):
        x_porto = (i + 1) * espaco_entre_portos - 25  # Ajuste a posição do porto para o centro
        if nome == "Berço A":
            porto = PortoA(x_porto)
        elif nome == "Berço B":
            porto = PortoB(x_porto)
        elif nome == "Berço C":
            porto = PortoC(x_porto)
        portos.add(porto)

# Função para criar um novo navio na fila
def criar_navio():
    x_navio = random.randint(50, largura - 50)
    y_navio = 50  # Mantenha os navios na parte superior da tela
    novo_navio = Navio(x_navio, y_navio)
    navios_esperando.add(novo_navio)

# Loop Principal do Jogo
tempo_navio = 0
tempo_espera_porto = 0
tempo_validade_carga = 1000  # Tempo para validade da carga em frames

# Iniciar o jogo
criar_portos()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # Verificar clique do botão esquerdo do mouse
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
                                # Verificar se o navio foi solto sobre um porto válido
                                pontos += 1
                                navio.rect.x = porto.rect.x + 10  # Ajuste a posição para o centro do berço
                                navio.rect.y = porto.rect.y - 20
                                navio.descarregado = False  # Defina o status do navio como não descarregado
                                navios_em_porto.add(navio)
                                navios_esperando.remove(navio)
    #contagem regressiva
    tempo_corrente -= 1
    if not navios_esperando:
        # Se não houver navios esperando, crie um novo navio
        tempo_navio += 1
        if tempo_navio >= tempo_espera_navio:
            criar_navio()  # Crie um novo navio
            tempo_navio = 0

    # Lógica do jogo
    tempo_espera_porto += 1
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

    

    # Renderizar---------------------------------------------------------
    janela.fill(preto)
    navios_esperando.draw(janela)
    navios_em_porto.draw(janela)
    portos.draw(janela)
   
    # Contador de tempo de carga:
    tempo_restante = tempo_validade_carga - tempo_espera_porto
    fonte = pygame.font.Font(None, 36)
    texto_tempo = fonte.render(f"Tempo Restante: {tempo_restante}", True, vermelho)
    janela.blit(texto_tempo, (10, 50))  # Posição onde o texto será exibido
    
    # Renderize a contagem regressiva na parte superior direita da tela:
    texto_contagem = fonte_contagem.render(f"Tempo: {tempo_corrente/1000}s", True, branco)
    janela.blit(texto_contagem, (largura - 200, 10))

    # Exibir pontos na tela
    fonte = pygame.font.Font(None, 36)
    texto_pontos = fonte.render(f"Pontos: {pontos}", True, branco)
    janela.blit(texto_pontos, (10, 10))

    pygame.display.flip()
