# Grupo-6---Av2---Prog-2

Tema: Forest Fire
# Fire Simulator (Forest Fire)
> É uma simples adaptação baseada do [Modelo Forest Fire](https://github.com/projectmesa/mesa-examples/tree/main/examples/forest_fire).
>O [Modelo Forest Fire](https://github.com/projectmesa/mesa-examples/tree/main/examples/forest_fire) é uma simples simulação de autômato celular de um fogo se espalhando por uma floresta. A floresta é um quadriculado de células, que podem estar vazias ou conter uma árvore. As árvores podem estar intactas, em chamas ou queimadas. O fogo se espalha de cada árvore em chamas para árvores intactas vizinhas; a árvore em chamas então se torna queimada. Isso continua até o fogo se acabar.
## ⚙️ Configuração e Execução do Fire Simulator
### 📦 Pré-requisitos
Antes de começar, certifique-se de que:
- Você tem o [git](https://git-scm.com) instalado em sua máquina.
- Você tem o [Python](https://www.python.org/downloads) instalado em sua máquina.
### 🏗️ Instalando a aplicação
Para instalar a aplicação usando o git, siga estas etapas:
1. Clone o projeto para o diretório de sua escolha (SSH):
    ```bash
    git clone https://github.com/Igor-Roberto-Alves/Grupo-6---Av2---Prog-2
    ```
    ou (SSH)
     ```bash
    git clone git@github.com:Igor-Roberto-Alves/Grupo-6---Av2---Prog-2.git
    ```
2. Após clonar o projeto, navegue até ele:
    ```bash
    cd Grupo-6---Av2---Prog-2
    ```
3. Crie um ambiente virtual `.venv` no Python:
    ```bash
    python -m venv .venv
    ```
4. Acesse seu ambiente virtual no Python:
    ```bash
    source .venv/bin/activate
    ```
5. Em seguida, instale as dependências em seu novo ambiente virtual no Python:
    ```bash
    pip install -r requirements.txt
    ```
### 🚀 Executando a aplicação
1. Execute-a usando o Python:
    ```bash
    python mymesa.py
    ```
## 🎉 Fazendo alterações no projeto
Após ter instalado a aplicação em sua máquina, certifique-se de que você está no diretório da aplicação ("Grupo-6---Av2---Prog-2").
### 🔖 Fazendo novas atualizações
1. Após ter escolhido sua tarefa, crie uma "branch" com o nome "feat-[nome da feat]" (ex: "feat-chuva"), onde o "nome da feat" pode ser obitdo no ClickUp:
    ```bash
    git checkout -b feat-[codigo]
    ```
2. Após ter feito suas alterações, adicione-as:
    ```bash
    git add [arquivo]
    ```
    ou adicione todos arquivos
     ```bash
    git add .
    ```
3. Faça seu commit com uma BREVE descrição das alterações feitas:
    ```bash
    git commit -m "[emoji] tipo(diretório): [breve descrição]"
    ```
    exemplo:
     ```bash
    git commit -m "✨ feat(mymesa.py): add button
    ```
    Obs: emoji pode ser obtido de [Gitmoji](https://gitmoji.dev/)
4. Faça o push (envio das alterações locais para o github):
    ```bash
    git push -u origin [nomeDaBranch]
    ```
    Obs: "nomeDaBranch" geralmente é "feat-[codigo]"
    
5. (Após ter feito todas alterações nessa branch, i.e., finalizou a feature),
   faça seu Pull Request (PR) [aqui](https://github.com/Igor-Roberto-Alves/Grupo-6---Av2---Prog-2/compare).
   Descreva suas alterações (anexe capturas de tela se necessário), e solicite o merge.
   Pronto! basta aguardar que alguém revise seu código e faça o merge para a main.
Participantes:
- IGOR ROBERTO ALVES
- GABRIEL DA SILVA OLIVEIRA
- GABRIEL DE SOUZA VIEIRA
- GIOVANI FIRMINO MOTA
- GUILHERME MASSAHIRO TAKEMORI
- JADER REZENDE MOHR APOLLO DUARTE
- JOÊNIO JOSÉ MILAGRE MARTINS
- LEONARDO GIBOSKI SEGHETO
- PABLO SANTOS CERQUEIRA
- PEDRO HENRIQUE BARBOSA DA SILVA
- PEDRO HENRIQUE DOS REIS PORTO
