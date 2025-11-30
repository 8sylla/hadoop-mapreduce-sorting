#!/bin/bash
# Script de configuration initiale du projet MapReduce Sorting
# À exécuter UNE SEULE FOIS après le clonage du projet

set -e  # Arrêter en cas d'erreur

echo "═══════════════════════════════════════════════════════════"
echo "  Configuration du Projet MapReduce Sorting"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Couleurs pour le terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Vérifier Docker
echo "1️⃣  Vérification de Docker..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker n'est pas installé${NC}"
    echo "   Installez Docker depuis: https://www.docker.com/get-started"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose n'est pas installé${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker et Docker Compose sont installés${NC}"
echo ""

# Vérifier Python
echo "2️⃣  Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python 3 n'est pas installé (optionnel pour tests locaux)${NC}"
else
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ $PYTHON_VERSION${NC}"
fi
echo ""

# Créer la structure de répertoires
echo "3️⃣  Création de la structure de répertoires..."
mkdir -p data/input
mkdir -p data/output
mkdir -p docs/screenshots
mkdir -p tests
mkdir -p src/python
mkdir -p notebooks
echo -e "${GREEN}✓ Structure créée${NC}"
echo ""

# Générer les données de test
echo "4️⃣  Génération des données de test (100 nombres)..."
if command -v python3 &> /dev/null; then
    python3 src/python/generate_data.py
    echo -e "${GREEN}✓ Données générées: data/input/numbers.txt${NC}"
else
    echo -e "${YELLOW}⚠️  Ignoré (Python non disponible)${NC}"
fi
echo ""

# Copier les données dans config/ pour Docker
echo "5️⃣  Préparation des fichiers pour Docker..."
if [ -f "data/input/numbers.txt" ]; then
    cp data/input/numbers.txt config/numbers.txt
    echo -e "${GREEN}✓ Fichier copié vers config/numbers.txt${NC}"
else
    echo -e "${YELLOW}⚠️  data/input/numbers.txt non trouvé${NC}"
fi
echo ""

# Rendre les scripts exécutables
echo "6️⃣  Configuration des permissions..."
chmod +x scripts/*.sh
chmod +x src/python/*.py
echo -e "${GREEN}✓ Scripts rendus exécutables${NC}"
echo ""

# Pull de l'image Docker
echo "7️⃣  Téléchargement de l'image Hadoop..."
echo "   (Cela peut prendre quelques minutes...)"
docker pull liliasfaxi/hadoop-cluster:latest
echo -e "${GREEN}✓ Image téléchargée${NC}"
echo ""

# Créer le fichier .env
echo "8️⃣  Création du fichier de configuration..."
cat > .env << EOF
# Configuration du cluster Hadoop
CLUSTER_NAME=hadoop-sorting-cluster
HADOOP_VERSION=3.3.6

# Configuration MapReduce
INPUT_FILE=numbers.txt
OUTPUT_DIR=output
EOF
echo -e "${GREEN}✓ Fichier .env créé${NC}"
echo ""

# Créer le .gitignore
echo "9️⃣  Création du .gitignore..."
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Data
data/output/*
!data/output/.gitkeep
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Jupyter
.ipynb_checkpoints/

# Docker
docker-compose.override.yml
EOF
echo -e "${GREEN}✓ .gitignore créé${NC}"
echo ""

# Créer .gitkeep pour data/output
touch data/output/.gitkeep

# Résumé
echo "═══════════════════════════════════════════════════════════"
echo -e "${GREEN}  ✅ Configuration terminée avec succès !${NC}"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📋 Prochaines étapes:"
echo ""
echo "1. Démarrer le cluster Hadoop:"
echo "   docker-compose up -d"
echo ""
echo "2. Initialiser Hadoop (attendre 30 secondes):"
echo "   docker exec -it hadoop-master ./start-hadoop.sh"
echo ""
echo "3. Lancer le tri MapReduce:"
echo "   ./scripts/run-sorting.sh"
echo ""
echo "4. Accéder aux interfaces Web:"
echo "   - HDFS:  http://localhost:9870"
echo "   - YARN:  http://localhost:8088"
echo ""
echo "═══════════════════════════════════════════════════════════"