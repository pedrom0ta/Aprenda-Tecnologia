# 🖥️ Aprenda Tecnologia

Plataforma gratuita de videoaulas de informática e inclusão digital.

## 🚀 Como rodar o projeto

### 1. Instale as dependências
```bash
pip install -r requirements.txt
```

### 2. Inicie o servidor
```bash
python app.py
```

O banco de dados SQLite será criado automaticamente na primeira execução,  
junto com as 5 categorias padrão e o usuário administrador.

### 3. Acesse no navegador
- **Site público:** http://localhost:5000
- **Painel admin:** http://localhost:5000/admin/login

## 🔑 Credenciais do Admin
| Campo  | Valor                            |
|--------|----------------------------------|
| E-mail | admin@aprendatecnologia.com      |
| Senha  | admin123                         |

> ⚠️ **Importante:** Troque a senha após o primeiro acesso!

## 📁 Estrutura do Projeto

```
aprenda_tecnologia/
│
├── app.py              # Aplicação Flask principal (rotas)
├── models.py           # Modelos do banco de dados (SQLAlchemy)
├── forms.py            # Formulários (Flask-WTF)
├── requirements.txt    # Dependências Python
│
├── templates/
│   ├── base.html           # Template base público
│   ├── index.html          # Página inicial
│   ├── aula.html           # Player de vídeo
│   ├── categoria.html      # Aulas por categoria
│   ├── sobre.html          # Sobre o projeto
│   ├── contato.html        # Página de contato
│   └── admin/
│       ├── base_admin.html     # Template base admin
│       ├── login.html          # Login
│       ├── dashboard.html      # Dashboard
│       ├── aulas.html          # Lista de aulas
│       ├── form_aula.html      # Cadastro/edição de aula
│       ├── categorias.html     # Lista de categorias
│       └── form_categoria.html # Cadastro de categoria
│
├── static/
│   ├── css/
│   │   ├── style.css   # Estilos públicos
│   │   └── admin.css   # Estilos do painel admin
│   └── js/
│       └── main.js     # JavaScript principal
│
└── uploads/            # Vídeos enviados (MP4)
```

## 📋 Funcionalidades

### Site Público
- ✅ Página inicial com hero animado
- ✅ Grid de videoaulas com cards
- ✅ Pesquisa por título
- ✅ Filtro por categoria (pills)
- ✅ Player HTML5 para cada aula
- ✅ Contador de visualizações
- ✅ Página Sobre com estatísticas
- ✅ Página de Contato
- ✅ Menu de navegação responsivo
- ✅ Design moderno com Bootstrap 5

### Painel Administrativo
- ✅ Login protegido (Flask-Login)
- ✅ Dashboard com métricas
- ✅ CRUD completo de videoaulas
- ✅ Upload de vídeos MP4 (até 500MB)
- ✅ Gerenciamento de categorias
- ✅ Sidebar responsiva

## 🛡️ Segurança
- Autenticação com Flask-Login
- Senhas com hash (Werkzeug)
- Upload restrito a MP4
- CSRF protection (Flask-WTF)
- Nomes de arquivo sanitizados (secure_filename)
