from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_mail import Mail, Message
from flask_migrate import Migrate  # Importa Migrate
from models import db, Agendamento, Usuario  # Importa a instância db e modelos

# Inicializa a aplicação Flask
app = Flask(__name__)
app.config.from_object('config.Config')

# Inicializa o banco de dados e o serviço de e-mail
db.init_app(app)  # Usa init_app para associar o SQLAlchemy com a aplicação Flask
mail = Mail(app)
migrate = Migrate(app, db)  # Configura o Flask-Migrate

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        horario = request.form.get('horario')
        data_agendamento = datetime.strptime(request.form.get('data_agendamento'), '%Y-%m-%d')
        tipo_volume = request.form.get('tipo_volume')

        novo_agendamento = Agendamento(
            nome=nome,
            telefone=telefone,
            email=email,
            horario=horario,
            data_agendamento=data_agendamento,
            tipo_volume=tipo_volume,
            usuario_id=session.get('user_id')  # Associa o agendamento ao usuário logado, se estiver logado
        )
        db.session.add(novo_agendamento)
        db.session.commit()
        
        # Enviar e-mail de confirmação
        msg = Message('Confirmação de Agendamento',
                      sender='caosgangsupply@gmail.com',  # Usando e-mail fornecido
                      recipients=[email])
        msg.body = f'Olá {nome},\n\nSeu agendamento foi realizado com sucesso!\nData: {data_agendamento.strftime("%d/%m/%Y")}\nHora: {horario}\nTipo: {tipo_volume}'
        mail.send(msg)
        
        flash('Agendamento realizado com sucesso!', 'success')
        return redirect(url_for('home'))

    return render_template('agendar.html')

@app.route('/visualizar')
def visualizar():
    if 'user_id' not in session or not Usuario.query.get(session['user_id']).is_admin:
        flash('Acesso restrito!', 'warning')
        return redirect(url_for('login'))
    
    agendamentos = Agendamento.query.all()
    return render_template('visualizar.html', agendamentos=agendamentos)

@app.route('/painel', methods=['GET', 'POST'])
def painel():
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar essa página.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'logout' in request.form:
            session.pop('user_id', None)
            flash('Você foi desconectado.', 'info')
            return redirect(url_for('login'))
        elif 'update_phone' in request.form:
            new_phone = request.form.get('phone_number')
            user = Usuario.query.get(session['user_id'])
            user.phone_number = new_phone  # Corrigido de phone_number para phone_number
            db.session.commit()
            flash('Número de telefone atualizado com sucesso!', 'success')

    user = Usuario.query.get(session['user_id'])
    return render_template('painel.html', phone_number=user.phone_number)  # Corrigido para phone_number

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Usuario.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):  # Usa check_password_hash para comparar senhas
            session['user_id'] = user.id
            if user.is_admin:
                return redirect(url_for('visualizar'))
            else:
                return redirect(url_for('agendar'))
        flash('Usuário ou senha incorretos.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if Usuario.query.filter_by(username=username).first():
            flash('Usuário já existe.', 'danger')
            return redirect(url_for('register'))

        new_user = Usuario(username=username, password_hash=generate_password_hash(password), is_admin=False)  # Hash a senha
        db.session.add(new_user)
        db.session.commit()
        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar essa página.', 'warning')
        return redirect(url_for('login'))
    
    user = Usuario.query.get(session['user_id'])
    if request.method == 'POST':
        if 'update_password' in request.form:
            old_password = request.form.get('old_password')
            new_password = request.form.get('new_password')
            if check_password_hash(user.password_hash, old_password):  # Usa check_password_hash para verificar a senha antiga
                user.password_hash = generate_password_hash(new_password)  # Hash a nova senha
                db.session.commit()
                flash('Senha atualizada com sucesso!', 'success')
            else:
                flash('Senha antiga incorreta.', 'danger')
    return render_template('perfil.html', phone_number=user.phone_number)  # Corrigido para phone_number

@app.route('/admin/usuarios', methods=['GET', 'POST'])
def admin_usuarios():
    if 'user_id' not in session or not Usuario.query.get(session['user_id']).is_admin:
        flash('Acesso restrito!', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'delete_user' in request.form:
            user_id = request.form.get('user_id')
            user = Usuario.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                flash('Usuário deletado com sucesso!', 'success')

    usuarios = Usuario.query.all()
    return render_template('admin_usuarios.html', usuarios=usuarios)

if __name__ == "__main__":
    app.run(debug=True)
