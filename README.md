# 📸 Galeria de Fotos Full Stack (Python + Flask)

Este é um projeto Full Stack desenvolvido do zero para criar uma galeria de fotos dinâmica. O sistema permite o upload de imagens, armazenamento em um banco de dados MySQL e a exclusão completa (tanto do banco quanto do arquivo físico no servidor).

## 🚀 Funcionalidades Até o Momento

- **Upload de Imagens:** Envio de arquivos de imagem via formulário HTML (`enctype="multipart/form-data"`).
- **Armazenamento Seguro:** As imagens são salvas localmente na pasta `static/uploads` com nomes validados pelo `secure_filename`.
- **Leitura de Dados (Read):** Exibição dinâmica das fotos cadastradas no banco de dados diretamente na interface web usando o motor de templates Jinja2.
- **Exclusão de Dados (Delete):** Remoção de um registro específico, que apaga a linha no banco de dados e remove fisicamente o arquivo da pasta do servidor para otimizar armazenamento.

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3, Flask, Werkzeug
- **Banco de Dados:** MySQL, PyMySQL
- **Frontend:** HTML5, CSS3, Jinja2

## ⚙️ Como Rodar o Projeto Localmente

### 1. Preparando o Banco de Dados

Certifique-se de ter um servidor MySQL rodando (como XAMPP ou WAMP). Rode o script abaixo no seu banco para criar a estrutura necessária:

```sql
CREATE DATABASE galeria_db;
USE galeria_db;

CREATE TABLE fotos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    nome_arquivo VARCHAR(255) NOT NULL,
    data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Configurando o Ambiente

Abra o terminal, clone este repositório e acesse a pasta do projeto:

```bash
git clone [https://github.com/SEU_USUARIO/galeria-flask-python.git](https://github.com/SEU_USUARIO/galeria-flask-python.git)
cd galeria-flask-python
```

_(Nota: Troque `SEU_USUARIO` pelo seu nome de usuário do GitHub)_

### 3. Instalando as Dependências

Crie um ambiente virtual e instale as bibliotecas necessárias:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Rodando o Servidor

Com o banco configurado e as dependências instaladas, inicie a aplicação:

```bash
python app.py
```

Acesse no seu navegador: `http://127.0.0.1:5000`
