#!/bin/bash
# Script d'exécution du tri MapReduce sur le cluster Hadoop
# Usage: ./scripts/run-sorting.sh

set -e

echo "═══════════════════════════════════════════════════════════"
echo "  MapReduce Sorting - Exécution sur Cluster Hadoop"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
MASTER_CONTAINER="hadoop-master"
INPUT_FILE="numbers.txt"
HDFS_INPUT_DIR="/user/root/input"
HDFS_OUTPUT_DIR="/user/root/output"
MAPPER_FILE="mapper.py"
REDUCER_FILE="reducer.py"

# Vérifier que le conteneur master tourne
echo "1️⃣  Vérification du cluster..."
if ! docker ps | grep -q $MASTER_CONTAINER; then
    echo -e "${RED}❌ Le conteneur $MASTER_CONTAINER n'est pas démarré${NC}"
    echo "   Lancez d'abord: docker-compose up -d"
    exit 1
fi
echo -e "${GREEN}✓ Cluster Hadoop actif${NC}"
echo ""

# Vérifier que Hadoop est démarré
echo "2️⃣  Vérification de Hadoop..."
NAMENODE_STATUS=$(docker exec $MASTER_CONTAINER jps | grep -c "NameNode" || echo "0")
if [ "$NAMENODE_STATUS" -eq "0" ]; then
    echo -e "${YELLOW}⚠️  Hadoop n'est pas démarré. Démarrage...${NC}"
    docker exec $MASTER_CONTAINER ./start-hadoop.sh
    echo "   Attente de 30 secondes pour l'initialisation..."
    sleep 30
fi
echo -e "${GREEN}✓ Hadoop opérationnel${NC}"
echo ""

# Copier les fichiers Python dans le conteneur
echo "3️⃣  Copie des scripts MapReduce..."
docker cp src/python/$MAPPER_FILE $MASTER_CONTAINER:/root/$MAPPER_FILE
docker cp src/python/$REDUCER_FILE $MASTER_CONTAINER:/root/$REDUCER_FILE
echo -e "${GREEN}✓ Scripts copiés${NC}"
echo ""

# Vérifier que le fichier de données existe
echo "4️⃣  Vérification des données..."
if [ ! -f "data/input/$INPUT_FILE" ]; then
    echo -e "${RED}❌ Fichier data/input/$INPUT_FILE introuvable${NC}"
    echo "   Générez les données avec: python src/python/generate_data.py"
    exit 1
fi

# Copier le fichier de données
docker cp data/input/$INPUT_FILE $MASTER_CONTAINER:/root/$INPUT_FILE
echo -e "${GREEN}✓ Données copiées ($(wc -l < data/input/$INPUT_FILE) nombres)${NC}"
echo ""

# Nettoyer les anciens répertoires HDFS
echo "5️⃣  Préparation de HDFS..."
docker exec $MASTER_CONTAINER bash -c "hdfs dfs -rm -r $HDFS_INPUT_DIR $HDFS_OUTPUT_DIR 2>/dev/null || true"
docker exec $MASTER_CONTAINER hdfs dfs -mkdir -p $HDFS_INPUT_DIR
echo -e "${GREEN}✓ Répertoires HDFS créés${NC}"
echo ""

# Charger les données dans HDFS
echo "6️⃣  Chargement des données dans HDFS..."
docker exec $MASTER_CONTAINER hdfs dfs -put $INPUT_FILE $HDFS_INPUT_DIR/
echo -e "${GREEN}✓ Données chargées dans $HDFS_INPUT_DIR/$INPUT_FILE${NC}"
echo ""

# Lancer le job MapReduce
echo "7️⃣  Lancement du Job MapReduce..."
echo -e "${BLUE}   (Cela peut prendre 30-60 secondes...)${NC}"
echo ""

START_TIME=$(date +%s)

docker exec $MASTER_CONTAINER bash -c "
hadoop jar \$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
  -input $HDFS_INPUT_DIR/$INPUT_FILE \
  -output $HDFS_OUTPUT_DIR \
  -mapper 'python3 $MAPPER_FILE' \
  -reducer 'python3 $REDUCER_FILE' \
  -file /root/$MAPPER_FILE \
  -file /root/$REDUCER_FILE
"

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo -e "${GREEN}✓ Job MapReduce terminé en ${DURATION}s${NC}"
echo ""

# Afficher les résultats
echo "8️⃣  Récupération des résultats..."

# Créer le répertoire de sortie s'il n'existe pas
mkdir -p data/output

# Récupérer le fichier de résultat
docker exec $MASTER_CONTAINER hdfs dfs -cat $HDFS_OUTPUT_DIR/part-00000 > data/output/sorted_numbers.txt

echo -e "${GREEN}✓ Résultats sauvegardés: data/output/sorted_numbers.txt${NC}"
echo ""

# Afficher un aperçu
echo "📊 Aperçu des résultats:"
echo ""
echo "   Premiers nombres:"
head -5 data/output/sorted_numbers.txt | sed 's/^/     /'
echo "     ..."
echo "   Derniers nombres:"
tail -5 data/output/sorted_numbers.txt | sed 's/^/     /'
echo ""

# Validation
echo "9️⃣  Validation du tri..."
if command -v python3 &> /dev/null; then
    python3 src/python/validate_sort.py data/input/$INPUT_FILE data/output/sorted_numbers.txt
else
    echo -e "${YELLOW}⚠️  Python non disponible, validation ignorée${NC}"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo -e "${GREEN}  ✅ Tri MapReduce terminé avec succès !${NC}"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📂 Fichiers générés:"
echo "   - data/output/sorted_numbers.txt"
echo ""
echo "🌐 Interfaces Web disponibles:"
echo "   - HDFS NameNode:        http://localhost:9870"
echo "   - YARN ResourceManager: http://localhost:8088"
echo "   - Worker 1:             http://localhost:8040"
echo "   - Worker 2:             http://localhost:8041"
echo ""
echo "📊 Statistiques HDFS:"
docker exec $MASTER_CONTAINER hdfs dfs -du -h $HDFS_OUTPUT_DIR
echo ""
echo "═══════════════════════════════════════════════════════════"