from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pymysql
import os
import base64
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'super_chave_secreta_do_pirata' # O Flask exige isso para os alertas!

# --- Configuração do Flask-Login ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redireciona usuários não logados para a tela de login
login_manager.login_message = "Por favor, faça login para acessar esta página."

# --- Modelo de Usuário ---
class Usuario(UserMixin):
    def __init__(self, id, nome, email):
        self.id = id
        self.nome = nome
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    conexao = conectar_banco()
    with conexao.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
        usuario_db = cursor.fetchone()
    conexao.close()
    
    if usuario_db:
        return Usuario(id=usuario_db['id'], nome=usuario_db['nome'], email=usuario_db['email'])
    return None

# Configuração de onde as fotos serão salvas fisicamente
PASTA_UPLOADS = 'static/uploads'
app.config['UPLOAD_FOLDER'] = PASTA_UPLOADS

# Truque de mestre: o código abaixo verifica se a pasta "uploads" existe. Se não existir, ele cria sozinho!
os.makedirs(PASTA_UPLOADS, exist_ok=True)

# Função para conectar ao banco
def conectar_banco():
    conexao = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="galeria_db"
    )
    return conexao

# ==========================================
# ROTAS DE AUTENTICAÇÃO (LOGIN E CADASTRO)
# ==========================================

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        conexao = conectar_banco()
        cursor = conexao.cursor(pymysql.cursors.DictCursor)
        
        # Verifica se o e-mail já existe no banco
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        se_existe = cursor.fetchone()

        if se_existe:
            flash("Este e-mail já está cadastrado. Faça o login.")
            conexao.close()
            return redirect(url_for('login'))

        # Criptografa a senha para o banco de dados não exibir a senha real
        senha_hash = generate_password_hash(senha)

        cursor.execute("INSERT INTO usuarios (nome, email, senha_hash) VALUES (%s, %s, %s)", (nome, email, senha_hash))
        conexao.commit()
        conexao.close()

        flash("Cadastro realizado com sucesso! Faça seu login para acessar o painel.")
        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conexao = conectar_banco()
        cursor = conexao.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario_db = cursor.fetchone()
        conexao.close()

        # Checa se o usuário existe e se a senha digitada bate com o hash salvo
        if usuario_db and check_password_hash(usuario_db['senha_hash'], senha):
            usuario = Usuario(id=usuario_db['id'], nome=usuario_db['nome'], email=usuario_db['email'])
            login_user(usuario)
            flash(f"Bem-vindo(a) de volta, {usuario.nome}!")
            return redirect(url_for('index'))
        else:
            flash("E-mail ou senha incorretos.")

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.")
    return redirect(url_for('login'))

# ==========================================
# ROTAS DO PAINEL DA GALERIA (PROTEGIDAS)
# ==========================================

@app.route('/')
def index():
    # 1. Se o usuário NÃO estiver logado, ele vê a Página Inicial (Vitrine)
    if not current_user.is_authenticated:
        return render_template('landing.html')
        
    # 2. Se ele já estiver logado, o sistema carrega o Dashboard dele!
    conexao = conectar_banco()
    cursor = conexao.cursor(pymysql.cursors.DictCursor)
    # Traz apenas as fotos que pertencem ao usuário logado no momento
    cursor.execute("SELECT * FROM fotos WHERE usuario_id = %s ORDER BY data_upload DESC", (current_user.id,))
    fotos_db = cursor.fetchall()
    conexao.close()
    
    return render_template('index.html', fotos_para_tela=fotos_db)

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'foto' not in request.files:
        flash('Nenhum arquivo enviado.')
        return redirect(request.url)
    
    foto = request.files['foto']
    titulo = request.form['titulo']
    
    if foto.filename == '':
        flash('Nenhum arquivo selecionado.')
        return redirect(request.url)
        
    if foto:
        nome_seguro = secure_filename(foto.filename)
        caminho_completo = os.path.join(app.config['UPLOAD_FOLDER'], nome_seguro)
        foto.save(caminho_completo)
        
        conexao = conectar_banco()
        cursor = conexao.cursor()
        # Salva a foto e vincula o ID do usuário atual (current_user.id)
        cursor.execute("INSERT INTO fotos (titulo, nome_arquivo, usuario_id) VALUES (%s, %s, %s)", (titulo, nome_seguro, current_user.id))
        conexao.commit()
        conexao.close()
        
        flash('Foto enviada com sucesso!')
        return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_foto(id):
    conexao = conectar_banco()
    cursor = conexao.cursor(pymysql.cursors.DictCursor)
    
    # 1. Busca a foto atual para sabermos o nome do arquivo original
    cursor.execute("SELECT * FROM fotos WHERE id = %s AND usuario_id = %s", (id, current_user.id))
    foto_db = cursor.fetchone()
    
    if not foto_db:
        flash('Foto não encontrada ou você não tem permissão para editá-la.')
        conexao.close()
        return redirect(url_for('index'))

    if request.method == 'POST':
        novo_titulo = request.form['titulo']
        imagem_base64 = request.form.get('imagem_base64')
        nome_arquivo_atual = foto_db['nome_arquivo']
        
        # 2. Verifica se veio uma imagem editada do Canvas (se o Base64 não está vazio)
        if imagem_base64 and ',' in imagem_base64:
            # Separa o cabeçalho "data:image/jpeg;base64," do código da imagem em si
            cabecalho, codigo_imagem = imagem_base64.split(',', 1)
            
            # Gera um novo nome para evitar que o navegador mostre a imagem velha (Cache)
            novo_nome = f"editada_{uuid.uuid4().hex}.jpg"
            caminho_novo = os.path.join(app.config['UPLOAD_FOLDER'], novo_nome)
            caminho_antigo = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo_atual)
            
            # Decodifica e salva o novo arquivo físico
            with open(caminho_novo, "wb") as arquivo:
                arquivo.write(base64.b64decode(codigo_imagem))
                
            # Apaga o arquivo antigo do servidor para economizar espaço
            if os.path.exists(caminho_antigo):
                os.remove(caminho_antigo)
                
            # Atualiza a variável para salvar o novo nome no banco de dados
            nome_arquivo_atual = novo_nome

        # 3. Atualiza o banco de dados (título e o novo nome do arquivo, se houver)
        cursor.execute("UPDATE fotos SET titulo = %s, nome_arquivo = %s WHERE id = %s AND usuario_id = %s", 
                       (novo_titulo, nome_arquivo_atual, id, current_user.id))
        conexao.commit()
        conexao.close()
        
        flash('Foto editada e salva com sucesso!')
        return redirect(url_for('index'))
        
    conexao.close()
    return render_template('editar.html', foto=foto_db)

@app.route('/deletar/<int:id>', methods=['POST'])
@login_required
def deletar_foto(id):
    conexao = conectar_banco()
    cursor = conexao.cursor(pymysql.cursors.DictCursor)
    
    # Busca o nome do arquivo, garantindo que pertence ao usuário
    cursor.execute("SELECT nome_arquivo FROM fotos WHERE id = %s AND usuario_id = %s", (id, current_user.id))
    foto_db = cursor.fetchone()
    
    if foto_db:
        nome_arquivo = foto_db['nome_arquivo']
        caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
        
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)
            
        cursor.execute("DELETE FROM fotos WHERE id = %s AND usuario_id = %s", (id, current_user.id))
        conexao.commit()
        flash('Foto excluída permanentemente.')
    else:
        flash('Erro ao excluir: Foto não encontrada ou sem permissão.')

    conexao.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)