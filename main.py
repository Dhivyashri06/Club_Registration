import psycopg2
from psycopg2 import sql
from colorama import Fore, init
import re

init(autoreset=True)

#Connect to the postgres DB
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="spotify",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(Fore.RED + f"[!] DB connection failed: {e}")
        exit(1)

#Input validation
def is_valid_name(name):
    return bool(re.fullmatch(r"[A-Za-z ]+", name))

def is_valid_roll(roll):
    return bool(re.fullmatch(r"[A-Za-z0-9]+", roll))

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.fullmatch(pattern, email))

def is_valid_batch(batch):
    return bool(re.fullmatch(r"[0-9-]+", batch))

def is_valid_year(year):
    return 1 <= year <= 5

#Display clubs
def show_clubs(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name, description FROM clubs ORDER BY id;")
    clubs = cur.fetchall()
    print(Fore.CYAN + "\nAvailable Clubs:\n")
    for club in clubs:
        print(f"{club[0]}. {club[1]} - {club[2]}")
    cur.close()
    return clubs

#Display quiz
def take_quiz(conn, club_id):
    cur = conn.cursor()
    cur.execute(
        "SELECT question, option_a, option_b, correct_option FROM questions WHERE club_id = %s ORDER BY id;",
        (club_id,)
    )
    questions = cur.fetchall()
    cur.close()

    score = 0
    print(Fore.MAGENTA + f"\nStarting Quiz for Club ID {club_id}...\n")
    for q in questions:
        print(Fore.YELLOW + f"Q: {q[0]}")
        print(f"a) {q[1]}")
        print(f"b) {q[2]}")
        ans = input("Enter your answer (a/b): ").strip().lower()
        if ans == q[3].lower():
            score += 1

    print(Fore.GREEN + f"\nYou scored {score}/{len(questions)}")
    return score >= 3  # Pass if 3 or more correct

#Register
def register_student(conn, club_id):
    print(Fore.CYAN + "\nEnter your details to register:")
    
    while True:
        name = input("Name: ").strip()
        if is_valid_name(name):
            break
        print(Fore.RED + "Invalid name. Use alphabets only.")

    while True:
        roll = input("Roll Number: ").strip()
        if is_valid_roll(roll):
            break
        print(Fore.RED + "Invalid roll number.")

    course = input("Course: ").strip()

    while True:
        email = input("Email: ").strip()
        if is_valid_email(email):
            break
        print(Fore.RED + "Invalid email.")

    while True:
        batch = input("Batch: ").strip()
        if is_valid_batch(batch):
            break
        print(Fore.RED + "Invalid batch.")

    while True:
        try:
            year = int(input("Current Year (1-5): ").strip())
            if is_valid_year(year):
                break
            else:
                print(Fore.RED + "Year must be between 1-5")
        except ValueError:
            print(Fore.RED + "Enter numeric year.")

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, roll_no, course, email, batch, year, club_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (name, roll, course, email, batch, year, club_id)
    )
    conn.commit()
    cur.close()
    print(Fore.GREEN + "\nRegistration successful!")

def main():
    conn = connect_db()
    while True:
        clubs = show_clubs(conn)
        try:
            club_choice = int(input("\nEnter the club ID you want to join: ").strip())
        except ValueError:
            print(Fore.RED + "Enter a valid number!")
            continue

        if not any(c[0] == club_choice for c in clubs):
            print(Fore.RED + "Invalid club ID!")
            continue

        passed = take_quiz(conn, club_choice)
        if passed:
            print(Fore.GREEN + "\nCongratulations! You passed the quiz.")
            register_student(conn, club_choice)
        else:
            print(Fore.RED + "\nSorry, you did not pass the quiz.")

        cont = input("\nDo you want to continue? (y/n): ").strip().lower()
        if cont != 'y':
            break

    conn.close()
    print(Fore.CYAN + "Goodbye!")

if __name__ == "__main__":
    main()
