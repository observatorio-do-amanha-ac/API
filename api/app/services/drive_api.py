from app.auth import drive_service

from app.auth import drive_service

def list_items_in_folder(folder_id, category=None):
    try:
        # Monta a query base para listar arquivos não excluídos da pasta especificada
        query = f"'{folder_id}' in parents and trashed = false"
        
        # Se uma categoria foi fornecida, aplica um filtro mais preciso
        if category:
            query += f" and name contains '{category}'"

        # Busca os arquivos no Google Drive
        items = drive_service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, mimeType)',
        ).execute().get('files', [])

        # Filtra arquivos com base em critérios adicionais (nome ou outros atributos)
        if category:
            items = [item for item in items if item['name'].startswith(category)]

        return items
    except Exception as e:
        raise RuntimeError(f"Erro ao listar arquivos na pasta {folder_id}: {e}")

def get_file_metadata(file_id):
    try:
        return drive_service.files().get(fileId=file_id).execute()
    except Exception as e:
        raise RuntimeError(f"Erro ao obter metadados do arquivo {file_id}: {e}")

def download_file_content(file_id, mime_type):
    try:
        if mime_type == 'application/vnd.google-apps.document':
            request = drive_service.files().export_media(
                fileId=file_id, mimeType="text/plain"
            )
        else:
            request = drive_service.files().get_media(fileId=file_id)

        return request.execute().decode("utf-8")
    except Exception as e:
        raise RuntimeError(f"Erro ao baixar conteúdo do arquivo {file_id}: {e}")
