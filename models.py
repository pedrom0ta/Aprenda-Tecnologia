from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f'<Usuario {self.email}>'


class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.Text)
    icone = db.Column(db.String(50), default='bi-play-circle')
    aulas = db.relationship('VideoAula', backref='categoria', lazy=True)

    @property
    def total_aulas(self):
        return len(self.aulas)

    def __repr__(self):
        return f'<Categoria {self.nome}>'


class VideoAula(db.Model):
    __tablename__ = 'video_aulas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    youtube_url = db.Column(db.String(500), nullable=False)   # URL original salva
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    visualizacoes = db.Column(db.Integer, default=0)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def youtube_id(self):
        """Extrai o ID do vídeo de qualquer formato de URL do YouTube."""
        patterns = [
            r'(?:v=)([a-zA-Z0-9_-]{11})',          # ?v=ID
            r'(?:youtu\.be/)([a-zA-Z0-9_-]{11})',   # youtu.be/ID
            r'(?:embed/)([a-zA-Z0-9_-]{11})',        # embed/ID
            r'(?:shorts/)([a-zA-Z0-9_-]{11})',       # shorts/ID
        ]
        for pattern in patterns:
            match = re.search(pattern, self.youtube_url)
            if match:
                return match.group(1)
        return None

    @property
    def embed_url(self):
        vid_id = self.youtube_id
        if vid_id:
            return f'https://www.youtube.com/embed/{vid_id}?rel=0&modestbranding=1'
        return None

    @property
    def thumbnail_url(self):
        vid_id = self.youtube_id
        if vid_id:
            return f'https://img.youtube.com/vi/{vid_id}/hqdefault.jpg'
        return None

    def __repr__(self):
        return f'<VideoAula {self.titulo}>'
