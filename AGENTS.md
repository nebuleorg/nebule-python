# Nebule Python - Documentation Technique

*Version: 0.1 - Dernière mise à jour: 2026-10-17*
*Projet: nebule-python*
*Site: www.nebule.org*

---

## Table des matières

1. [Structure du projet](#1-structure-du-projet)
2. [Architecture et synchronisation avec PHP](#2-architecture-et-synchronisation-avec-php)
3. [Structure des liens nebule](#3-structure-des-liens-nebule)
4. [Organisation du code Python](#4-organisation-du-code-python)
5. [Fonctionnement de prep_library.py](#5-fonctionnement-de-prep_librarypy)
6. [Conventions de nommage](#6-conventions-de-nommage)
7. [Flux de travail recommandé](#7-flux-de-travail-recommandé)
8. [Points d'attention](#8-points-dattention)
9. [Références utiles](#9-références-utiles)

---


## 1. Structure du projet

```
nebule-python/
├── AGENTS.md                    # Ce fichier - documentation technique
├── nebule.py                    # Bootstrap Python (équivalent de bootstrap.php)
├── prep_library.py              # Script d'assemblage de la librairie
├── nebule_library.py            # Copie de référence de la librairie assemblée
├── library/                     # Code source modulaire de la librairie
│   ├── 000_init.py
│   ├── 001_nebule.py
│   ├── 002_references.py
│   ├── 003_functions.py
│   ├── 004_metrology.py
│   ├── 005_configuration.py
│   ├── ...
│   ├── 500_link_interface.py
│   ├── 501_bloclink.py
│   ├── 502_link_register.py
│   ├── 999_license.py
│   └── __init__.py
├── o/                          # Dossier des objets (gérés par leur empreinte)
│   └── <hash>.sha2.256          # Objets avec nom = empreinte cryptographique
├── l/                          # Dossier des liens
│   ├── <nid>.sha2.256           # Fichiers de liens par nœud source
│   └── h                       # Historique de tous les liens
└── prep.sh                     # Script bash pour l'assemblage rapide
```

---


## 2. Architecture et synchronisation avec PHP

### 2.1 Correspondance PHP ↔ Python

| Élément | PHP | Python |
|---------|-----|--------|
| Bootstrap | `bootstrap.php` | `nebule.py` |
| Librairie OO | `lib_nebule/` | `library/` |
| Dossier objets | `o/` | `o/` |
| Dossier liens | `l/` | `l/` |
| Dossier session | `c/` | `c/` |
| Dossier entité | `e/` | `e/` |
| Fichier historique | `h/` | `l/h` |

### 2.2 Synchronisation fonctionnelle

**Le code Python doit rester synchronisé avec le code PHP en termes de :**

1. **Fonctionnalités de base** :
   - Gestion des nœuds (Node)
   - Gestion des liens (Link)
   - Gestion des entités (Entity)
   - Chiffrement et signatures
   - Cache et session

2. **Structure des données** :
   - Format des NID (Node ID)
   - Format des liens (Bloc Link)
   - Algorithmes de hachage (sha2.256, sha2.512, etc.)
   - Structure des objets

3. **Conventions** :
   - Nommage des fichiers
   - Organisation des dossiers
   - Format des métadonnées

4. **Constantes partagées** :
   - `LIB_REF_CODE_ALGO = 'sha2.256'`
   - `LIB_LINK_VERSION = '2:0'`
   - `LIB_LOCAL_LINKS_FOLDER = 'l'`
   - `LIB_LOCAL_OBJECTS_FOLDER = 'o'`

### 2.3 Fichiers PHP de référence

Pour maintenir la synchronisation, se référer à :

- **bootstrap.php** : Initialisation, chargement de la librairie, gestion des erreurs
- **lib_nebule/001_nebule.php** : Classe principale Nebule
- **lib_nebule/002_references.php** : Constants et références globales
- **lib_nebule/004_metrology.php** : Métrologie et logging
- **lib_nebule/500_link_interface.php** : **Structure des liens (CRUCIAL)**
- **lib_nebule/501_bloclink.php** : Implémentation des blocs de liens
- **lib_nebule/502_link_register.php** : Registre des liens

### 2.4 Scripts PHP de préparation

- **prep_loop_code_master_php.sh** : Script de préparation du code master PHP
  - Montre comment les liens sont créés et signés
  - Exemple de format de liens à suivre

---


## 3. Structure des liens nebule

### 3.1 Format général

Un **Bloc de Liens** suit la structure : **`BH_BL_BS`**

```
+----------------+ +-------------------------------+ +--------------------------+
|     BH         | |           BL                  | |          BS               |
| (Block Header) | |     (Block Links)             | |   (Block Signature)       |
+----------------+ +-------------------------------+ +--------------------------+
```

Séparateurs :
- `BH_BL` : premier underscore (`_`)
- `BL_BS` : deuxième underscore (`_`)

### 3.2 Block Header (BH)

**Format** : `nebule:link/<version>`

- `nebule:link` = APP:TYP (Application:Type)
- `<version>` = VER:SUB (Version:Sous-version)

**Exemple** : `nebule:link/2:0`

### 3.3 Block Links (BL)

**Format** : `RC/RL1/RL2/RL3/...`

#### 3.3.1 Chronology Register (RC)

**Format** : `MOD>CHR`

- `MOD` : Mode (actuellement toujours `"0"`)
- `CHR` : Timestamp (Unix timestamp en secondes)

**Exemple** : `0>1792235888`

#### 3.3.2 Link Register (RL)

**Format** : `REQ>NID1>NID2>NID3>NID4`

- `REQ` : Type de requête (1 caractère)
  - `l` : Link (lien entre objets)
  - `f` : Fork (dérivé/parenté)
  - `u` : Update (mise à jour)
  - `d` : Delete (suppression)
  - `e` : Equivalent (objets interchangeables)
  - `c` : Concealed (lien chiffré/dissimulé)
  - `k` : Encrypted object (objet chiffré)
  - `s` : Subdivision (fragment d'objet)
  - `x` : Link deletion (suppression de lien)

- `NID1...NID4` : Identifiants de nœuds (3 à 4 typiquement)
  - `NID1` : Source du lien
  - `NID2` : Cible du lien
  - `NID3` : Méta-information ou type (optionnel)
  - `NID4` : Autres informations (optionnel)

**Exemple** : `l>88848d09edc4...>bee2d069...>0`
- REQ = `l` (lien)
- NID1 = `88848d09edc4...` (source = entité maître)
- NID2 = `bee2d069...` (cible = objet librairie)
- NID3 = `0` (pas de méta)

### 3.4 Block Signature (BS)

**Format** : `_EID1>SIG1.algo1.size1_EID2>SIG2.algo2.size2...`

En pratique (pour un seul signataire) : `_EID>SIG.algo.size`

- `EID` : Identifiant de l'entité signataire (NID)
- `SIG` : Signature cryptographique (hexadécimale)
- `algo.size` : Algorithme et taille (ex: `sha2.256`)

**Exemple** : `_88848d09edc4...>000000...0.sha2.256`
- EID = `88848d09edc4...`
- SIG = `000000...0` (mock pour l'instant)
- algo.size = `sha2.256`

### 3.5 Exemple complet

```
nebule:link/2:0_0>1792235888/l>88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256>
0b9240e54f9a54687ef1eb59122a78d9ee73d5ae02bb239138c00fd077af536c.sha2.256>0_
88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256>
0000000000000000000000000000000000000000000000000000000000000000.sha2.256
```

Découpage :
```
BH:  nebule:link/2:0
BL:  0>1792235888/l>88848d09...>0b9240e5...>0
BS:  _88848d09...>0000...0.sha2.256
```

### 3.6 Stockage des liens

Les blocs de liens sont stockés dans le dossier `l/` :

- **Un fichier par NID source** : `l/<NID>`
  - Chaque ligne = un bloc de liens complet où ce NID apparaît
  - Plusieurs blocs peuvent exister pour un même NID
  
- **Fichier historique** : `l/h`
  - Contient tous les blocs de liens créés
  - Une ligne par bloc

**Exemple** :
```
l/
├── 88848d09edc4...sha2.256    # Liens où cette entité apparaît
├── 0b9240e54f9a...sha2.256    # Liens où cet objet apparaît
└── h                           # Historique complet
```

---


## 4. Organisation du code Python

### 4.1 Structure modulaire

La librairie est organisée en fichiers numérotés pour :

1. **Maintenir l'ordre de dépendance**
2. **Faciliter la synchronisation avec PHP** (même numérotation)
3. **Permettre l'assemblage en un seul fichier**

**Ordre de chargement** (voir `LIBRARY_FILE_ORDER` dans `prep_library.py`) :

```
000-009 : Initialisation, métrologie, configuration, utilitaires
010-014 : Cache, session, tokenization, routage
100-114 : Interfaces I/O (io_interface, io, io_disk, io_network_*)
200-204 : Interfaces et implémentations Crypto
300-312 : Interfaces et implémentations Social
400-409 : Interfaces et implémentations Node (node, group, entity, location, conversation, currency, tokenpool, token, wallet)
500-503 : Interfaces et implémentations Link (link_interface, bloclink, link_register, transaction)
999    : License
```

### 4.2 Fichiers clés

| Fichier | Rôle | Équivalent PHP |
|---------|------|----------------|
| `000_init.py` | Initialisation des constantes | `lib_nebule/000_init.php` |
| `001_nebule.py` | Classe principale Nebule | `lib_nebule/001_nebule.php` |
| `002_references.py` | Références et types | `lib_nebule/002_references.php` |
| `003_functions.py` | Fonctions utilitaires | `lib_nebule/003_functions.php` |
| `004_metrology.py` | Métrologie et logging | `lib_nebule/004_metrology.php` |
| `005_configuration.py` | Configuration | `lib_nebule/005_configuration.php` |
| `500_link_interface.py` | Interface des liens | `lib_nebule/500_link_interface.php` |
| `501_bloclink.py` | Bloc de liens | `lib_nebule/501_bloclink.php` |

### 4.3 Classes principales

- **Nebule** (`001_nebule.py`) : Classe centrale de la librairie
- **Node** (`401_node.py`) : Gestion des nœuds
- **BlocLink** (`501_bloclink.py`) : Gestion des blocs de liens
- **LinkRegister** (`502_link_register.py`) : Registre des liens

---


## 5. Fonctionnement de prep_library.py

### 5.1 Rôle

Le script `prep_library.py` permet de :

1. **Assembler** tous les fichiers de `library/` en un seul fichier
2. **Calculer** l'empreinte SHA2-256 du fichier assemblé
3. **Nommer** le fichier résultant selon son empreinte (`<hash>.sha2.256`)
4. **Placer** le fichier dans `o/`
5. **Créer** les liens correspondants dans `l/`
6. **Copier** une version de référence dans `nebule_library.py`

### 5.2 Usage

```bash
python3 prep_library.py \
    --master-entity <entity_id> \
    --master-password <password> \
    [--clean] \
    [--verbose]
```

**Exemple** :
```bash
python3 prep_library.py \
    --master-entity 88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256 \
    --master-password mypassword \
    --clean
```

### 5.3 Étapes détaillées

1. **Nettoyage** (si `--clean`) : Suppression des fichiers existants dans `o/`
2. **Assemblage** : Concatenation de tous les fichiers de `library/` dans l'ordre
3. **Calcul du hash** : SHA2-256 du fichier assemblé
4. **Création du NID** : Format `<hash>.sha2.256`
5. **Écriture dans o/** : Fichier nommé par son empreinte
6. **Création des liens** :
   - Génération du bloc de liens (BH_BL_BS)
   - Extraction des NID référencés
   - Écriture dans les fichiers correspondants dans `l/`
   - Ajout à l'historique `l/h`
7. **Copie de référence** : `nebule_library.py` au niveau du script

### 5.4 Fonctions internes

Voir la documentation dans le code pour :

- `compute_file_hash()` : Calcul du hash d'un fichier
- `format_node_id()` : Formatage d'un NID
- `create_bh()`, `create_rc()`, `create_rl()`, `create_bl()`, `create_bs()` : Création des composants de lien
- `create_simple_link()` : Création d'un lien complet
- `extract_nids_from_*()` : Extraction des NID depuis les différentes parties
- `write_link_file()` : Écriture dans les fichiers de liens

---


## 6. Conventions de nommage

### 6.1 Node ID (NID)

**Format** : `<hash>.<algo>.<size>` ou `<hash>.<algo>` (le size est optionnel dans le nom de fichier)

- `<hash>` : Empreinte hexadécimale (64 caractères pour SHA2-256)
- `<algo>` : Algorithme de hachage (ex: `sha2`, `sha3`, etc.)
- `<size>` : Taille en bits (ex: `256`, `512`)

**Exemples** :
- `88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256`
- `0b9240e54f9a54687ef1eb59122a78d9ee73d5ae02bb239138c00fd077af536c.sha2.256`

**Règle importante** : Les NID ne doivent **pas contenir de underscores** (`_`) car ce caractère est utilisé comme séparateur dans la structure des liens.

### 6.2 Nommage des fichiers

| Type | Dossier | Nom du fichier | Exemple |
|------|---------|----------------|---------|
| Objet (librairie) | `o/` | `<hash>.sha2.256` | `88848d09...sha2.256` |
| Lien par nœud | `l/` | `<nid>` | `88848d09...sha2.256` |
| Historique | `l/` | `h` | `h` |
| Entité | (futur) | `e` | `e` |
| Configuration | (futur) | `c` | `c` |

---


## 7. Flux de travail recommandé

### 7.1 Modification du code

1. **Modifier** les fichiers dans `library/`
2. **Tester** les modifications individuellement
3. **Assembler** avec `prep_library.py`
4. **Vérifier** que le hash correspond au contenu

### 7.2 Synchronisation avec PHP

1. **Comparer** les fichiers `lib_nebule/` avec `library/`
2. **Mettre à jour** les fichiers Python pour refléter les changements PHP
3. **Vérifier** les structures de données (NID, liens, etc.)
4. **Tester** les deux versions avec les mêmes entrées

### 7.3 Création d'une nouvelle version

1. **Modifier** les fichiers sources dans `library/`
2. **Exécuter** `prep_library.py` avec les bonnes entités
3. **Vérifier** que `nebule_library.py` est à jour
4. **Copier** le fichier de `o/` vers les autres projets si nécessaire

### 7.4 Dépannage

- **Problème de hash** : Vérifier que le fichier n'a pas été modifié après assemblage
- **Problème de liens** : Vérifier la structure BH_BL_BS avec un debug verbose
- **Problème de NID** : S'assurer que les NID ne contiennent pas d'underscores

---


## 8. Points d'attention

### 8.1 Compatibilité PHP

- **Les NID doivent être compatibles** : Même format, même algorithme de hachage
- **Les liens doivent suivre la même structure** : BH_BL_BS avec les mêmes séparateurs
- **Les constants doivent être identiques** : LIB_REF_CODE_ALGO, LIB_LINK_VERSION, etc.

### 8.2 Performances

- Le calcul du hash SHA2-256 sur de gros fichiers peut être lent
- L'assemblage de la librairie peut prendre du temps si beaucoup de fichiers
- Le script utilise la lecture par chunks (8192 octets) pour gérer les gros fichiers

### 8.3 Sécurité

- **Les signatures sont mock pour l'instant** : Utilisation de zéros comme placeholder
- **À implémenter** : Signatures réelles avec OpenSSL ou Sodium
- **Gestion des clés** : Le mot de passe de l'entité maître est nécessaire pour la signature

### 8.4 Limitations actuelles

1. **Signatures** : Utilisation de signatures mock (zéros)
   - À remplacer par des signatures réelles avec la clé privée
   - Voir `prep_loop_code_master_php.sh` pour l'implémentation PHP

2. **Timestamp** : Utilisation de Unix timestamp
   - Le PHP utilise un format personnalisé (ex: `020260714000000`)
   - À synchroniser si nécessaire

3. **Gestion des erreurs** : Certaines erreurs ne sont pas encore gérées

4. **Validation des liens** : Pas encore implémentée
   - Vérification des signatures
   - Vérification de la structure

---


## 9. Références utiles

### 9.1 Fichiers importants

- **nebule.py** : Bootstrap Python (à comparer avec bootstrap.php)
- **prep_library.py** : Script d'assemblage
- **library/500_link_interface.py** : Interface des liens (documentation)
- **library/501_bloclink.py** : Implémentation des blocs de liens
- **library/001_nebule.py** : Classe principale

### 9.2 Commandes utiles

```bash
# Assemblage rapide
./prep.sh

# Assemblage avec nettoyage
python3 prep_library.py --master-entity <eid> --master-password <pwd> --clean --verbose

# Vérification du hash
python3 -c "import hashlib; print(hashlib.sha256(open('o/<hash>.sha2.256', 'rb').read()).hexdigest())"

# Diff entre la copie de référence et le fichier assemblé
diff nebule_library.py o/<hash>.sha2.256

# Liste des fichiers dans l/
ls -la l/

# Contenu d'un fichier de liens
cat l/<nid>
```

### 9.3 Correspondance avec les scripts PHP

| Script Python | Script PHP | Rôle |
|---------------|------------|------|
| `prep_library.py` | `prep_loop_code_master_php.sh` | Assemblage et création des liens |
| `nebule.py` | `bootstrap.php` | Bootstrap et chargement |

### 9.4 Sites et ressources

- **Site officiel** : https://www.nebule.org
- **Dépôt PHP** : `~/workspace/nebule-php/`
- **Dépôt Python** : `~/workspace/nebule-python/`
- **Code Master PHP** : `~/code.master.nebule.org/`

---


## 10. Historique des modifications

- **2026-10-17** : Création initiale de AGENTS.md
- **2026-10-17** : Mise à jour de prep_library.py pour générer des liens conformes à la structure PHP
- **2026-10-17** : Ajout de la gestion des NID, hash, et structure BH_BL_BS

---


## 11. Questions fréquentes (FAQ)

### Q: Comment ajouter un nouveau fichier à la librairie ?
A: Ajouter le fichier dans `library/` avec un numéro approprié, puis mettre à jour `LIBRARY_FILE_ORDER` dans `prep_library.py`.

### Q: Pourquoi le hash change à chaque exécution ?
A: Le hash dépend du contenu exact du fichier. Si le timestamp dans le header change, le hash change. Utiliser `--clean` pour nettoyer avant assemblage.

### Q: Comment vérifier qu'un lien est valide ?
A: Pour l'instant, les signatures sont mock. La validation complète nécessitera l'implémentation de la vérification des signatures.

### Q: Où sont stockées les configurations ?
A: Les configurations sont définies dans `005_configuration.py` et les constantes dans `000_init.py`.

### Q: Comment synchroniser avec le code PHP ?
A: Comparer les fichiers `lib_nebule/` avec `library/`, en particulier les fichiers 000-009, 500-503. Vérifier que les structures (NID, liens) sont identiques.

### Q: Quel algorithme de hachage utiliser ?
A: SHA2-256 (`sha2.256`) par défaut, comme défini dans `LIB_REF_CODE_ALGO`.

### Q: Comment nommer un nouveau fichier d'objet ?
A: Calculer son hash SHA2-256, puis utiliser le format `<hash>.sha2.256`.

---


*Document généré pour faciliter la reprise du travail dans PyCharm.*
*À mettre à jour régulièrement lors des modifications du code.*
