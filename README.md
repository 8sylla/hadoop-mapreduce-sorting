# MapReduce Sorting with Hadoop Cluster 🚀

[![Hadoop](https://img.shields.io/badge/Hadoop-3.3.6-orange.svg)](https://hadoop.apache.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Description

Implémentation d'un algorithme de **tri distribué** utilisant le paradigme **MapReduce** sur un cluster Hadoop de 3 nœuds. Ce projet démontre la puissance du traitement distribué pour trier 100 valeurs numériques en exploitant le framework Apache Hadoop.

### 🎯 Objectifs

- ✅ Déployer un cluster Hadoop multi-nœuds avec Docker
- ✅ Implémenter un tri MapReduce en Python
- ✅ Comprendre les phases Map, Shuffle & Sort, Reduce
- ✅ Monitorer les jobs via les interfaces Web Hadoop
- ✅ Valider le tri distribué

## Architecture

```
┌─────────────────────────────────────────────────────┐
│              Hadoop Cluster (Docker)                 │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐    ┌──────────────┐              │
│  │   Master     │    │   Worker 1   │              │
│  │ (NameNode)   │◄──►│ (DataNode)   │              │
│  │ (JobTracker) │    │ (TaskTracker)│              │
│  └──────────────┘    └──────────────┘              │
│         ▲                    ▲                       │
│         │                    │                       │
│         └────────┬───────────┘                       │
│                  │                                   │
│         ┌──────────────┐                            │
│         │   Worker 2   │                            │
│         │ (DataNode)   │                            │
│         │ (TaskTracker)│                            │
│         └──────────────┘                            │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Flux MapReduce

```
Input (100 nombres non triés)
        ↓
   [Map Phase]
   - Émet (nombre, nombre)
        ↓
[Shuffle & Sort]
   - Hadoop trie automatiquement
        ↓
  [Reduce Phase]
  - Émet les nombres triés
        ↓
Output (100 nombres triés)
```

## Démarrage Rapide

### Prérequis

### Installation en 3 étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/8sylla/hadoop-mapreduce-sorting.git
cd hadoop-mapreduce-sorting

# 2. Démarrer le cluster Hadoop
docker-compose up -d

# 3. Exécuter le tri MapReduce
./scripts/run-sorting.sh
```

**C'est tout !** Les résultats seront dans `data/output/`

## 📖 Guide Détaillé

### Étape 1 : Démarrer le cluster

```bash
# Construire l'image (si nécessaire)
docker-compose build

# Démarrer les 3 conteneurs
docker-compose up -d

# Vérifier que tout fonctionne
docker-compose ps
```

Vous devriez voir :
```
NAME              STATUS
hadoop-master     Up
hadoop-worker1    Up
hadoop-worker2    Up
```

### Étape 2 : Initialiser Hadoop

```bash
# Entrer dans le conteneur master
docker exec -it hadoop-master bash

# Lancer Hadoop et YARN
./start-hadoop.sh

# Vérifier HDFS
hdfs dfs -ls /
```

### Étape 3 : Générer les données

```bash
# Sur votre machine hôte
python src/python/generate_data.py

# Copier dans le conteneur
docker cp data/input/numbers.txt hadoop-master:/root/numbers.txt
```

### Étape 4 : Exécuter le Job MapReduce

```bash
# Dans le conteneur master
docker exec -it hadoop-master bash

# Créer les répertoires HDFS
hdfs dfs -mkdir -p /user/root/input
hdfs dfs -mkdir -p /user/root/output

# Charger les données
hdfs dfs -put numbers.txt /user/root/input/

# Lancer le job MapReduce
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
  -input /user/root/input/numbers.txt \
  -output /user/root/output \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -file mapper.py \
  -file reducer.py
```

### Étape 5 : Récupérer les résultats

```bash
# Afficher le résultat dans HDFS
hdfs dfs -cat /user/root/output/part-00000

# Copier sur votre machine
hdfs dfs -get /user/root/output/part-00000 /root/sorted_result.txt
docker cp hadoop-master:/root/sorted_result.txt data/output/
```

## 🖥️ Interfaces Web

Une fois le cluster démarré, accédez aux interfaces :

| Interface | URL | Description |
|-----------|-----|-------------|
| **HDFS NameNode** | http://localhost:9870 | Gestion du système de fichiers |
| **YARN ResourceManager** | http://localhost:8088 | Suivi des jobs MapReduce |
| **Worker 1** | http://localhost:8040 | Statut du worker 1 |
| **Worker 2** | http://localhost:8041 | Statut du worker 2 |

## 📊 Résultats Attendus

### Input (data/input/numbers.txt)
```
847
123
956
42
...
```

### Output (data/output/part-00000)
```
1
7
12
42
...
998
```

### Métriques

- **Temps d'exécution** : ~30-60 secondes
- **Nombre de mappers** : 1-2 (selon split)
- **Nombre de reducers** : 1
- **Taille des données** : ~300 bytes

## 🧪 Tests

### Test local (sans Hadoop)

```bash
# Pipeline complet en local
cat data/input/numbers.txt | \
  python src/python/mapper.py | \
  sort -n -k1 | \
  python src/python/reducer.py > data/output/local_result.txt

# Valider le tri
python src/python/validate_sort.py data/output/local_result.txt
```

### Tests unitaires

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer les tests
python -m pytest tests/ -v
```

## 🔧 Configuration

### Modifier le nombre de valeurs

Éditez `src/python/generate_data.py` :

```python
# Générer 1000 valeurs au lieu de 100
generate_random_numbers(count=1000, min_val=1, max_val=10000)
```

### Ajouter des reducers

Dans le job Hadoop :

```bash
-D mapreduce.job.reduces=3  # 3 reducers au lieu de 1
```

### Erreur "Connection refused" sur HDFS

```bash
# Vérifier que Hadoop est démarré
docker exec hadoop-master jps

# Vous devez voir : NameNode, SecondaryNameNode, ResourceManager
```

### Job MapReduce échoue

```bash
# Vérifier les logs YARN
http://localhost:8088

# Nettoyer les anciens outputs
hdfs dfs -rm -r /user/root/output
```

## 🙏 Remerciements

- [Apache Hadoop](https://hadoop.apache.org/) pour le framework
- [liliasfaxi/hadoop-cluster](https://github.com/liliasfaxi/hadoop-cluster-docker) pour l'image Docker de base
- La communauté Big Data pour les ressources

---
