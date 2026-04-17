from flask import Flask, render_template, request
import psycopg2
 
app = Flask(__name__)
 
# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        port=os.environ.get('DB_PORT')
    )
    return conn
 
@app.route('/movies', methods=['GET', 'POST'])
def movies():
    conn = get_db_connection()
    cur = conn.cursor()
 
    search = request.form.get('title')
 
    if search:
        cur.execute("""
            SELECT * FROM Movies
            WHERE title ILIKE %s
        """, ('%' + search + '%',))
    else:
        cur.execute("""
            SELECT * FROM Movies
        """)
 
    movies = cur.fetchall()
 
    cur.close()
    conn.close()
 
    return render_template('movies.html', movies=movies, search=search)
 
@app.route('/', methods=['GET', 'POST'])
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor()
 
    total_movies = cur.execute("SELECT COUNT(*) FROM Movies")
    total_movies = cur.fetchone()[0]
 
    total_showings = cur.execute("SELECT COUNT(*) FROM showing WHERE date BETWEEN '2024-05-01' AND '2024-05-31'")
    total_showings = cur.fetchone()[0]
 
    cur.execute("""
                SELECT * FROM showing WHERE date BETWEEN '2024-05-01' AND '2024-05-31'
            """)
 
    movies = cur.fetchall()
 
    total_tickets = cur.execute("SELECT COUNT(*) FROM ticket")
    total_tickets = cur.fetchone()[0]
    cur.close()
    conn.close()
    return render_template('dashboard.html', total_movies=total_movies, total_showings=total_showings, total_tickets=total_tickets, movies=movies)
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
