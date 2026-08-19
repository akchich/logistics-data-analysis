import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler

orders = pd.read_csv("../data/olist_orders_dataset.csv")

print(orders.head())
print(orders.columns)
print(orders.shape)

orders["order_delivered_customer_date"] = pd.to_datetime(
    orders["order_delivered_customer_date"]
)

orders["order_estimated_delivery_date"] = pd.to_datetime(
    orders["order_estimated_delivery_date"]
)

orders["retard"] = (
    orders["order_delivered_customer_date"]
    > orders["order_estimated_delivery_date"]
)

print(orders[[
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "retard"
]].head())
taux_retard = orders["retard"].mean() * 100

print(f"Taux de commandes en retard : {taux_retard:.2f}%")
print("\nValeurs manquantes :")
print(orders.isnull().sum())
orders_livrees = orders.dropna(subset=["order_delivered_customer_date"]).copy()

orders_livrees["retard"] = (
    orders_livrees["order_delivered_customer_date"]
    > orders_livrees["order_estimated_delivery_date"]
)

taux_retard_livrees = orders_livrees["retard"].mean() * 100

print(f"Nombre de commandes livrées : {len(orders_livrees)}")
print(f"Taux de retard parmi les commandes livrées : {taux_retard_livrees:.2f}%")
orders_livrees["jours_retard"] = (
    orders_livrees["order_delivered_customer_date"]
    - orders_livrees["order_estimated_delivery_date"]
).dt.days

retards = orders_livrees[orders_livrees["retard"] == True]

print(
    f"Retard moyen : {retards['jours_retard'].mean():.2f} jours"
)
customers = pd.read_csv("../data/olist_customers_dataset.csv")

print(customers.head())
print(customers.columns)
print(customers.shape)
orders_clients = orders_livrees.merge(
    customers,
    on="customer_id",
    how="left"
)

print(orders_clients.shape)

print(
    orders_clients[
        ["order_id", "customer_city", "customer_state", "retard"]
    ].head()
)
retard_par_etat = (
    orders_clients
    .groupby("customer_state")["retard"]
    .mean()
    .sort_values(ascending=False)
    * 100
)

print("\nTaux de retard par État :")
print(retard_par_etat.head(10))
volume_par_etat = (
    orders_clients
    .groupby("customer_state")
    .size()
    .sort_values(ascending=False)
)

print("\nNombre de commandes par État :")
print(volume_par_etat.head(10))
analyse_etat = (
    orders_clients
    .groupby("customer_state")
    .agg(
        nombre_commandes=("order_id", "count"),
        taux_retard=("retard", "mean")
    )
)

analyse_etat["taux_retard"] = analyse_etat["taux_retard"] * 100

analyse_etat = analyse_etat.sort_values(
    by="taux_retard",
    ascending=False
)

print("\nAnalyse par État :")
print(analyse_etat.head(10))
import matplotlib.pyplot as plt

top_etats = analyse_etat.head(10)
plt.figure()
top_etats["taux_retard"].plot(kind="bar")

plt.title("Top 10 des États par taux de retard")
plt.xlabel("État")
plt.ylabel("Taux de retard (%)")

plt.axhline(
    y=taux_retard_livrees,
    linestyle="--",
    label="Moyenne globale"
)

plt.legend()
plt.tight_layout()
plt.savefig("../images/taux_retard_etats.png", dpi=300, bbox_inches="tight")
#plt.show()
order_items = pd.read_csv("../data/olist_order_items_dataset.csv")

print(order_items.head())
print(order_items.columns)
print(order_items.shape)
order_items_agg = (
    order_items
    .groupby("order_id")
    .agg(
        total_price=("price", "sum"),
        total_freight=("freight_value", "sum"),
        nombre_articles=("order_item_id", "count")
    )
    .reset_index()
)

print(order_items_agg.head())
print(order_items_agg.shape)
dataset_final = orders_clients.merge(
    order_items_agg,
    on="order_id",
    how="left"
)

print(dataset_final.shape)

print(
    dataset_final[
        [
            "order_id",
            "customer_state",
            "total_price",
            "total_freight",
            "nombre_articles",
            "retard"
        ]
    ].head()
)
dataset_final["order_purchase_timestamp"] = pd.to_datetime(
    dataset_final["order_purchase_timestamp"]
)

dataset_final["jour_semaine"] = (
    dataset_final["order_purchase_timestamp"].dt.dayofweek
)

dataset_final["mois"] = (
    dataset_final["order_purchase_timestamp"].dt.month
)

dataset_final["heure_commande"] = (
    dataset_final["order_purchase_timestamp"].dt.hour
)

print(
    dataset_final[
        [
            "order_purchase_timestamp",
            "jour_semaine",
            "mois",
            "heure_commande"
        ]
    ].head()
)
retard_par_jour = (
    dataset_final
    .groupby("jour_semaine")["retard"]
    .mean()
    * 100
)

print("\nTaux de retard par jour de la semaine :")
print(retard_par_jour)
jours = {
    0: "Lundi",
    1: "Mardi",
    2: "Mercredi",
    3: "Jeudi",
    4: "Vendredi",
    5: "Samedi",
    6: "Dimanche"
}

retard_par_jour.index = retard_par_jour.index.map(jours)

print("\nTaux de retard par jour :")
print(retard_par_jour)
retard_par_mois = (
    dataset_final
    .groupby("mois")["retard"]
    .mean()
    * 100
)

print("\nTaux de retard par mois :")
print(retard_par_mois)
plt.figure()

mois_noms = {
    1: "Jan",
    2: "Fév",
    3: "Mar",
    4: "Avr",
    5: "Mai",
    6: "Juin",
    7: "Juil",
    8: "Août",
    9: "Sept",
    10: "Oct",
    11: "Nov",
    12: "Déc"
}

retard_par_mois.index = retard_par_mois.index.map(mois_noms)

retard_par_mois.plot(kind="line", marker="o")

plt.title("Évolution du taux de retard par mois")
plt.xlabel("Mois")
plt.ylabel("Taux de retard (%)")

plt.axhline(
    y=taux_retard_livrees,
    linestyle="--",
    label="Moyenne globale"
)

plt.legend()
plt.tight_layout()

plt.savefig(
    "../images/taux_retard_mois.png",
    dpi=300,
    bbox_inches="tight"
)

#plt.show()
dataset_final["order_estimated_delivery_date"] = pd.to_datetime(
    dataset_final["order_estimated_delivery_date"]
)

dataset_final["delai_prevu_jours"] = (
    dataset_final["order_estimated_delivery_date"]
    - dataset_final["order_purchase_timestamp"]
).dt.days


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline


numeric_features = [
    "total_price",
    "total_freight",
    "nombre_articles",
    "jour_semaine",
    "mois",
    "heure_commande",
    "delai_prevu_jours"
]

categorical_features = [
    "customer_state"
]

features = numeric_features + categorical_features

ml_data = dataset_final[features + ["retard"]].dropna()

print("\nDonnées utilisées pour le Machine Learning :")
print(ml_data.shape)
print(ml_data["retard"].value_counts())


X = ml_data[features]
y = ml_data["retard"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            StandardScaler(),
            numeric_features
        ),
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ]
)


logistic_pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced"
            )
        )
    ]
)


logistic_pipeline.fit(X_train, y_train)

y_pred_logistic = logistic_pipeline.predict(X_test)


print("\nRégression logistique avec customer_state")
print("\nMatrice de confusion :")
print(confusion_matrix(y_test, y_pred_logistic))

print("\nRapport de classification :")
print(classification_report(y_test, y_pred_logistic))
from sklearn.ensemble import RandomForestClassifier

random_forest_pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            RandomForestClassifier(
                n_estimators=200,
                random_state=42,
                class_weight="balanced",
                n_jobs=-1
            )
        )
    ]
)

random_forest_pipeline.fit(X_train, y_train)

y_pred_rf = random_forest_pipeline.predict(X_test)

print("\nRandom Forest")
print("\nMatrice de confusion :")
print(confusion_matrix(y_test, y_pred_rf))

print("\nRapport de classification :")
print(classification_report(y_test, y_pred_rf))
dataset_final.to_csv(
    "../data/dataset_final_logistics.csv",
    index=False
)