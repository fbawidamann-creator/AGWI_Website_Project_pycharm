import mysql.connector
from flask import Flask, request, session, render_template, flash, redirect, url_for
from werkzeug.security import check_password_hash
from hashmaps import halle_hashmap, trainer_hashmap, add_trainer_to_hashmap, add_halle_to_hashmap
from geschaeftsobjekte import Adresse, Halle, Trainer, Bewertung
from datetime import date, datetime, timedelta

# Konstanten für die Datenbankverbindung
DB_USER = '?'
DB_PASSWORD = '?'
DB_HOST = '?'
DB_NAME = '?'

# Flask-App initialisieren
app = Flask(__name__)
app.secret_key = "8474747"  # Setze einen geheimen Schlüssel für Sessions


# Hilfsfunktionen:

def connect_to_database():
    """
    Stellt eine Verbindung zur MySQL-Datenbank her und gibt den Cursor zurück.
    Wenn die Verbindung fehlschlägt, wird None zurückgegeben.
    """
    try:
        cnx = mysql.connector.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            database=DB_NAME
        )
        cursor = cnx.cursor(dictionary=True)
        print("Verbindung zur Datenbank erfolgreich hergestellt!")
        return cnx, cursor
    except mysql.connector.Error as err:
        print(f"Fehler bei der Verbindung zur Datenbank: {err}")
        return None, None


# Startseite
@app.route('/')
def hello_world():
    """Zeigt die Startseite und zählt die Besuche des Benutzers."""
    mycounter = session.get("counter", 0)
    mycounter += 1
    session['counter'] = mycounter
    print(f"Session counter: {mycounter}")
    return render_template('base.html')


# Login-Seite
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        cnx, cursor = connect_to_database()
        if not cnx:
            flash("Fehler bei der Verbindung zur Datenbank.", "danger")
            return render_template('login.html')

        try:
            query = "SELECT password FROM users WHERE name = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            if user and password == user[0]:

                flash("Login erfolgreich!", "success")
                return redirect(url_for('loggedin'))
            else:
                flash("Ungültiger Benutzername oder Passwort!", "danger")

        except Exception as e:
            flash(f"Ein Fehler ist aufgetreten: {e}", "danger")
        finally:
            cursor.close()
            cnx.close()

    return render_template('loggedin.html')


# Trainer-Seite
@app.route('/trainer')
def zeige_trainer():
    """Zeigt eine Liste von Trainern an."""
    cnx, cursor = connect_to_database()
    if not cnx:
        flash("Fehler bei der Verbindung zur Datenbank.", "danger")
        return render_template('trainer.html', trainers=[])

    try:
        query = "SELECT * FROM trainer"
        cursor.execute(query)
        trainers = cursor.fetchall()

    except Exception as e:
        flash(f"Fehler beim Abrufen der Trainer: {e}", "danger")
        trainers = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('trainer.html', trainers=trainers)


# Hallen-Seite
@app.route('/hallen')
def hallen():
    cnx, cursor = connect_to_database()
    if not cnx:
        flash("Fehler bei der Verbindung zur Datenbank.", "danger")
        return render_template('hallen.html', hallen=[])

    try:
        query = "SELECT * FROM locations"
        cursor.execute(query)
        hallen = cursor.fetchall()

    except Exception as e:
        flash(f"Fehler beim Abrufen der Hallen: {e}", "danger")
        hallen = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('hallen.html', hallen=hallen)


# Bewertungs-Seite
@app.route('/bewerten')
def zeige_bewertung():
    """Zeigt die Bewertungsseite an."""
    return render_template('bewerten.html')


# Trainer hinzufügen
@app.route('/trainer/hinzufuegen', methods=['GET', 'POST'])
def trainer_hinzufuegen():

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        image_url = request.form.get('image_url')
        birthday = request.form.get('birthday')
        bewertung = request.form.get('bewertung')


        try:
            bewertung = int(bewertung)
            if bewertung < 1 or bewertung > 5:
                flash("Die Bewertung muss zwischen 1 und 5 liegen!", "danger")
                return redirect(url_for('trainer_hinzufuegen'))
        except ValueError:
            flash("Die Bewertung muss eine Zahl sein!", "danger")
            return redirect(url_for('trainer_hinzufuegen'))


        cnx, cursor = connect_to_database()
        if not cnx:
            flash("Fehler bei der Verbindung zur Datenbank.", "danger")
            return redirect(url_for('trainer_hinzufuegen'))

        try:
            query_insert = """
                INSERT INTO trainer (name, email, image_url, birthday, bewertung)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query_insert, (name, email, image_url, birthday, bewertung))
            cnx.commit()
            trainerId = cursor.lastrowid
            add_trainer_to_hashmap(trainerId, name, email, image_url, birthday)

            flash("Trainer erfolgreich hinzugefügt!", "success")
            return redirect(url_for('trainer_hinzufuegen'))

        except Exception as e:
            flash(f"Ein Fehler ist aufgetreten: {e}", "danger")
        finally:
            cursor.close()
            cnx.close()

    return render_template('trainer_hinzufuegen.html')


# Hallen hinzufügen
@app.route('/hallen/hinzufuegen', methods=['GET', 'POST'])
def hallen_hinzufuegen():

    if request.method == 'POST':
        name = request.form.get('name')
        image_url = request.form.get('image_url')
        opening_time = request.form.get('opening_time')
        address = request.form.get('address')
        bewertung = request.form.get('bewertung')


        try:
            bewertung = int(bewertung)
            if bewertung < 1 or bewertung > 5:
                flash("Die Bewertung muss zwischen 1 und 5 liegen!", "danger")
                return redirect(url_for('hallen_hinzufuegen'))
        except ValueError:
            flash("Die Bewertung muss eine Zahl sein!", "danger")
            return redirect(url_for('hallen_hinzufuegen'))


        cnx, cursor = connect_to_database()
        if not cnx:
            flash("Fehler bei der Verbindung zur Datenbank.", "danger")
            return redirect(url_for('hallen_hinzufuegen'))

        try:
            query_insert = """
                INSERT INTO locations (name, image_url, opening_time, address, bewertung)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query_insert, (name, image_url, opening_time, address, bewertung))
            cnx.commit()
            halleId = cursor.lastrowid
            add_halle_to_hashmap(halleId, name, opening_time, address, image_url, bewertung)

            flash("Halle erfolgreich hinzugefügt!", "success")
            return redirect(url_for('hallen_hinzufuegen'))

        except Exception as e:
            flash(f"Ein Fehler ist aufgetreten: {e}", "danger")
        finally:
            cursor.close()
            cnx.close()

    return render_template('hallen_hinzufuegen.html')


# Registrierung-Seite
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')


        cnx, cursor = connect_to_database()
        if not cnx:
            flash("Fehler bei der Verbindung zur Datenbank.", "danger")
            return render_template('register.html')

        try:
            query = "SELECT * FROM users WHERE name = %s OR email = %s"
            cursor.execute(query, (username, email))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Benutzername oder E-Mail existieren bereits!", "danger")
            else:
                query_insert = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
                cursor.execute(query_insert, (username, email, password))
                cnx.commit()
                flash("Registrierung erfolgreich! Du kannst dich jetzt einloggen.", "success")
                return redirect(url_for('login'))

        except mysql.connector.Error as err:
            flash(f"Ein Fehler ist aufgetreten: {err}", "danger")
        finally:
            cursor.close()
            cnx.close()

    return render_template('register.html')


# Abmeldefunktion
@app.route('/logout')
def logout():
        return render_template('logout.html')

@app.route('/loggedin')
def loggedin():
        return render_template('loggedin.html')


if __name__ == '__main__':
    app.run(debug=True)
