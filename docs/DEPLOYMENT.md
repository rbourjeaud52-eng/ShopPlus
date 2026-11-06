# ShopPlus — GitHub Free et déploiement HTTPS

## Environnement

- **Dépôt GitHub** : https://github.com/rbourjeaud52-eng/ShopPlus
- **Site pilote** : https://shopplus-haiti-pilote-ub21b4.v2.appdeploy.ai/
- **Mode actuel** : DEMO / TEST UNIQUEMENT ; ventes réelles fermées.
- **Code source du site actuel** : stocké dans AppDeploy ; pas encore importé dans ce dépôt.

## Respect de la confidentialité

Le propriétaire veut un dépôt **privé** et une utilisation de **GitHub Free**.

**ÉTAPE REQUISE** : changer la visibilité de ce dépôt public en privé depuis la page *Settings → General → Danger Zone → Change repository visibility*. La connexion ChatGPT GitHub actuelle ne donne pas de méthode permettant de changer la visibilité automatiquement.

Ne pas pousser les sources du backend avant ce changement. Aucun secret, jeton, certificat ou fichier .env ne doit être commité.

## État du prototype HTTPS

- Catalogue fictif, recherche et panier : opérationnels en mode pilote.
- Candidature vendeur et brouillons produits : stockage authentifié.
- Commandes d'essai : API créée avec références idempotentes et historique privé par compte.
- Paiement à la livraison : **simulation uniquement**.
- MonCash, NatCash, cartes : désactivés tant que des comptes marchands, API et tests ne sont pas fournis.
- Commissions ShopPlus : **5 % calculés sur la commande TEST côté serveur**; aucun revenu comptable généré.
- Administration : routes protégées par authentification et liste blanche des emails administrateurs. Sans configuration secrète SHOPPLUS_ADMIN_EMAILS, l'accès reste refusé.
- Produits vendeurs non publiés ; aucun stock réel ni expédition en cours.

## Avant toute vente réelle

1. Importer les sources dans ce dépôt après mise en privé.
2. Configurer le ou les emails propriétaires autorisés au backend (secret côté serveur, non commité).
3. Créer des produits réels et des rôles vendeurs vérifiés.
4. Concevoir des commandes commerciales atomiques avec contrôle de stock et réservation, taxes/frais, remboursements et idempotence.
5. Connecter le paiement à la livraison avec preuve de remise et rapprochement financier.
6. Intégrer MonCash et NatCash seulement après validation officielle des API et du compte marchand.
7. Ajouter un fournisseur carte certifié avec webhooks signés ; ne jamais stocker des numéros de carte.
8. Journal de commissions 5 % : vente confirmée et encaissée, annulation, remboursement, reversements.
9. Conditions d'utilisation, politique confidentialité, support, gestion des réclamations, sauvegardes et audits sécurité.
10. Exécuter les tests clients, vendeurs et administrateurs avec de vrais comptes avant ouverture.

Le maintien de GitHub Free n'assure pas que l'hébergement, les services de paiement, la base de données ou les domaines personnalisés seront gratuits.
