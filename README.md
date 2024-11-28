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
   * Credencial Google Drive
   Mover o arquivo de credencial para a pasta `api` do projeto.
5. **Executar a API**
   ```bash
   uvicorn app.main:app --reload
   ```
6. **Acessar a Documentação da API**
   Acessar `http://127.0.0.1:8000/docs` no navegador.

**Observações:**
* Certifique-se de que o arquivo de credenciais foi colocado corretamente.
* Para acessar a API, utilize `http://127.0.0.1:8000`.

Siga os passos acima para configurar e executar a API localmente.
```

**Opção 2: Com Melhorias Visuais e Organização**

```markdown
##  Iniciando sua API: Um Guia Completo

### Pré-requisitos
* **Python 3.8+:** Certifique-se de ter o Python instalado.
* **Terminal:** Você precisará de um terminal para executar os comandos.

### 1. Crie um Ambiente Virtual
```bash
python -m venv .venv
```
Isso isola as dependências do seu projeto.

### 2. Ative o Ambiente Virtual
* **Windows:**
  ```bash
  .venv\Scripts\activate
  ```
* **Linux/MacOS:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Instale as Dependências
```bash
pip install fastapi uvicorn pydantic aiofiles python-dotenv google-auth ...
```

### 4. Configure as Credenciais
* **Baixe:** Obtenha o arquivo de credenciais do Google Drive.
* **Mova:** Coloque o arquivo na pasta `api` do seu projeto.

### 5. Inicie a API
```bash
uvicorn app.main:app --reload
```

### 6. Explore a Documentação
Acesse `http://127.0.0.1:8000/docs` para ver a documentação interativa da sua API.

**Observação:**
* **Credenciais:** Certifique-se de que o arquivo de credenciais está no local correto.
* **Acesso:** Use `http://127.0.0.1:8000` para acessar sua API.

