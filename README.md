# Environnement de Traitement de Données avec Hadoop et Spark

Ce projet configure un environnement complet Hadoop et Spark en utilisant Docker. Il inclut HDFS, Spark, Hive, PostgreSQL et MariaDB, permettant le stockage distribué et le traitement de données.

## Prérequis

- Docker
- Docker Compose

## Instructions de Mise en Place

1. Clonez le dépôt :

   ```bash
   git clone <url-du-repo>
   cd <répertoire-du-projet>
   ```

2. Lancez les services avec Docker Compose :

   ```bash
   docker-compose up -d
   ```

3. Initialisez le système de fichiers HDFS dans le container `namenode` :

   Accédez au container :

   ```bash
   docker exec -it namenode bash
   ```

   Exécutez les commandes suivantes dans le container :

   ```bash
   hdfs dfs -mkdir -p /nyc_subway_data
   hdfs dfs -put /data/* /nyc_subway_data
   ```

4. Soumettez les jobs Spark dans le container `spark-master` :

   Accédez au container :

   ```bash
   docker exec -it spark-master bash
   ```

   Exécutez les commandes suivantes pour soumettre les jobs Spark :

   ```bash
   spark-submit --master spark://spark-master:7077 /app/transform_stations.py
   spark-submit --master spark://spark-master:7077 /app/transform_turnstiles.py
   spark-submit --master spark://spark-master:7077 --jars /opt/spark/postgresql-42.7.5.jar /app/turnstiles_fill_datamart.py
   spark-submit --master spark://spark-master:7077 --jars /opt/spark/postgresql-42.7.5.jar /app/stations_fill_datamart.py
   ```

## Configuration des Ports Exposés

| Service                | Port Local | Port Container | Description                   |
| ---------------------- | ---------- | -------------- | ----------------------------- |
| HDFS Web UI (Namenode) | 50070      | 50070          | Interface Web de HDFS         |
| HDFS RPC (Namenode)    | 9000       | 9000           | RPC du Namenode               |
| HDFS Web UI (Datanode) | 50075      | 50075          | Interface Web du Datanode     |
| Resource Manager UI    | 8088       | 8088           | Interface du Resource Manager |
| History Server UI      | 8188       | 8188           | Interface du History Server   |
| Spark Master UI        | 8080       | 8080           | Interface du Spark Master     |
| Spark Worker UI        | 8081       | 8081           | Interface du Spark Worker     |
| Hive Metastore Thrift  | 9083       | 9083           | Interface Thrift du Metastore |
| PostgreSQL             | 5433       | 5432           | Base de données PostgreSQL    |
| MariaDB                | 3306       | 3306           | Base de données MariaDB       |

## Structure des Répertoires

- `data/` : Contient les données brutes à charger dans HDFS.
- `spark/` : Contient les scripts Spark.
- `bin/spark/` : Contient les dépendances Spark comme les fichiers `.jar`.

## Notes Importantes

- Assurez-vous que les fichiers de configuration et les volumes de données sont correctement configurés avant de démarrer.
- Vérifiez les logs des containers en cas de problème avec la commande :

  ```bash
  docker logs <nom-du-container>
  ```

- Pour arrêter les services, exécutez :

  ```bash
  docker-compose down
  ```
