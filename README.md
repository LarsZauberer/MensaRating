# MensaRating

In den Schulen ist die Mensa nicht immer gut. Man kann nie Wissen, ob das Essen
schmeckt, bis man es gekauft hat. Dieser Problemstellung widmet sich dieses
Projekt. Es soll das Essen an der Mensa der Neuen Kantonsschule Aarau bewerten
werden. Genauer soll das Essen von den Schülern/Kunden selbst bewertet werden.
Das soll mithilfe eines neuen Bewertungsportal in Form einer Webseite ermöglicht
werden. Dadurch kann man schon einen Blick auf das Essen erhaschen, bevor man es
gekauft hat.

## Nutzung
### Öffentliche Seite
Es gibt eine öffentliche Seite: [MensaRating](http://mensarating.herokuapp.com/)

### Local Instance
Getestet auf:
- Python 3.10.9

1. Laden Sie den ganzen Source Code des Projektes herunter.
2. Laden Sie alle Python Dependencies herunter (nach Bedarf, machen Sie ein virtual environment).
```bash
pip install -r requirements.txt
```
3. Migrieren der Datenbank
```bash
python manage.py migrate
```
4. (optional) Erstellen eines Admin-Accounts
```bash
python manage.py createsuperuser
```
Hier ist es wichtig, dass Sie nach dem Starten des Servers in Schritt 5 sich ins
Admin-Panel `localhost:8000/admin` gehen und sich dort mit dem erstellten Account
anmelden. Dann müssen Sie ein neues `Profil` erstellen, welches mit dem
erstellten Admin-Account verknüpft ist.

5. Starten des Servers
```bash
python manage.py runserver
```
6. Öffnen Sie die Webseite über http://localhost:8000

## Admin-Page
Auf die Admin-Page http://localhost:8000/admin kann man nur mit einem
Admin-Account gelangen. Dort befinden sich alle Datenbankmodelle, wo die
einzelnen Daten verwaltet und manipuliert werden können.
