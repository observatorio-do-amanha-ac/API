def generate_route(item):
    try:
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            return f"https://drive.google.com/drive/folders/{item['id']}"
        else:
            return f"https://drive.google.com/file/d/{item['id']}/view"
    except KeyError:
        raise ValueError("Erro ao gerar link para o item")
