# whatsapp-client

Biblioteca Python para automação de envio de mensagens e arquivos no WhatsApp Web usando Playwright.

## Visão geral

Esta lib expõe a classe `WhatsappClient`, que:

- abre o WhatsApp Web;
- valida login (incluindo fluxo de QR Code);
- busca contato/grupo;
- envia mensagem de texto;
- envia arquivo como documento ou imagem.

A pasta principal do projeto é `client/`, onde ficam:

- `client.py`: implementação da automação (`WhatsappClient`);
- `config.py`: leitura de variáveis de ambiente e timeouts;
- `elements.py`: seletores (XPaths/CSS) usados pela RPA.

---

## Estrutura

```text
whatsapp-client/
├── README.MD
├── client/
│   ├── __init__.py
│   ├── client.py
│   ├── config.py
│   └── elements.py
└── session/
```

---

## Pré-requisitos

- Python 3.10+
- Google Chrome/Chromium instalado
- Conta WhatsApp com acesso ao WhatsApp Web

Dependências Python usadas no código:

- `playwright`
- `python-dotenv`

## Instalação

No diretório do projeto:

```bash
pip install playwright python-dotenv
python -m playwright install chromium
```

---

## Configuração (.env)

Crie um arquivo `.env` na raiz do projeto com as variáveis abaixo:

```env
PATH_USER_DATA=./session/user_data
PATH_DOWNLOADS=./session/downloads
URL_WHATSAPP=https://web.whatsapp.com/
TIMEOUT=120000
```

### Significado das variáveis

- `PATH_USER_DATA`: pasta para sessão persistente do navegador (mantém login);
- `PATH_DOWNLOADS`: pasta de downloads do navegador automatizado;
- `URL_WHATSAPP`: URL do WhatsApp Web;
- `TIMEOUT`: timeout (em ms) para operações de espera.

> Dica: se a pasta não existir, crie antes de rodar para evitar erros de caminho.

---

## Uso rápido

### 1) Enviar mensagem de texto

```python
from client.client import WhatsappClient

with WhatsappClient(headless=False) as bot:
		ok = bot.send_text(contact="Nome do contato", message="Olá! Mensagem automática.")
		print("Enviado?", ok)
```

### 2) Enviar arquivo

```python
from pathlib import Path

from client.client import WhatsappClient

arquivo = Path(r"C:/caminho/arquivo.pdf")

with WhatsappClient(headless=False) as bot:
		ok = bot.send_file(
				file=arquivo,
				contact="Nome do contato",
				caption="Segue o arquivo.",
				mediatype="document",  # "document" | "image"
		)
		print("Arquivo enviado?", ok)
```

### 3) Fluxo de login

- No primeiro uso, o WhatsApp Web pode exibir QR Code;
- após escanear, a sessão fica salva em `PATH_USER_DATA`;
- execuções seguintes tendem a reutilizar a sessão.

---

## API principal

### `WhatsappClient(headless: bool = True)`

Inicializa o cliente de automação.

- `headless=True`: roda sem abrir janela;
- `headless=False`: abre navegador (recomendado para setup/login).

### Métodos

- `start()`
	- inicializa Playwright e contexto persistente.

- `login() -> bool`
	- abre WhatsApp Web e valida se está logado;
	- pode lançar `TimeoutError` caso login não ocorra no tempo esperado.

- `find_contact(contact: str) -> bool`
	- pesquisa e abre a conversa do contato/grupo.

- `send_text(contact: str, message: str) -> bool`
	- envia texto para o contato informado.

- `send_file(file: Path, contact: str, caption: str | None = None, mediatype: Literal["image", "document"] = "document") -> bool`
	- envia arquivo como documento ou imagem.

---

## Personalização de RPA (seletores)

Os seletores usados na automação ficam em `client/elements.py`.

Se o WhatsApp Web mudar a interface e quebrar o fluxo, atualize os seletores nesse arquivo (ex.: campo de busca, botão enviar, menu de anexo).

---

## Solução de problemas

- **Contato não encontrado**
	- confirme o nome exatamente como aparece no WhatsApp.

- **Timeout no login**
	- aumente `TIMEOUT` no `.env`;
	- rode com `headless=False` para visualizar o processo.

- **Erro ao enviar arquivo**
	- valide se o caminho existe e se o arquivo é acessível;
	- verifique se `mediatype` está correto (`document` ou `image`).

---

## Observações

- A automação depende dos seletores atuais do WhatsApp Web e pode exigir manutenção periódica.
- Use com responsabilidade e em conformidade com os termos da plataforma.
