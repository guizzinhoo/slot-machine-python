import random

MAX_LINES = 3
MAX_BETS = 100
MIN_BETS = 1

ROWS = 3  # define a quantidade de linhas horizontais
COLS = 3  # define a quantidade de colunas verticais

contagem_simbolos = {  # dicionário que define os símbolos do jogo e sua frequência no sorteio
    "♞": 2,  #  aparece 2 vezes (mais raro)
    "♬": 4,
    "✈": 6,
    "☘": 8,  #  aparece 8 vezes (mais comum)
}

valor_simbolos = {  # dicionário que define os valores dos símbolos
    "♞": 5,
    "♬": 4,
    "✈": 3,
    "☘︎": 2,
}


def check_winning(colunas, lines, bets, valores): # verifica ganhos com base nas linhas apostadas
    winnings = 0
    winning_lines = []

    for line in range(lines): # percorrerá as linhas
        symbol = colunas[0][line] # confere o simbolo da primeira coluna

        for coluna in colunas: # percorre todas as colunas
            symbol_to_check = coluna[line] #pega o simbolo da coluna atual na mesma linha
            if symbol != symbol_to_check: # verifica se são diferentes, se for, quebra (a linha não é vencedora)
                break
        else:
            winnings += valores[symbol] * bets # se não houve quebra, soma o prêmio da linha (valor do símbolo * aposta)
            winning_lines.append(line + 1) # + 1 para aparecer o número correto da linhas

    return winnings, winning_lines


def spinMachine(rows, cols, simbolos):  # simula o giro do caça-níquel
    lista_simbolos = []  # reservatório de símbolos para o sorteio

    for symbol, contagem_simbolos in simbolos.items():  # percorre cada símbolo e sua quantidade no dicionário
        for _ in range(contagem_simbolos):  # repete de acordo com a quantidade definida para cada símbolo
            lista_simbolos.append(symbol)  # adiciona o símbolo à lista de sorteio

    colunas = []  # armazena as colunas da máquina

    for _ in range(cols):  # repete o processo para cada coluna
        coluna = []
        simbolosUsados = lista_simbolos[:]  # [:] cria uma cópia da lista

        for _ in range(rows):  # repete para preencher cada linha da coluna
            valor = random.choice(simbolosUsados)  # escolhe aleatoriamente um símbolo
            simbolosUsados.remove(valor)  # remove o símbolo escolhido da cópia para evitar repetição
            coluna.append(valor)  # adiciona o símbolo sorteado à coluna

        colunas.append(coluna)

    return colunas


def printar_spinMachine(colunas): #vai organizar a saída
    for row in range(len(colunas[0])):
        for i, coluna in enumerate(colunas):
            if i != len(colunas) - 1: #verifica se é a ultima coluna, colocando um separador ou apenas o simbolo
                print(coluna[row], end=" | ") #sem o end com o separador usado ( | ), o console quebraria linha
            else:
                print(coluna[row], end="")

        print() #uma forma manual de fazer o console quebrar linha


# verificando quantia de deposito e garantindo que será um número inteiro e posito
def deposito():
    while True:
        quantia = input("Qual quantia será depositada? Aposta máxima de 100, mínima de 1. R$")

        if not quantia.isdigit():
            print("Por favor, digite um número.")
            continue

        quantia = int(quantia)

        if quantia > MAX_BETS:
            print("O valor máximo de depósito é de R$100.")
        elif quantia <= MIN_BETS:
            print("Seu depósito deve ser maior que 0.")
        else:

            return quantia


# quantas vezes o valor depositado será apostado na mesma rodada
def numero_linhas(quantia):
    while True:
        lines = input("Número de linhas à serem apostadas (1-"+ str(MAX_LINES) + "): ")

        if not lines.isdigit():
            print("Por favor, digite um numero.")
            continue

        lines = int(lines)

        if not (1 <= lines <= MAX_LINES): # verificar se o valor está entre minimo e maximo
            print("Entre com um valor válido de linhas.")
            continue

        if lines * MIN_BETS > quantia:
            print("Com esse saldo, não é possível apostar nessa quantidade de linhas.") # pois o número de linhas não pode ser maior que o valor depositado
            continue

        return lines


# valor a ser apostado
def qtd_bets():
    while True:
        quantia = input("Quanto deseja apostar em cada linha? R$")

        if quantia.isdigit():
            quantia = int(quantia)
            if MIN_BETS <= quantia <= MAX_BETS: # verificar se o valor está entre minimo e maximo
                break
            else:
                print(f"Seu deposito deve ser entre R${MIN_BETS} - R${MAX_BETS}.") # informa ao usuário o valor mínimo e máximo permitido, ja automaticamente convertudo para str
        else:
            print("Por favor, digite um numero.")

    return quantia


def giro(saldo):
    lines = numero_linhas(saldo)
    while True:
        bet = qtd_bets()
        total_bet = bet * lines  # calcula quanto foi apostado

        if total_bet > saldo:  # verifica se a aposta condiz com o saldo
            print(f"Você não possui saldo para esta quantia, seu saldo atual é de R${saldo}")
        else:
            break

    print()
    print(f"Você está apostando ${bet} em {lines} linhas. Aposta total será de R${total_bet}")
    print()

    slots = spinMachine(ROWS, COLS, contagem_simbolos)
    printar_spinMachine(slots)
    winnings, winning_lines = check_winning(slots, lines, bet, valor_simbolos)

    print()
    print(f"Você ganhou R${winnings}.")

    if winning_lines:
        print(f"Você ganhou em linha:", *winning_lines)
    else:
        print("Nenhuma linha vencedora.")

    return winnings - total_bet


def main(): # função principal que roda o código
    print("Seja muito bem vindo!")
    saldo = deposito()
    while True:
        print(f"Saldo atual é de R${saldo}")
        resposta = input("Pressione enter para jogar (tecle 'q' para sair). ").strip().lower()

        if resposta == "q":
            break
        saldo += giro(saldo) # modifica o saldo por rodada

    print()
    print(f"Lhe sobraram R${saldo}")
    print("Obrigado por jogar!")

main()

