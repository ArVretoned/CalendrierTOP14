# Calendrier TOP14 🏉  
*[English below]*


## 🎯 Concept  

*Pour les amateurs du TOP14 qui veulent regarder les matchs en replay sans être spoilé*  

Pour ceux qui veulent regarder deux matchs (ou plus) du week-end en replay la semaine suivante mais qui ne savent pas par lequel commencer, c'est pratique d'avoir le plannig.  

## 📺 Mise en situation

Il y a un aléchant **ASM vs Avrion** et un **Stade Toulousain vs Section** le week-end. Si on veut les regarder en replay et éviter le fameux :  

> *"Comme l'ASM qui s'est imposé hier"*  

lâché par Éric Bayle alors qu'on a commencé par Stade Toulousain vs Section 😤  

… alors il faut absolument connaître l’ordre des matchs.

Mais trouver le calendrier **sans résultats** sur Internet ?  
👉 *C’est quasi impossible.* 😩  

Donc, c'est bien pratique d'avoir **un agenda perso** avec le programme !


## 🛠️ L’idée du script  

L'idée de ce script est assez simple : éviter la fastidieuse tâche de rentrer tous les matchs, à la main, dans son calendrier.  

Surtout que les horaires ne sont pas toutes connues à l'avance.  
Il faut faire la manip tous les 5 week-end environ.  

---

## 📦 Utilisation  

### 🐍 Installation

1. Cloner le projet  
2. Créer l’environnement Python à partir du `requirements.txt` :

```bash
python -m venv .venv
source .venv/bin/activate   # ou .venv\Scripts\activate sous Windows
pip install -r requirements.txt
```

3. Compléter le .env

```bash
cp .env.exemple .env
```
```ini
SAISON=2025-2026
URL_NLR=https://top14.lnr.fr/calendrier-et-resultats
URL_CLOUD= #URL du calendrier WebDAV
UTILISATEUR= #Nom d'utilisateur
CLE= #Clé d'accès
```

### ⚙️ Options du script


`--local` Génère un fichier `.ics` en local.  
Pratique pour importer manuellement dans n’importe quel agenda *(iOS, Google, Outlook…)*.

`--enligne` Écrit directement dans un agenda en ligne via WebDAV.  
Testé sur un agenda Nextcloud auto-hébergé

# TOP14 agenda 🏉

Et bien non, car comme l'a dit l'homme des cavernes :  
**"We are in France, we speak french"** 🇫🇷  

![alt text](https://media1.tenor.com/m/bEjkwM76WvAAAAAd/sebastien-chabal-we-are-in-france.gif)

## 😁😇