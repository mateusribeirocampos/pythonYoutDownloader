# Gerenciamento de Pacotes Python: pip vs uv (Local vs Global)

Guia completo sobre gerenciamento de pacotes Python, diferenças entre instalação local e global, e como usar pip e uv eficientemente.

## 1. Conceitos Fundamentais

### Instalação Global vs Local

**Global (Sistema):**

- Pacotes instalados para todos os projetos
- Localizado em: `/Users/usuario/.pyenv/versions/3.12.6/lib/python3.12/site-packages/`
- Problemas: conflitos de versão, dependências conflitantes

**Local (Ambiente Virtual):**

- Pacotes isolados por projeto
- Localizado em: `venv/lib/python3.12/site-packages/`
- Vantagens: isolamento, versões específicas, sem conflitos

## 2. pip - Gerenciador Tradicional

### Comandos Básicos

```bash
# Verificar versão
pip --version

# Instalar pacote
pip install nome-do-pacote

# Instalar versão específica
pip install nome-do-pacote==1.2.3

# Instalar com restrição de versão
pip install 'nome-do-pacote>=1.0,<2.0'

# Listar pacotes instalados
pip list

# Mostrar informações de um pacote
pip show nome-do-pacote

# Atualizar pacote
pip install --upgrade nome-do-pacote

# Desinstalar pacote
pip uninstall nome-do-pacote
```

### Gerenciamento de Dependências

```bash
# Criar arquivo de dependências
pip freeze > requirements.txt

# Instalar de arquivo de dependências
pip install -r requirements.txt

# Instalar em modo desenvolvimento (editável)
pip install -e .
```

### Exemplo requirements.txt

```txt
# Dependências principais
yt-dlp==2025.7.21
requests>=2.31.0,<3.0.0
pydantic>=2.0.0

# Dependências de desenvolvimento
pytest>=7.0.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
```

## 3. uv - Gerenciador Moderno (Rápido)

### Instalação do uv

```bash
# Instalar uv
pip install uv

# Ou via curl (Linux/macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Comandos Básicos do uv

```bash
# Instalar pacote
uv pip install nome-do-pacote

# Instalar de requirements.txt
uv pip install -r requirements.txt

# Listar pacotes
uv pip list

# Desinstalar pacote
uv pip uninstall nome-do-pacote

# Criar ambiente virtual
uv venv

# Ativar ambiente (mesmo comando que python -m venv)
source .venv/bin/activate  # Linux/macOS
```

### Vantagens do uv

- **Velocidade**: 10-100x mais rápido que pip
- **Compatibilidade**: API compatível com pip
- **Cache inteligente**: reutiliza downloads
- **Resolução melhor**: resolve dependências mais eficientemente

## 4. Comparação pip vs uv

| Aspecto | pip | uv |
|---------|-----|----|
| Velocidade | Padrão | 10-100x mais rápido |
| Compatibilidade | Nativo Python | Compatible com pip |
| Cache | Básico | Avançado |
| Resolução de deps | Lenta | Rápida e inteligente |
| Tamanho binário | Incluso no Python | ~15MB |
| Maturidade | Estável | Em desenvolvimento |

## 5. Estratégias de Uso

### Desenvolvimento Local

```bash
# Criar projeto novo
mkdir meu-projeto
cd meu-projeto

# Configurar Python
pyenv local 3.12.6

# Criar ambiente virtual
python -m venv venv
# OU usando uv (mais rápido)
uv venv

# Ativar ambiente
source venv/bin/activate

# Instalar dependências
uv pip install -r requirements.txt
# OU pip install -r requirements.txt
```

### Workflow Recomendado

```bash
# 1. Sempre usar ambiente virtual
python -m venv venv && source venv/bin/activate

# 2. Atualizar pip/uv
pip install --upgrade pip uv

# 3. Instalar dependências com uv (mais rápido)
uv pip install nome-do-pacote

# 4. Salvar dependências
pip freeze > requirements.txt

# 5. Para desenvolvimento, separar dependências
echo "pytest>=7.0.0" >> requirements-dev.txt
```

## 6. Gerenciamento de Versões

### Especificação de Versões

```txt
# requirements.txt - Exemplos de especificação

# Versão exata
yt-dlp==2025.7.21

# Versão mínima
requests>=2.31.0

# Versão com limite superior
numpy>=1.20.0,<2.0.0

# Versão compatível (semver)
fastapi~=0.100.0  # Equivale a >=0.100.0,<0.101.0

# Versão de desenvolvimento
git+https://github.com/user/repo.git@branch

# Pacote local editável
-e .
```

### Atualização de Dependências

```bash
# Ver pacotes desatualizados
pip list --outdated

# Atualizar específico
pip install --upgrade nome-do-pacote

# Atualizar todos (cuidado!)
pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U
```

## 7. Ambientes para Diferentes Casos de Uso

### Desenvolvimento

```bash
# requirements-dev.txt
-r requirements.txt
pytest>=7.0.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
pre-commit>=3.0.0
```

### Produção

```bash
# requirements-prod.txt (versões fixas)
yt-dlp==2025.7.21
requests==2.31.0
pydantic==2.5.3
```

### Testes

```bash
# requirements-test.txt
-r requirements.txt
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0
```

## 8. Ferramentas Complementares

### pip-tools (Gerenciamento Avançado)

```bash
# Instalar pip-tools
pip install pip-tools

# Criar requirements.in
echo "yt-dlp" > requirements.in
echo "requests>=2.31.0" >> requirements.in

# Gerar requirements.txt com versões fixas
pip-compile requirements.in

# Atualizar dependências
pip-compile --upgrade requirements.in
```

### pyproject.toml (Moderno)

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "youtube-downloader"
version = "1.0.0"
dependencies = [
    "yt-dlp>=2025.7.21",
    "requests>=2.31.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
]
```

## 9. Scripts de Automação

### Script de Setup Rápido

```bash
#!/bin/bash
# setup.sh

echo "Configurando ambiente Python..."

# Verificar se pyenv existe
if ! command -v pyenv &> /dev/null; then
    echo "pyenv não encontrado. Instale primeiro."
    exit 1
fi

# Configurar Python local
pyenv local 3.12.6

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente
source venv/bin/activate

# Atualizar pip e instalar uv
pip install --upgrade pip uv

# Instalar dependências
if [ -f "requirements.txt" ]; then
    uv pip install -r requirements.txt
    echo "Dependências instaladas com sucesso!"
else
    echo "Arquivo requirements.txt não encontrado."
fi

echo "Ambiente configurado! Use 'source venv/bin/activate' para ativar."
```

## 10. Boas Práticas

### Checklist de Projeto

- [ ] Usar sempre ambiente virtual
- [ ] Fixar versão Python com pyenv local
- [ ] Especificar versões em requirements.txt
- [ ] Separar dependências (dev, prod, test)
- [ ] Usar uv para velocidade (quando disponível)
- [ ] Manter requirements.txt atualizado
- [ ] Não commitar pasta venv/
- [ ] Documentar setup no README.md

### Comandos de Verificação

```bash
# Verificar ambiente atual
echo "Python: $(python --version)"
echo "Pip: $(pip --version)"
echo "Ambiente: $VIRTUAL_ENV"
echo "Pacotes: $(pip list | wc -l)"

# Verificar consistência
pip check

# Auditoria de segurança
pip-audit  # Instalar com: pip install pip-audit
```

Este guia fornece uma base sólida para gerenciar pacotes Python de forma eficiente e segura.
