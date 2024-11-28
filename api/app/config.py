# app/config.py
import logging
import os
from google.oauth2.service_account import Credentials

# Configuração do Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Escopos para o Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']

# Arquivo de credenciais
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_CREDENTIALS_PATH', 'credentials.json')

# Função para obter as credenciais
def get_credentials():
    """
    Função que carrega as credenciais da conta de serviço para autenticação no Google API.
    Retorna um objeto de credenciais para uso nas operações da API.
    """
    try:
        credentials = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        logger.info("Credenciais carregadas com sucesso.")
        return credentials
    except Exception as e:
        logger.error(f"Erro ao carregar credenciais: {e}")
        return None
