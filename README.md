# 📸 Galeria Pro - SaaS & Advanced Image Editor

Este projeto evoluiu de uma simples galeria para uma plataforma **Full Stack (SaaS)** completa. Inspirado no Adobe Lightroom, o sistema oferece uma experiência de edição profissional diretamente no navegador, utilizando processamento matemático de pixels e ferramentas de manipulação de imagem de alto nível.

## 🚀 Novas Funcionalidades Premium

- **Landing Page Cinematográfica:** Interface de entrada imersiva com Dark Mode e efeito Glassmorphism.
- **Estúdio de Edição (Engine Canvas):** Motor de renderização em tempo real que permite ajustes finos de Exposição, Contraste, Realces, Sombras, Brancos, Pretos e Saturação.
- **Sistema de Predefinições (Presets):** Aplicação de filtros profissionais (Cinematográfico, Vintage, P&B Pro) com apenas um clique.
- **Ferramenta de Corte (Crop Pro):** Integração com a biblioteca `Cropper.js` para redimensionamento de fotos com grade de "Regra dos Terços" e proporções fixas (1:1, 16:9, 4:3).
- **Exportação HD:** Funcionalidade de download instantâneo da imagem editada em alta definição diretamente para o computador do usuário.
- **Autenticação com UX Fluida:** Modais de login e páginas de cadastro consistentes com a identidade visual do software.

## 🛠️ Tecnologias de Ponta

- **Backend:** Python 3 + Flask
- **Banco de Dados:** MySQL com arquitetura Multi-tenant (isolamento de dados por usuário)
- **Processamento de Imagem:** HTML5 Canvas API + Cropper.js
- **Frontend:** Modern CSS (Flexbox/Grid), Variáveis, Backdrop-filter e Vanilla JavaScript

## ⚙️ Instalação e Configuração

### 1. Requisitos de Banco de Dados

Execute o script SQL para estruturar o seu ambiente MySQL:

```sql
CREATE DATABASE galeria_db;
USE galeria_db;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL
);

CREATE TABLE fotos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    nome_arquivo VARCHAR(255) NOT NULL,
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);
```

### 2. Rodando o Projeto

```bash
# Clone o repositório
git clone [https://github.com/Allan14GDS/projeto-galeria-fotos.git](https://github.com/Allan14GDS/projeto-galeria-fotos.git)

# Instale as dependências
pip install Flask PyMySQL Werkzeug Flask-Login

# Execute a aplicação
python app.py
```

## 📈 Roadmap de Evolução

- [x] Motor de processamento via Canvas
- [x] Ferramenta de Crop (Recorte)
- [x] Sistema de Presets
- [ ] Gráfico de Curva de Tons (Fase 3)
- [ ] Deploy em Nuvem (AWS/Heroku)
