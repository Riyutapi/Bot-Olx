# Bot OLX Monitor

Bot em **Python** que monitora novos anúncios na OLX com base em uma palavra-chave e envia notificações para um chat do **Telegram**.

---

# 1. Requisitos

* Python **3.10 ou superior**
* Conta no **Telegram**

---

# 2. Instalando o Python

1. Baixe o Python no site oficial:
   https://www.python.org/downloads/

2. Execute o instalador.

3. **IMPORTANTE:** marque a opção:

```
Add Python to PATH
```

4. Clique em **Install Now**.

---

# 3. Baixar o projeto

Baixe o projeto ou clone o repositório:

```
git clone https://github.com/Riyutapi/Bot-Olx.git
```

Ou baixe o ZIP pelo GitHub e extraia.

Depois abra o terminal dentro da pasta do projeto.

---

# 4. Instalar as bibliotecas

Execute:

```
pip install -r requirements.txt
```

---

# 5. Criar um Bot no Telegram

1. Abra o Telegram
2. Pesquise por **BotFather**

Ou acesse:

https://t.me/BotFather

### Criar o bot

Digite:

```
/start
```

Depois:

```
/newbot
```

O BotFather irá pedir:

1️⃣ **Nome do bot**
Exemplo:

```
OLX Monitor Bot
```

2️⃣ **Username do bot** (deve terminar com `bot`)
Exemplo:

```
olx_monitor_bot
```

Depois disso o BotFather irá enviar algo assim:

```
Use this token to access the HTTP API:
123456789:AAxxxxxxxxxxxxxxxxxxxxxxxx
```

⚠️ **Guarde esse TOKEN**, ele será usado no código.

---

# 6. Descobrir o CHAT ID

Agora você precisa descobrir o ID do chat onde o bot irá enviar as mensagens.

### Método simples

1️⃣ Pesquise seu bot no Telegram
2️⃣ Envie uma mensagem para ele

ou

Adicione o bot em um grupo e envie uma mensagem.

Depois descubra o chat ID, ele fica na url do telegram depois do #.

Se for **grupo**, normalmente começa com:

```
-
```

Exemplo:

```
-1234567890
```

---

# 7. Inserir as configurações no código

Abra o arquivo:

```
monitor.py
```

Localize estas linhas:

```python
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
CHAT_ID = os.getenv("CHAT_ID", "")
KEYWORD = os.getenv("KEYWORD", "")
```

Preencha com seus dados:

```python
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "TOKEN_DO_SEU_BOT")
CHAT_ID = os.getenv("CHAT_ID", "SEU_CHAT_ID")
KEYWORD = os.getenv("KEYWORD", "produto que deseja monitorar")
```

Exemplo:

```python
TOKEN_DO_SEU_BOT = "123456789:AAxxxxxxxxxxxxxxxx"
SEU_CHAT_ID = "-1234567890"
produto que deseja monitorar = "ps5"
```

---

# 8. Rodar o bot

Salve as alterações, no terminal dentro da pasta do projeto:

```
python monitor.py
```

Se tudo estiver correto o bot começará a monitorar anúncios e enviar notificações no Telegram.

---

# 9. Rodar o bot 24h (GitHub)

Você pode rodar o bot usando **GitHub Actions**, mesmo com o computador desligado.

### 1️⃣ Criar um repositório no GitHub

Acesse:

https://github.com

Clique em:

```
New Repository
```

Envie os arquivos do projeto.

---

### 2️⃣ Pasta de workflow

O projeto usa GitHub Actions.

A pasta precisa estar exatamente assim:

```
.github/workflows/run_bot.yml
```

Se você recebeu a pasta sem o ponto:

```
github/workflows
```

basta renomear para:

```
.github
```

Assim o GitHub reconhecerá automaticamente os **workflows**.

---

### 3️⃣ Adicionar Secrets

No repositório vá em:

```
Settings
Secrets and variables
Actions
New repository secret
```

Crie estes secrets:

```
TELEGRAM_TOKEN
CHAT_ID
KEYWORD
```

Exemplo:

```
TELEGRAM_TOKEN = token do bot
CHAT_ID = id do chat
KEYWORD = palavra chave
```

---

### 4️⃣ Iniciar o bot

Depois vá em:

```
Actions
```

Clique no workflow e selecione:

```
Run workflow
```

O GitHub irá iniciar o processo.

⏱️ **A primeira execução manual acontecerá logo em seguida as automáticas pode demorar cerca de 40 minutos para enviar atualizações.**

Depois disso o bot continuará rodando automaticamente.

---

# Aviso

Este projeto é apenas para fins educacionais.
Use com responsabilidade e respeite os termos de uso da OLX.
Está bem cru estou desenvolvendo privado um que abrangerá outros marktplaces e com filtro melhor
