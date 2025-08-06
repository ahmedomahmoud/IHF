import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def get_db_connection():
    """Establishes a connection to the PostgreSQL database using environment variables."""
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS')
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error connecting to the database: {e}")
        return None

# --- The rest of your functions (create_tables, add_championship, etc.) remain exactly the same ---
# They will just use the new get_db_connection() function.

def create_tables():
    """Creates database tables by executing the schema.sql file."""
    conn = get_db_connection()
    if conn is None:
        return
        
    try:
        with conn.cursor() as cur:
            with open('schema.sql', 'r') as f:
                cur.execute(f.read())
        conn.commit()
        print("Tables created successfully!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error creating tables: {error}")
    finally:
        if conn is not None:
            conn.close()

def add_championship(name, description, start_date, end_date):
    """Adds a new championship to the championships table."""
    sql = """INSERT INTO championships(name, description, start_date, end_date)
             VALUES(%s, %s, %s, %s) RETURNING id;"""
    conn = get_db_connection()
    championship_id = None
    if conn is None:
        return
        
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (name, description, start_date, end_date))
            championship_id = cur.fetchone()[0]
            conn.commit()
            print(f"Successfully added championship '{name}' with ID: {championship_id}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error adding championship: {error}")
    finally:
        if conn is not None:
            conn.close()
    return championship_id

def get_championships():
    """Retrieves all championships from the database."""
    conn = get_db_connection()
    if conn is None:
        return []
        
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, start_date, end_date FROM championships;")
            champs = cur.fetchall()
            return champs
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error fetching championships: {error}")
        return []
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    # This block will be executed when the script is run directly
    
    # 1. Create the tables
    print("Initializing database schema...")
    create_tables()
    
    # 2. Example: Add a new championship
    print("\nAdding a new championship...")
    add_championship(
        'World Handball Championship 2025',
        'The 29th edition of the championship.',
        '2025-01-14',
        '2025-02-02'
    )
    
    # 3. Example: Retrieve and print all championships
    print("\nFetching all championships from the database:")
    all_champs = get_championships()
    for champ in all_champs:
        print(f"ID: {champ[0]}, Name: {champ[1]}, Start: {champ[2]}, End: {champ[3]}")