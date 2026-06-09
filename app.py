import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, Usuario, Categoria, VideoAula
from forms import LoginForm, VideoAulaForm, CategoriaForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aprenda-tecnologia-secret-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aprenda_tecnologia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.context_processor
def inject_nav_categories():
    return dict(categorias_nav=Categoria.query.all())

# ──────────────────────────────────────────────
# ROTAS PÚBLICAS
# ──────────────────────────────────────────────

@app.route('/')
def index():
    search = request.args.get('q', '').strip()
    categoria_id = request.args.get('categoria', type=int)
    query = VideoAula.query

    if search:
        query = query.filter(VideoAula.titulo.ilike(f'%{search}%'))
    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)

    aulas = query.order_by(VideoAula.criado_em.desc()).all()
    categorias = Categoria.query.all()
    categoria_selecionada = Categoria.query.get(categoria_id) if categoria_id else None
    return render_template('index.html', aulas=aulas, categorias=categorias,
                           search=search, categoria_selecionada=categoria_selecionada)

@app.route('/aula/<int:id>')
def aula(id):
    aula = VideoAula.query.get_or_404(id)
    aula.visualizacoes += 1
    db.session.commit()
    aulas_relacionadas = VideoAula.query.filter(
        VideoAula.categoria_id == aula.categoria_id,
        VideoAula.id != aula.id
    ).limit(4).all()
    return render_template('aula.html', aula=aula, aulas_relacionadas=aulas_relacionadas)

@app.route('/categoria/<int:id>')
def categoria(id):
    cat = Categoria.query.get_or_404(id)
    aulas = VideoAula.query.filter_by(categoria_id=id).order_by(VideoAula.criado_em.desc()).all()
    categorias = Categoria.query.all()
    return render_template('categoria.html', categoria=cat, aulas=aulas, categorias=categorias)

@app.route('/sobre')
def sobre():
    total_aulas = VideoAula.query.count()
    total_views = db.session.query(db.func.sum(VideoAula.visualizacoes)).scalar() or 0
    total_cats = Categoria.query.count()
    return render_template('sobre.html', total_aulas=total_aulas,
                           total_views=total_views, total_cats=total_cats)

@app.route('/contato')
def contato():
    return render_template('contato.html')

# ──────────────────────────────────────────────
# ÁREA ADMINISTRATIVA
# ──────────────────────────────────────────────

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.senha.data):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin_dashboard'))
        flash('Email ou senha incorretos.', 'danger')
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    total_aulas = VideoAula.query.count()
    total_views = db.session.query(db.func.sum(VideoAula.visualizacoes)).scalar() or 0
    total_cats = Categoria.query.count()
    aulas_recentes = VideoAula.query.order_by(VideoAula.criado_em.desc()).limit(5).all()
    return render_template('admin/dashboard.html', total_aulas=total_aulas,
                           total_views=total_views, total_cats=total_cats,
                           aulas_recentes=aulas_recentes)

@app.route('/admin/aulas')
@login_required
def admin_aulas():
    aulas = VideoAula.query.order_by(VideoAula.criado_em.desc()).all()
    return render_template('admin/aulas.html', aulas=aulas)

@app.route('/admin/aulas/nova', methods=['GET', 'POST'])
@login_required
def admin_nova_aula():
    form = VideoAulaForm()
    form.categoria_id.choices = [(c.id, c.nome) for c in Categoria.query.all()]
    if form.validate_on_submit():
        aula = VideoAula(
            titulo=form.titulo.data,
            descricao=form.descricao.data,
            categoria_id=form.categoria_id.data,
            youtube_url=form.youtube_url.data.strip()
        )
        db.session.add(aula)
        db.session.commit()
        flash('Aula cadastrada com sucesso!', 'success')
        return redirect(url_for('admin_aulas'))
    return render_template('admin/form_aula.html', form=form, titulo='Nova Aula')

@app.route('/admin/aulas/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def admin_editar_aula(id):
    aula = VideoAula.query.get_or_404(id)
    form = VideoAulaForm(obj=aula)
    form.categoria_id.choices = [(c.id, c.nome) for c in Categoria.query.all()]
    if form.validate_on_submit():
        aula.titulo = form.titulo.data
        aula.descricao = form.descricao.data
        aula.categoria_id = form.categoria_id.data
        aula.youtube_url = form.youtube_url.data.strip()
        db.session.commit()
        flash('Aula atualizada com sucesso!', 'success')
        return redirect(url_for('admin_aulas'))
    return render_template('admin/form_aula.html', form=form, titulo='Editar Aula', aula=aula)

@app.route('/admin/aulas/<int:id>/excluir', methods=['POST'])
@login_required
def admin_excluir_aula(id):
    aula = VideoAula.query.get_or_404(id)
    db.session.delete(aula)
    db.session.commit()
    flash('Aula excluída com sucesso!', 'success')
    return redirect(url_for('admin_aulas'))

@app.route('/admin/categorias')
@login_required
def admin_categorias():
    categorias = Categoria.query.all()
    return render_template('admin/categorias.html', categorias=categorias)

@app.route('/admin/categorias/nova', methods=['GET', 'POST'])
@login_required
def admin_nova_categoria():
    form = CategoriaForm()
    if form.validate_on_submit():
        cat = Categoria(nome=form.nome.data, descricao=form.descricao.data, icone=form.icone.data)
        db.session.add(cat)
        db.session.commit()
        flash('Categoria criada com sucesso!', 'success')
        return redirect(url_for('admin_categorias'))
    return render_template('admin/form_categoria.html', form=form, titulo='Nova Categoria')

# ──────────────────────────────────────────────
# INICIALIZAÇÃO
# ──────────────────────────────────────────────

def init_db():
    with app.app_context():
        db.create_all()
        if not Usuario.query.filter_by(email='admin@aprendatecnologia.com').first():
            admin = Usuario(nome='Administrador', email='admin@aprendatecnologia.com')
            admin.set_password('admin123')
            db.session.add(admin)
        categorias_padrao = [
            ('Montagem de Computadores', 'Aprenda a montar e desmontar computadores do zero', 'bi-cpu'),
            ('Windows', 'Instalação e configuração do sistema operacional Windows', 'bi-windows'),
            ('Segurança Digital', 'Proteja seus dados e privacidade online', 'bi-shield-lock'),
            ('Como Evitar Golpes', 'Reconheça e evite golpes na internet e redes sociais', 'bi-exclamation-triangle'),
            ('Informática para Idosos', 'Aprenda tecnologia no seu ritmo com paciência e carinho', 'bi-heart'),
        ]
        for nome, desc, icone in categorias_padrao:
            if not Categoria.query.filter_by(nome=nome).first():
                db.session.add(Categoria(nome=nome, descricao=desc, icone=icone))
        db.session.commit()
        print("✅ Banco de dados inicializado!")
        print("👤 Admin: admin@aprendatecnologia.com / senha: admin123")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
