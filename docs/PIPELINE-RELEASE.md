# ShopPlus — Pipeline GitHub Free + application HTTPS

Dernière vérification : 6 novembre 2026.

## Architecture réellement en place

| Composant | Fournisseur | État |
| --- | --- | --- |
| Dépôt source du projet | GitHub Free | Créé, actuellement **public** |
| Code complet de l'application en ligne | AppDeploy | Hébergé séparément, **pas encore importé dans GitHub** |
| Application HTTPS | AppDeploy | [Pilote en ligne](https://shopplus-haiti-pilote-ub21b4.v2.appdeploy.ai/) |
| Déploiement automatique depuis un push GitHub | — | **Non connecté** |
| Manifeste de version | `deployments/staging.json` | Actif |
| Test de l'application HTTPS après commit de manifeste | GitHub Actions | **Actif** |
| Ventes et paiements commerciaux | — | Désactivés |

Le workflow `.github/workflows/shopplus-staging-smoke.yml` suit le manifeste
`deployments/staging.json` et teste la version **déjà déployée**.
Il ne construit ni ne publie le serveur AppDeploy. Cette distinction est
essentielle pour éviter qu'un commit GitHub donne une fausse impression de
déploiement.

## Vérifications automatisées et leur portée

Lancer depuis GitHub Free : **Actions → ShopPlus - QA HTTPS (GitHub Free)**.
Les mêmes tests démarrent sur modification du manifeste ou des scripts QA.

Les tests effectuent uniquement des demandes sans paiement et sans session :

1. Interface web HTTPS accessible (HTTP 200).
2. Santé du backend et catalogue fictif.
3. Récupération des méthodes de paiement : MonCash / NatCash / carte désactivés ; paiement à la livraison TEST uniquement.
4. Devis calculé côté serveur, en HTG, avec commission prévisionnelle de **500 points de base (5 %)**.
5. Rejet des quantités invalides.
6. Refus des accès anonymes aux commandes clients, commandes vendeurs et données/actions administrateur.
7. Vérification que le manifeste interdit l'ouverture des ventes.

Première série complète de contrôles : **PASS** le 6 novembre 2026.
Résultat : https://github.com/rbourjeaud52-eng/ShopPlus/actions/runs/42180227090

Ces contrôles ne prouvent PAS les opérations avec sessions authentifiées,
la réception de paiements, les webhooks, la disponibilité de stock,
les reversements vendeur ni l'absence de vulnérabilités.

## Procédure de livraison actuelle (manuelle et prudente)

1. Modifier et déployer l'application via AppDeploy.
2. Attendre l'état `ready` et vérifier les erreurs et la QA.
3. Actualiser `deployments/staging.json` avec le nouvel identifiant de version (`snapshot_version`).
4. La mise à jour du manifeste déclenche GitHub Actions.
5. Consulter le résultat des contrôles HTTPS.
6. Ne pas activer les paiements commerciaux tant que les barrières ci-dessous sont en échec.

## Conditions bloquantes pour une véritable CI/CD

- **Rendre le dépôt privé** (GitHub Settings → General → Danger Zone).
  L'intégration GitHub actuellement disponible ne peut pas modifier ce
  paramètre ; un dépôt public expose tous les fichiers qui y sont poussés.
- Importer la **version AppDeploy actuelle**, et non seulement un ancien kit
  Flutter/FastAPI. Les deux bases de code ne sont pas interchangeables.
- Disposer d'une méthode de publication GitHub → AppDeploy officiellement
  supportée et autorisée. Aucun jeton ou point d'accès de déploiement machine
  n'a été configuré ici. Il serait dangereux d'en inventer un.
- Ajouter tests bout en bout **avec comptes clients, vendeurs et propriétaire
  administrateur autorisés**.
- Configurer dans la gestion chiffrée des secrets du backend
  `SHOPPLUS_ADMIN_EMAILS`; sa valeur n'est actuellement pas liée.
- Ouvrir les modes de paiement uniquement après contrat marchand, vérification
  du fournisseur, authentification des webhooks et tests de réconciliation.
- Contrôler les prix, le vrai stock, les livraisons, les litiges et
  la comptabilisation des commissions sur encaissements confirmés.
- Fournir les textes légaux et le support client.

## GitHub Free et dépenses

Aucun abonnement GitHub Pro n'est nécessaire pour créer un dépôt privé,
versionner le code et exécuter des GitHub Actions dans les quotas inclus.
Les coûts éventuels d'AppDeploy, du nom de domaine, des moyens de paiement
et des services tiers sont **indépendants** de GitHub.

Le mode pilote ne nécessite aucune saisie de carte ni transaction réelle.
