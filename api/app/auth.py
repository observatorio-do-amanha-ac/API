import logging
from google.auth import credentials
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuração de log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Escopos e arquivo de credenciais para Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'

def authenticate():
    """Autentica a conta de serviço e retorna o serviço do Google Drive"""
    creds = None
    try:
        # Carregar as credenciais da conta de serviço
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        # Criar o serviço para a API do Google Drive
        drive_service = build('drive', 'v3', credentials=creds)
        logger.info("Autenticação bem-sucedida.")
        return drive_service

    except Exception as e:
        logger.error(f"Erro ao autenticar com a conta de serviço: {e}")
        return None

# Chame a função para autenticar e obter o serviço
drive_service = authenticate()
