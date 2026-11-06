# ShopPlus Haïti

Application e-commerce et marketplace conçue pour les clients et vendeurs en Haïti.

## Version actuellement en ligne

**Prototype pilote (HTTPS)** : https://shopplus-haiti-pilote-ub21b4.v2.appdeploy.ai/

L'application en ligne possède un catalogue de démonstration, un panier, une connexion utilisateur, des candidatures vendeurs et des brouillons produits. Le backend a aussi des routes de commandes **de test** et une base de sécurisation de l'administration.

> **Important : aucune vente ni transaction réelle n'est autorisée pour le moment.** Les produits affichés sont fictifs. MonCash, NatCash et les cartes bancaires n'encaissent aucun paiement.

## GitHub Free

Ce dépôt sert à versionner le code. Le site HTTPS est hébergé séparément ; un dépôt GitHub Free ne constitue pas à lui seul un hébergement de backend commercial et de paiements.

### Étape de confidentialité requise

Avant l'import du code complet, rendre ce dépôt **Private** dans **Settings → General → Danger Zone → Change repository visibility → Make private**.

Le propriétaire a demandé un dépôt privé pour ShopPlus. Le code source complet ne doit pas être importé tant que ce dépôt est public.

## Architecture du prototype

- Interface React/Vite responsive avec identité rouge grenat « Shop Plus ».
- Backend TypeScript sur AppDeploy et stockage de données du fournisseur.
- Connexion des clients et des vendeurs.
- Commandes d'essai uniquement ; commission de 5 % calculée à titre indicatif sur le serveur.
- Accès administrateur refusé par défaut tant qu'un compte propriétaire n'est pas explicitement autorisé.

## Liste de contrôle avant l'ouverture commerciale

- [ ] Dépôt privé et sauvegarde du code source complet.
- [ ] Sécurisation du compte administrateur et tests d'autorisation.
- [ ] Catalogue, stocks et vendeurs vérifiés.
- [ ] Commandes réelles atomiques, disponibilité des stocks et gestion des annulations.
- [ ] Livraison et paiement à la livraison avec preuve d'encaissement.
- [ ] Intégration contractuelle et tests MonCash / NatCash / carte.
- [ ] Webhooks et rapprochements financiers ; commissions de 5 % comptabilisées après encaissement.
- [ ] Conditions générales, politique de confidentialité, conformité et assistance client.
- [ ] Audit de sécurité, tests bout en bout, sauvegardes et restauration.

Dernière mise à jour : novembre 2026.
