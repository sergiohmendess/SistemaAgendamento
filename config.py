import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente de um arquivo .env, se presente
load_dotenv()

class Config:
    # Chave secreta para gerenciar sessões e proteção CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24).hex()

    # Configuração do banco de dados PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:minhadeusa@localhost:5432/agendamento_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configurações do e-mail para envio de mensagens
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'caosgangsupply@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'minhadeusa')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').strip().lower() in ['true', '1']
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').strip().lower() in ['true', '1']
