# Instruções de Inicialização da API

**Opção 1: Mantendo a Estrutura Original**

```markdown
# Instruções de Inicialização da API

Este guia descreve os passos necessários para configurar e executar a API.

## Pré-requisitos
* **Python** instalado (versão 3.8 ou superior).
* Acesso ao terminal ou prompt de comando.

## Passos de Inicialização
1. **Criar o ambiente virtual**
   ```bash
   python -m venv .venv
   ```
2. **Ativar o ambiente virtual**
   * **Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   * **Linux/MacOS:**
     ```bash
     source .venv/bin/activate
     ```
3. **Instalar as dependências**
   ```bash
   pip install fastapi uvicorn pydantic aiofiles python-dotenv google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client simplejson rapidfuzz
   ```
4. **Baixar a credencial**
   Faça o download da credencial a partir do link abaixo:
   
   * https://drive.google.com/file/d/1yshtWv_qyzsZHtGjMScrFefsRge3bjIg/view?usp=sharing
   * Credencial Google Drive
     
   Mover o arquivo de credencial para a pasta `api` do projeto.
6. **Executar a API**
   ```bash
   uvicorn app.main:app --reload
   ```
7. **Acessar a Documentação da API**
   Acessar `http://127.0.0.1:8000/docs` no navegador.

**Observações:**
* Certifique-se de que o arquivo de credenciais foi colocado corretamente.
* Para acessar a API, utilize `http://127.0.0.1:8000`.

Siga os passos acima para configurar e executar a API localmente.
