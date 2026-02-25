"""Pacote client é responsável por criar a classe WhatsappClient, que é a interface para o usuário interagir com o WhatsApp Web. Ela utiliza a biblioteca Playwright para controlar o navegador e realizar as ações necessárias para enviar mensagens e arquivos para os contatos do WhatsApp.

Raises:
    TimeoutError: Error de timeout, caso o usuário não faça o login no tempo esperado ou caso o contato não seja encontrado.

Returns:
    bool: Retorna True se a ação foi realizada com sucesso, False caso contrário.
"""

import time
from pathlib import Path
from typing import Literal

from config import PATH_DOWNLOADS, PATH_USER_DATA, TIMEOUT, URL_WHATSAPP
from elements import (
    DOCUMENTS,
    FIND_CONVERSATION,
    IMAGES,
    INPUT_TEXT,
    IS_SEND,
    PLUS_ICON,
    QRCODE,
    SEND_BUTTON,
    SEND_BUTTON_ATTACHMENTS,
)
from playwright.sync_api import sync_playwright


class WhatsappClient:
    def __init__(self, headless: bool = True):
        self.page = None
        self.headless = headless
        self.browser = None
        self.playwright = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.close()

    def start(self):
        """Inicia uma pagina no navegador"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch_persistent_context(
            user_data_dir=PATH_USER_DATA,
            headless=self.headless,
            downloads_path=PATH_DOWNLOADS,
            timeout=TIMEOUT,
        )
        self.page = self.browser.new_page()

    def login(self):
        """Abre o WhatsApp Web e checa se já foi feito o scan do QRCODE ou se o usuario ainda vai logar"""
        self.page.goto(URL_WHATSAPP)
        try:
            # espera o elemento de pesquisar contato aparecer para saber que já logou, se não aparecer é porque precisa logar
            self.page.wait_for_selector(
                FIND_CONVERSATION,
                timeout=TIMEOUT,
            )
            print("Logged in to WhatsApp Web successfully.")
            return True
        except TimeoutError:
            if self.page.wait_for_selector(QRCODE):
                print(
                    "Please scan the QR code to log in to WhatsApp Web and execute the script again."
                )
                try:
                    self.page.wait_for_selector(
                        FIND_CONVERSATION,
                        timeout=TIMEOUT,
                    )
                    return True
                except TimeoutError:
                    print("Login timed out.")
                    raise TimeoutError("Scan the QR code and run it again.")

    def find_contact(self, contact: str):
        """Procura o contato, ou grupo na barra de pesquisa do WhatsApp Web e clica nele para abrir a conversa

        Args:
            contact (str): Nome (ou número) do contato ou grupo a ser encontrado

        Returns:
            bool: Retorna True se o contato foi encontrado, False caso contrário
        """
        self.page.query_selector(FIND_CONVERSATION).fill(contact)
        self.page.keyboard.press("Enter")
        try:
            # procura o elemento de digitar msg para saber que encontrou o contato
            self.page.wait_for_selector(INPUT_TEXT)
        except TimeoutError:
            print(f"Contact '{contact}' not found.")
            return False
        return True

    def send_text(self, contact: str, message: str):
        """Envia uma mensagem de texto para o contato passado

        Args:
            contact (str): Nome (ou número) do contato ou grupo a ser encontrado
            message (str): Mensagem a ser enviada

        Returns:
            bool: Retorna True se a mensagem foi enviada com sucesso, False caso contrário
        """
        self.login()
        if self.find_contact(contact):
            try:
                self.page.fill(INPUT_TEXT, message)
                self.page.click(SEND_BUTTON)
                # espera o IS_SEND sumir da tela, ficar detached
                self.page.wait_for_selector(IS_SEND, state="detached")
                print(f"Message '{message}' sent to {contact}.")
                return True
            except Exception as e:
                print(f"Err in send message to {contact}: {e}")
                return False
        return False

    def send_file(
        self,
        file: Path,
        contact: str,
        caption: str = None,
        mediatype: Literal["image", "document"] = "document",
    ):
        """Envia um arquivo para o contato passado

        Args:
            file (Path): Caminho do arquivo a ser enviado
            contact (str): Nome (ou número) do contato ou grupo a ser encontrado
            caption (str, optional): Texto a ser adicionado ao anexo. Defaults to None.
            mediatype (Literal["image", "document"], optional): Tipo do arquivo a ser enviado. Defaults to "document".

        Returns:
            bool: Retorna True se o arquivo foi enviado com sucesso, False caso contrário
        """
        self.login()
        if self.find_contact(contact):
            try:
                if mediatype == "document":
                    print("Sending document")
                    # se o mediatype for documento abre o explore de arquivos (.pdf,.xlsx e etc.)
                    self.page.click(PLUS_ICON)
                    with self.page.expect_file_chooser() as fc_info:
                        self.page.click(DOCUMENTS)
                    fc = fc_info.value
                    # seta o arquivo desse explorador sendo o file do argumento
                    fc.set_files(file)
                else:
                    print("Sending image")
                    # se o mediatype for image abre o explore de arquivos (.jpg,.png e etc.)
                    self.page.click(PLUS_ICON)
                    with self.page.expect_file_chooser() as fc_info:
                        self.page.click(IMAGES)
                    fc = fc_info.value
                    # seta o arquivo desse explorador sendo o file do argumento
                    fc.set_files(file)
                if caption:
                    # adiciona um texto ao anexo
                    self.page.fill(INPUT_TEXT, caption)
                self.page.click(SEND_BUTTON_ATTACHMENTS)
                time.sleep(3)
                # espera o IS_SEND sumir da tela, ficar detached
                self.page.wait_for_selector(IS_SEND, state="detached", timeout=TIMEOUT)
                print(f"File '{file.name}', sent to {contact}.")
                return True
            except TimeoutError as e:
                print(f"Error sending file to {contact}: {e}")
                return False
        return False
