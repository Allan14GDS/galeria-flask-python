# 📸 Galeria de Fotos Full Stack (SaaS & Advanced Photo Editor)

Este é um projeto Full Stack em Python (Flask) estruturado como um **SaaS (Software as a Service)**. O sistema possui autenticação de usuários, isolamento de banco de dados e um **Estúdio de Edição de Imagens Profissional** embutido, capaz de processar pixels em tempo real diretamente no navegador.

## 🚀 Funcionalidades da Aplicação

- **Estúdio de Edição (Motor Canvas):** Interface de edição inspirada no Lightroom (Dark Mode). Processamento matemático de imagem no lado do cliente utilizando HTML5 `<canvas>`.
- **Manipulação de Pixels:** Algoritmos de luminância para ajustes finos de Exposição, Contraste, Realces (Highlights), Sombras, Brancos e Pretos.
- **Processamento Backend Seguro:** Recepção assíncrona da imagem editada via Base64. O Flask decodifica, gera um hash único (`uuid`) para evitar cache do navegador, salva o novo arquivo físico e deleta a versão anterior para economizar armazenamento.
- **Autenticação e Segurança (SaaS):** Login e Cadastro de usuários utilizando `Flask-Login` e proteção de senhas com `Werkzeug Security`.
- **Arquitetura Multi-tenant:** Rotas trancadas (`@login_required`) e isolamento no MySQL (Foreign Keys). Usuários interagem estritamente com seus próprios arquivos.
- **Upload via Drag and Drop:** Área interativa para envio de arquivos físicos arrastando e soltando.
- **Interface Premium (UI/UX):** Design responsivo com grid Masonry, notificações flutuantes (Toasts auto-destrutivos), Lightbox (Modal para tela cheia) e tipografia Inter.

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3, Flask, Flask-Login, Werkzeug, UUID, Base64
- **Banco de Dados:** MySQL, PyMySQL
- **Frontend:** HTML5 Canvas (Image Processing), CSS3 (Variáveis & Dark Theme), JavaScript (Vanilla), Jinja2

## ⚙️ Como Rodar o Projeto Localmente

### 1. Preparando o Banco de Dados

Certifique-se de ter um servidor MySQL rodando. Execute o script abaixo para criar as tabelas e a estrutura de relacionamento (Multi-tenant):

```sql
CREATE DATABASE galeria_db;
USE galeria_db;

-- Tabela de Usuários
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Fotos (Relacionada ao Usuário)
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

_(Nota: Lembre-se de atualizar o `SEU_USUARIO` na URL acima pelo seu username real no GitHub)._

### 3. Rodando o Servidor

Inicie a aplicação:

```bash
python app.py
```

Acesse no seu navegador: `http://127.0.0.1:5000`
