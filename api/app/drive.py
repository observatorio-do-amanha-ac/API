from app.services.drive_api import list_items_in_folder, get_file_metadata, download_file_content, drive_service
from googleapiclient.errors import HttpError
from app.services.link_utils import generate_route
from app.services.file_utils import extract_range_from_name, extract_suffix_from_name
from app.config import logger
from rapidfuzz import process, fuzz
import json

DATASET_CATEGORIA_TO_FOLDER_ID = {
    "tecnologia": "1t9IsyVDU4Ai_LCL0d9zt-eWhbhAIZBZK",
    "educacao": "197vVMHXyHWE6hOvhpBREm4QnoapnZSjY",
    "empresarial": "1X9ZVOH19YSgrCwfoqWPZF_OnCOUkS18T",
    "inclusao_social": "1nL-uPH2brJsubkcK1kuMk65uq-LXyjiY",
    "inovacao": "1pZrEoicWNdPd6aF1LeHKOfzkXmpX9Op1",
    "meio_ambiente": "1rHiBbLfBFJx8vmRRzX8Nktl-2oX9Mbwm",
}

FOLDER_IDS = {
    "datasets": "1XexQGZBvMi8VZbRlyd440fpN0PqLBtdE",
    "descricoes": "1tfmOPNUbsxx0rQewx1FQnMaWmNk60X56",
    "imagens": "1h3Y6fCjAIl8f4k_ihPQJ5uZugFhIi30C",
    "conteudos": "14u-Rq0d3vVWWloB_1Etuw_l8nWe3sIIP",
    "fontes": "1etbIPBK9oC13u-_7DME76RDvH-pj3kMi",
    "extras": "1nqShlIuf2T3SHK8oJxK9T9RBYluhZ0Yy",
}

def extract_identifier(file_name):
    """
    Extrai um identificador único do nome do arquivo, ignorando intervalos e extensões.
    """
    file_name = file_name.lower()
    if '[' in file_name:
        # Remove intervalos [2020-2024] e extensões
        file_name = file_name.split(']')[-1]
    file_name = file_name.split('.')[0]
    return '_'.join(file_name.split('_')[-2:])

def find_best_match(identifier, items, threshold=80):
    """
    Encontra o item com maior similaridade ao identificador fornecido.
    """
    if not items:
        return None

    # Normalizar os nomes para comparação
    item_names = [item['name'].lower() for item in items]
    matches = process.extract(identifier, item_names, scorer=fuzz.partial_ratio)

    # Filtrar pelo threshold de similaridade
    best_match = max(matches, key=lambda x: x[1], default=None)
    if best_match and best_match[1] >= threshold:
        index = item_names.index(best_match[0])
        return items[index]
    return None
def list_items_by_category(category=None):
    try:
        if category not in DATASET_CATEGORIA_TO_FOLDER_ID:
            logger.error(f"Categoria inválida: {category}")
            return {"error": f"Categoria '{category}' não encontrada."}

        dataset_folder_id = DATASET_CATEGORIA_TO_FOLDER_ID[category]

        datasets = list_items_in_folder(dataset_folder_id)
        descricoes = list_items_in_folder(FOLDER_IDS["descricoes"])
        imagens = list_items_in_folder(FOLDER_IDS["imagens"])
        conteudos = list_items_in_folder(FOLDER_IDS["conteudos"])
        fontes = list_items_in_folder(FOLDER_IDS["fontes"])
        extras = list_items_in_folder(FOLDER_IDS["extras"])

        # Carregar o arquivo JSON com as configurações extras
        extra = get_json_data_from_drive(extras[0]["id"]) if extras else None
        if not extra or "data" not in extra:
            logger.error("Arquivo JSON com configurações extras não encontrado ou inválido.")
            return {"error": "Configurações extras não encontradas."}

        result = []

        for dataset in datasets:
            dataset_name = dataset['name'].lower()
            extra = get_json_data_from_drive(extras[0]["id"])
            identifier = extract_identifier(dataset_name)

            logger.info(f"Processando dataset: {dataset_name} | Identificador extraído: {identifier}")

            # Obter detalhes como intervalo e local
            range_inicial, range_final = extract_range_from_name(dataset['name'])
            if not range_inicial or not range_final:
                logger.warning(f"Intervalo inválido para o dataset {dataset_name}.")
                range_inicial, range_final = "N/A", "N/A"

            local = extract_suffix_from_name(dataset_name)

            # Buscar descrição associada
            descricao_item = find_best_match(identifier, descricoes)
            descricao_text = (
                download_file_content(descricao_item['id'], 'application/vnd.google-apps.document')
                if descricao_item else "Descrição não encontrada"
            )

            # Buscar imagem associada
            imagem_item = find_best_match(identifier, imagens)
            imagem_link = generate_route(imagem_item) if imagem_item else "Imagem não encontrada"

            # Buscar conteúdo associado
            conteudo_item = find_best_match(identifier, conteudos)
            conteudo_text = (
                download_file_content(conteudo_item['id'], 'application/vnd.google-apps.document')
                if conteudo_item else "Conteúdo não encontrado"
            )

            # Buscar fonte associada
            fonte_item = find_best_match(identifier, fontes)
            fonte_text = (
                download_file_content(fonte_item['id'], 'application/vnd.google-apps.document')
                if fonte_item else "Fonte não encontrada"
            )

            # Gerar link para o dataset
            dataset_link = generate_route(dataset)


            result.append({
                "id": dataset['id'],
                "dataset": dataset_link,
                "descricao": descricao_text,
                "imagem": imagem_link,
                "titulo": extra["data"].get(dataset['name']).get('titulo'),
                "range_inicial": range_inicial,
                "range_final": range_final,
                "local": local,
                "temas": extra["data"].get(dataset['name']).get('temas'),
                "palavrasChaves": extra["data"].get(dataset['name']).get('palavrasChaves'),
                "rota_front": f"/pesquisa/dataset?key={dataset['id']}",
                "conteudo": conteudo_text,
                "fonte": fonte_text,
            })

        logger.info(f"Resultados gerados para a categoria {category}: {result}")
        return result

    except Exception as e:
        logger.exception(f"Erro ao listar itens: {str(e)}")
        return []



def get_json_data_from_drive(id_planilha: str):
    try:
        logger.info(f"Acessando o arquivo no Drive com ID: {id_planilha}")

        # Obter os metadados do arquivo para validação
        file_metadata = drive_service.files().get(fileId=id_planilha).execute()
        logger.info(f"Metadados do arquivo: {file_metadata}")

        # Verificar se o arquivo é um JSON
        mime_type = file_metadata.get('mimeType', '')
        if mime_type != 'application/json':
            return {"error": "O arquivo não é um JSON válido."}

        # Ler o conteúdo do arquivo diretamente
        request = drive_service.files().get_media(fileId=id_planilha)
        file_content = request.execute()

        # Decodificar os dados do JSON
        json_data = json.loads(file_content)

        # Retornar os dados do JSON
        return {"data": json_data}

    except HttpError as err:
        logger.error(f"Erro ao acessar o arquivo no Drive: {err}")
        return {"error": f"Erro ao acessar o arquivo no Drive: {err}"}
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar o JSON: {e}")
        return {"error": f"Erro ao decodificar o JSON: {e}"}
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        return {"error": f"Erro inesperado: {e}"}