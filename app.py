from flask import Flask, render_template, request, redirect, url_for
import pymysql
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

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

# Rota principal (A página inicial)
# Rota principal (A página inicial)
@app.route('/')
def home():
    # 1. Abre a ponte com o banco de dados
    conexao = conectar_banco()
    
    # Usamos o DictCursor para o Python entender os dados como um Dicionário (facilita muito no HTML!)
    cursor = conexao.cursor(pymysql.cursors.DictCursor)
    
    # 2. Busca todas as fotos, ordenando da mais nova para a mais velha
    cursor.execute("SELECT * FROM fotos ORDER BY id DESC")
    fotos_do_banco = cursor.fetchall() # Pega todos os resultados
    
    # 3. Fecha as conexões
    cursor.close()
    conexao.close()
    
    # 4. Manda as fotos para o nosso arquivo HTML!
    return render_template('index.html', fotos_para_tela=fotos_do_banco)

# Rota que recebe a foto quando você clica em "Fazer Upload"
@app.route('/upload', methods=['POST'])
def upload_foto():
    # 1. Pega os dados que vieram do formulário HTML
    titulo = request.form['titulo']
    foto = request.files['foto']

    if foto.filename != '':
        # 2. Limpa o nome do arquivo para evitar bugs (tira espaços, acentos, etc)
        nome_arquivo = secure_filename(foto.filename)
        
        # 3. Salva a imagem fisicamente na pasta static/uploads
        caminho_completo = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
        foto.save(caminho_completo)

        # 4. Salva as informações no Banco de Dados MySQL
        conexao = conectar_banco()
        cursor = conexao.cursor()
        sql = "INSERT INTO fotos (titulo, nome_arquivo) VALUES (%s, %s)"
        cursor.execute(sql, (titulo, nome_arquivo))
        conexao.commit() # Confirma a gravação!
        cursor.close()
        conexao.close()

    # 5. Recarrega a página inicial
    return redirect(url_for('home'))

# Rota para deletar uma foto
@app.route('/deletar/<int:id>', methods=['POST'])
def deletar_foto(id):
    conexao = conectar_banco()
    cursor = conexao.cursor(pymysql.cursors.DictCursor)
    
    # 1. Busca o nome do arquivo no banco de dados para podermos apagar o arquivo físico
    cursor.execute("SELECT nome_arquivo FROM fotos WHERE id = %s", (id,))
    foto = cursor.fetchone() # Pega apenas o resultado específico
    
    if foto:
        # 2. Apaga a imagem fisicamente da pasta static/uploads
        caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], foto['nome_arquivo'])
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)
        
        # 3. Apaga o registro do banco de dados
        cursor.execute("DELETE FROM fotos WHERE id = %s", (id,))
        conexao.commit() # Confirma a exclusão!
        
    cursor.close()
    conexao.close()
    
    # 4. Recarrega a página inicial
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)