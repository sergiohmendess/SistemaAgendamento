from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Inicializa a instância do SQLAlchemy
db = SQLAlchemy()

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    horario = db.Column(db.String(20), nullable=False)
    data_agendamento = db.Column(db.Date, nullable=False)
    tipo_volume = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))  # Chave estrangeira para Usuario
    
    usuario = db.relationship('Usuario', backref=db.backref('agendamentos', lazy=True))  # Relacionamento com Usuario
    
    def __repr__(self):
        return f'<Agendamento {self.nome}>'

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    phone_number = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return f'<Usuario {self.username}>'
