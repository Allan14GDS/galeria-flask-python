# 📸 Galeria de Fotos Full Stack (SaaS Architecture)

Este é um projeto Full Stack em Python (Flask) que evoluiu de uma galeria simples para uma arquitetura **Multi-tenant (SaaS)**. O sistema possui autenticação de usuários, isolamento de banco de dados, armazenamento local de arquivos e uma interface premium de alta interatividade.

## 🚀 Funcionalidades da Aplicação

- **Autenticação e Segurança:** Sistema completo de Login e Cadastro de usuários utilizando `Flask-Login`. As senhas são protegidas com hash criptográfico via `Werkzeug Security`.
- **Arquitetura Multi-tenant:** Rotas protegidas (`@login_required`) e isolamento de dados no MySQL. Cada usuário tem acesso exclusivo apenas às fotos que ele mesmo enviou (através de Foreign Keys).
- **Upload via Drag and Drop:** Área interativa para envio de arquivos arrastando e soltando, com validação de segurança (`secure_filename`).
- **Leitura de Dados e Visualização Avançada:** Exibição dinâmica usando Jinja2 e um visualizador em tela cheia (Modal/Lightbox) sem recarregamento de página.
- **Edição e Exclusão com Validação:** Permite renomear títulos e excluir fotos com segurança. A exclusão remove a linha no banco e também o arquivo físico do servidor, evitando acúmulo de lixo.
- **Notificações Flutuantes (Toasts):** Alertas visuais animados e auto-destrutivos que informam o sucesso ou erro das ações do usuário.
- **Interface Premium (UI/UX):** Design responsivo com grid Masonry, paleta de cores moderna (variáveis CSS), sombras difusas e tipografia Inter (Google Fonts).

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3, Flask, Flask-Login, Werkzeug
- **Banco de Dados:** MySQL, PyMySQL
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla), Jinja2

## ⚙️ Como Rodar o Projeto Localmente

### 1. Preparando o Banco de Dados

Certifique-se de ter um servidor MySQL rodando. Execute o script abaixo para criar as tabelas e o relacionamento estrutural:

```sql
CREATE DATABASE galeria_db;
USE galeria_db;

-- Tabela de Usuários (Clientes)
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Fotos com vínculo ao Usuário Dono (Foreign Key)
CREATE TABLE fotos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    nome_arquivo VARCHAR(255) NOT NULL,
    data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_id INT,
    CONSTRAINT fk_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);
```

### 2. Configurando o Ambiente e Instalando Dependências

Abra o terminal, clone o repositório, ative o ambiente virtual e instale as bibliotecas:

```bash
git clone [https://github.com/SEU_USUARIO/galeria-flask-python.git](https://github.com/SEU_USUARIO/galeria-flask-python.git)
cd galeria-flask-python

# Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate  # No Linux/Mac use: source venv/bin/activate

# Instale os pacotes necessários
pip install Flask PyMySQL Werkzeug Flask-Login
```

_(Nota: Lembre-se de atualizar o `SEU_USUARIO` na URL acima pelo seu username real)._

### 3. Rodando o Servidor

Com o banco configurado e as dependências instaladas, inicie a aplicação:

```bash
python app.py
```

Acesse no seu navegador: `http://127.0.0.1:5000`
