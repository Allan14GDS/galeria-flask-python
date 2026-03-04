# 📸 Galeria de Fotos Full Stack (Python + Flask)

Este é um projeto Full Stack desenvolvido do zero para criar uma galeria de fotos dinâmica. O sistema possui o ciclo CRUD completo (Create, Read, Update, Delete) com armazenamento em um banco de dados MySQL e gerenciamento de arquivos físicos no servidor, aliado a uma interface de usuário (UI) moderna e responsiva.

## 🚀 Funcionalidades da Aplicação

- **Upload via Drag and Drop (Create):** Área interativa para envio de arquivos arrastando e soltando ou clicando, com validação de segurança (`secure_filename`). As imagens são salvas localmente na pasta `static/uploads`.
- **Leitura de Dados e Visualização Avançada (Read):** Exibição dinâmica das fotos usando o motor Jinja2. Conta com um visualizador em tela cheia (Modal/Lightbox) acionado ao clicar nas imagens, permitindo visualizar os detalhes sem recarregar a página.
- **Edição de Títulos (Update):** Interface dedicada para renomear o título de fotos já enviadas, atualizando os registros em tempo real no banco de dados.
- **Exclusão Completa (Delete):** Remoção de um registro específico, que apaga a linha no banco de dados e remove fisicamente o arquivo da pasta do servidor para otimizar o armazenamento.
- **Prevenção de Exclusão Acidental:** Implementação de alertas de confirmação em JavaScript para evitar a deleção indesejada de registros.
- **Notificações Flutuantes (Toasts):** Sistema de alertas visuais animados e auto-destrutivos que notificam o usuário instantaneamente sobre o sucesso de suas ações de forma não intrusiva.
- **Interface Premium (Masonry Layout & UI Polish):** Design profissional utilizando tipografia moderna (Inter), sombras difusas, variáveis CSS e grid dinâmico (Masonry). As imagens mantêm suas proporções originais sem cortes e os cartões se reorganizam automaticamente conforme o dispositivo.

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3, Flask, Werkzeug
- **Banco de Dados:** MySQL, PyMySQL
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla), Jinja2

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
