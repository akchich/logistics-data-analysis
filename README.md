# Logistics Data Analysis & Delay Prediction

Projet d’analyse de données logistiques basé sur le dataset public **Brazilian E-Commerce Public Dataset by Olist**.

L’objectif est d’analyser les retards de livraison, d’identifier certains facteurs associés à ces retards et de comparer deux modèles de Machine Learning pour essayer de détecter les commandes à risque.

Le projet couvre plusieurs étapes d’un workflow Data :

* préparation et nettoyage des données ;
* jointure de plusieurs sources ;
* création de KPI ;
* analyse géographique et temporelle ;
* feature engineering ;
* visualisation ;
* préparation d’un dataset final ;
* classification avec Scikit-learn ;
* comparaison de modèles.

## Objectif métier

L’objectif principal est de répondre à la question :

**Quels facteurs semblent influencer les retards de livraison, et peut-on détecter les commandes à risque à partir des informations disponibles ?**

Une commande est considérée comme en retard lorsque :

```text
date de livraison réelle > date de livraison estimée
```

## Dataset

Le projet utilise trois fichiers issus du dataset Olist :

```text
olist_orders_dataset.csv
olist_customers_dataset.csv
olist_order_items_dataset.csv
```

### Orders

Le fichier des commandes contient notamment :

* identifiant de commande ;
* identifiant client ;
* statut ;
* date d’achat ;
* date d’approbation ;
* date de remise au transporteur ;
* date réelle de livraison ;
* date estimée de livraison.

### Customers

Le fichier clients permet d’ajouter des informations géographiques :

* ville ;
* État ;
* code postal.

### Order items

Le fichier des articles contient notamment :

* identifiant de commande ;
* produit ;
* vendeur ;
* prix ;
* frais de livraison.

Une commande pouvant contenir plusieurs articles, les données ont d’abord été agrégées par `order_id` avant la jointure avec les autres tables.

## Pipeline de préparation des données

Le workflow principal du projet est :

```text
Données commandes
       +
Données clients
       +
Données articles
       ↓
Nettoyage
       ↓
Agrégation des articles par commande
       ↓
Jointures avec Pandas
       ↓
Création de nouvelles variables
       ↓
Analyse et KPI
       ↓
Dataset final
       ↓
Machine Learning
```

## Nettoyage des données

Une première analyse des valeurs manquantes a montré notamment :

```text
order_approved_at                 160
order_delivered_carrier_date     1783
order_delivered_customer_date    2965
```

Les commandes sans date réelle de livraison ne permettent pas de déterminer correctement si elles sont en retard.

Pour le calcul des KPI liés aux retards, seules les commandes disposant d’une date de livraison réelle ont donc été conservées.

## KPI principaux

Le dataset initial contient :

```text
99 441 commandes
```

Après filtrage des commandes ayant une date réelle de livraison :

```text
96 476 commandes livrées
```

### Taux de retard

Parmi les commandes livrées :

```text
8,11 % sont arrivées après la date estimée
```

### Retard moyen

Pour les commandes réellement en retard :

```text
Retard moyen : 8,87 jours
```

## Analyse géographique

Les données clients ont été jointes aux commandes afin d’étudier le taux de retard selon l’État.

Quelques résultats observés :

| État | Nombre de commandes | Taux de retard |
| ---- | ------------------: | -------------: |
| AL   |                 397 |        23,93 % |
| MA   |                 717 |        19,67 % |
| PI   |                 476 |        15,97 % |
| CE   |               1 279 |        15,32 % |
| SE   |                 335 |        15,22 % |
| BA   |               3 256 |        14,04 % |
| RJ   |              12 353 |        13,47 % |

Ces résultats montrent qu’il est important de regarder à la fois le **taux de retard** et le **volume de commandes**.

Un État peut afficher un taux très élevé sur un faible volume, tandis qu’un État comme `RJ` combine un volume important et un taux de retard supérieur à la moyenne.

### Visualisation

![Taux de retard par État](images/taux_retard_etats.png)

La ligne horizontale représente le taux moyen global de retard.

## Analyse temporelle

Des variables temporelles ont été créées à partir de la date de commande :

```text
jour_semaine
mois
heure_commande
```

### Jour de la semaine

Taux de retard observé selon le jour de commande :

| Jour     | Taux de retard |
| -------- | -------------: |
| Lundi    |         9,06 % |
| Mardi    |         8,49 % |
| Mercredi |         7,80 % |
| Jeudi    |         7,57 % |
| Vendredi |         8,45 % |
| Samedi   |         7,60 % |
| Dimanche |         7,49 % |

Le lundi présente le taux de retard le plus élevé dans cette analyse, même si l’écart avec les autres jours reste modéré.

### Analyse mensuelle

Les retards varient davantage selon les mois :

| Mois      | Taux de retard |
| --------- | -------------: |
| Janvier   |         6,23 % |
| Février   |        13,42 % |
| Mars      |        17,15 % |
| Avril     |         5,96 % |
| Mai       |         6,64 % |
| Juin      |         2,21 % |
| Juillet   |         4,08 % |
| Août      |         7,58 % |
| Septembre |         5,23 % |
| Octobre   |         5,05 % |
| Novembre  |        14,31 % |
| Décembre  |         8,38 % |

Les mois de **mars** et **novembre** ressortent comme des périodes avec un taux de retard particulièrement élevé.

### Visualisation

![Taux de retard par mois](images/taux_retard_mois.png)

## Agrégation des données articles

Le fichier `olist_order_items_dataset.csv` contient :

```text
112 650 lignes
```

Une même commande pouvant contenir plusieurs articles, une agrégation par `order_id` a été réalisée.

Les variables suivantes ont été créées :

```text
total_price
total_freight
nombre_articles
```

Après agrégation :

```text
98 666 commandes uniques
```

Ces données ont ensuite été jointes aux commandes et aux informations client.

## Feature Engineering

Plusieurs variables ont été créées pour l’analyse et le Machine Learning :

```text
total_price
total_freight
nombre_articles
jour_semaine
mois
heure_commande
delai_prevu_jours
customer_state
```

### Délai prévu

La variable `delai_prevu_jours` représente le nombre de jours prévu entre la date de commande et la date estimée de livraison.

```text
date estimée de livraison - date de commande
```

Cette variable est connue avant la livraison réelle et peut donc être utilisée pour essayer de prédire un risque de retard.

## Problème de Machine Learning

Le problème est traité comme une classification binaire :

```text
False = commande livrée à temps
True  = commande en retard
```

La distribution des classes est très déséquilibrée :

```text
Pas de retard : 88 649
Retard        : 7 827
```

Les commandes en retard représentent seulement environ 8 % du dataset.

Pour cette raison, l’accuracy seule n’est pas une métrique suffisante pour comparer les modèles.

Les métriques particulièrement observées sont :

* precision ;
* recall ;
* F1-score.

Le **recall de la classe retard** est important dans ce contexte car il indique la proportion de vrais retards détectés.

## Prétraitement pour le Machine Learning

Les variables numériques sont standardisées avec :

```python
StandardScaler()
```

La variable catégorielle `customer_state` est transformée avec :

```python
OneHotEncoder(handle_unknown="ignore")
```

Le prétraitement et le modèle sont regroupés dans un pipeline Scikit-learn afin d’automatiser les transformations.

## Modèle 1 — Régression logistique

Une régression logistique avec pondération des classes a été utilisée comme premier modèle.

```python
LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)
```

### Résultats sur la classe retard

```text
Precision : 0,13
Recall    : 0,61
F1-score  : 0,22
```

La matrice de confusion obtenue est :

```text
[[11385  6346]
 [  603   962]]
```

Le modèle détecte environ **61 % des véritables retards**, mais génère également beaucoup de faux positifs.

L’ajout de la variable géographique `customer_state` a amélioré les performances par rapport à une première version du modèle qui utilisait uniquement les variables numériques.

## Modèle 2 — Random Forest

Un deuxième modèle a été testé :

```python
RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)
```

### Résultats sur la classe retard

```text
Precision : 0,46
Recall    : 0,04
F1-score  : 0,08
```

La matrice de confusion obtenue est :

```text
[[17652    79]
 [ 1498    67]]
```

Le Random Forest atteint une accuracy globale d’environ 92 %, mais détecte seulement environ **4 % des vrais retards**.

Cette comparaison montre pourquoi l’accuracy peut être trompeuse lorsque les classes sont fortement déséquilibrées.

## Comparaison des modèles

| Modèle                | Precision retard | Recall retard | F1 retard |
| --------------------- | ---------------: | ------------: | --------: |
| Régression logistique |             0,13 |      **0,61** |  **0,22** |
| Random Forest         |         **0,46** |          0,04 |      0,08 |

Pour l’objectif de détection des commandes à risque, la régression logistique est retenue comme modèle principal car elle détecte une proportion beaucoup plus importante des véritables retards.

Le Random Forest est conservé comme modèle de comparaison.

## Limites du modèle

Les résultats montrent que les variables disponibles ne suffisent pas encore à prédire précisément les retards.

Plusieurs informations pourraient améliorer le modèle :

* distance réelle entre vendeur et client ;
* caractéristiques du vendeur ;
* catégorie du produit ;
* transporteur ;
* volume logistique de la période ;
* informations météorologiques ;
* jours fériés ;
* données opérationnelles liées aux centres logistiques.

Le faible niveau de précision de la régression logistique montre notamment que le modèle génère encore beaucoup de fausses alertes.

Le projet constitue donc une première approche exploratoire et non un système de prédiction destiné à la production.

## Dataset final

Le dataset préparé est enregistré dans :

```text
data/dataset_final_logistics.csv
```

Il contient les données issues des différentes sources après nettoyage, agrégation, jointures et feature engineering.

## Structure du projet

```text
logistics-data-analysis/
│
├── data/
│   ├── dataset_final_logistics.csv
│   ├── olist_customers_dataset.csv
│   ├── olist_order_items_dataset.csv
│   └── olist_orders_dataset.csv
│
├── images/
│   ├── taux_retard_etats.png
│   └── taux_retard_mois.png
│
├── notebooks/
│   └── 01_exploration.py
│
├── src/
│
└── README.md
```

## Technologies utilisées

* Python
* Pandas
* NumPy
* Matplotlib
* Scikit-learn
* Machine Learning
* Data Cleaning
* Feature Engineering
* Data Visualization
* Data Pipeline

## Compétences mobilisées

Ce projet m’a permis de travailler sur :

* exploration d’un dataset réel ;
* identification des valeurs manquantes ;
* nettoyage des données ;
* agrégation avec Pandas ;
* jointures entre plusieurs tables ;
* création de KPI logistiques ;
* analyse géographique ;
* analyse temporelle ;
* visualisation de données ;
* création de nouvelles variables ;
* gestion d’une classification déséquilibrée ;
* encodage de variables catégorielles ;
* standardisation ;
* création de pipelines Scikit-learn ;
* entraînement et comparaison de modèles ;
* interprétation d’une matrice de confusion ;
* analyse de precision, recall et F1-score.

## Conclusion

L’analyse met en évidence plusieurs facteurs associés aux retards de livraison.

Le taux global de retard est d’environ **8,11 %**, avec un retard moyen de **8,87 jours** pour les commandes concernées.

Certaines zones géographiques présentent un taux de retard supérieur à la moyenne, et une saisonnalité importante apparaît également, notamment en mars et en novembre.

Deux modèles de classification ont été comparés. Malgré une accuracy plus faible, la régression logistique est plus adaptée à l’objectif du projet car elle détecte environ **61 % des vrais retards**, contre seulement 4 % pour le Random Forest.

Le projet montre ainsi l’importance de combiner préparation des données, analyse métier et choix de métriques adaptées avant d’interpréter les performances d’un modèle.
