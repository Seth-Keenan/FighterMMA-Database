import mysql.connector

def build_database(host, user, password, database_name):
    try:
        cnx = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password
        )
        
        print("here")

        cursor = cnx.cursor()
        
        # Create the database if it doesn't exist
        cursor.execute("CREATE DATABASE " + database_name)
        
        # Switch to the created database
        cursor.execute("USE " + database_name)
        
        cursor.close()
        cnx.close()
        
        print("Database " + database_name + " created successfully.")
        
    except mysql.connector.Error as err:
        print("Error:", err)

def populate_database(host, user, password, database_name):
    try:
        cnx = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=database_name
        )

        cursor = cnx.cursor()

        # Create table for Organizations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Organization (
                organization_id INT PRIMARY KEY AUTO_INCREMENT,
                organization_name VARCHAR(100) NOT NULL,
                country VARCHAR(100)
            )
        ''')

        # Create table for Events
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Event (
                event_id INT PRIMARY KEY AUTO_INCREMENT,
                event_name VARCHAR(100) NOT NULL,
                event_date DATE,
                organization_id INT,
                venue VARCHAR(200),
                city VARCHAR(100),
                country VARCHAR(100),
                FOREIGN KEY (organization_id) REFERENCES Organization(organization_id)
            )
        ''')

        # Create table for Referees
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Referee (
                referee_id INT PRIMARY KEY AUTO_INCREMENT,
                referee_name VARCHAR(100) NOT NULL,
                experience_years INT
            )
        ''')

        # Create table for Fighters
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Fighter (
                fighter_id INT PRIMARY KEY AUTO_INCREMENT,
                fighter_name VARCHAR(100) NOT NULL,
                weight_class VARCHAR(50),
                height DECIMAL(5,2),
                reach DECIMAL(5,2),
                record_win INT DEFAULT 0,
                record_loss INT DEFAULT 0,
                record_draw INT DEFAULT 0,
                win_percentage DECIMAL(5,2)
            )
        ''')

        # Create table for Fights
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Fight (
                fight_id INT PRIMARY KEY AUTO_INCREMENT,
                event_id INT,
                fighter1_id INT,
                fighter2_id INT,
                winner_id INT,
                referee_id INT,
                start_time DATETIME,
                end_time DATETIME,
                duration_minutes INT,
                result VARCHAR(50),
                FOREIGN KEY (event_id) REFERENCES Event(event_id),
                FOREIGN KEY (fighter1_id) REFERENCES Fighter(fighter_id),
                FOREIGN KEY (fighter2_id) REFERENCES Fighter(fighter_id),
                FOREIGN KEY (winner_id) REFERENCES Fighter(fighter_id),
                FOREIGN KEY (referee_id) REFERENCES Referee(referee_id)
            )
        ''')

        # Create table for Corner Teams
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS CornerTeam (
                team_id INT PRIMARY KEY AUTO_INCREMENT,
                team_name VARCHAR(100) NOT NULL
            )
        ''')

        # Create table for Fighter-Corner Team Relationship
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS FighterCornerTeam (
                fighter_id INT,
                team_id INT,
                PRIMARY KEY (fighter_id, team_id),
                FOREIGN KEY (fighter_id) REFERENCES Fighter(fighter_id),
                FOREIGN KEY (team_id) REFERENCES CornerTeam(team_id)
            )
        ''')

        cursor.execute('''
            INSERT INTO Organization (organization_name, country) 
            VALUES 
            ('UFC', 'USA'),
            ('Bellator', 'USA'),
            ('ONE Championship', 'Singapore')
        ''')

        # Insert synthetic data into the Event table
        cursor.execute('''
            INSERT INTO Event (event_name, event_date, organization_id, venue, city, country) 
            VALUES 
            ('UFC 1', '1993-11-12', 1, 'McNichols Sports Arena', 'Denver', 'USA'),
            ('Bellator 1', '2009-04-03', 2, 'Hollywood Seminole Hard Rock Hotel & Casino', 'Hollywood', 'USA'),
            ('ONE Championship: Enter the Dragon', '2019-05-17', 3, 'Singapore Indoor Stadium', 'Kallang', 'Singapore')
        ''')

        # Insert synthetic data into the Referee table
        cursor.execute('''
            INSERT INTO Referee (referee_name, experience_years) 
            VALUES 
            ('Herb Dean', 15),
            ('John McCarthy', 25),
            ('Marc Goddard', 10)
        ''')

        # Insert synthetic data into the Fighter table
        cursor.execute('''
            INSERT INTO Fighter (fighter_name, weight_class, height, reach, record_win, record_loss, record_draw, win_percentage) 
            VALUES 
            ('Conor McGregor', 'Lightweight', 1.75, 74, 22, 6, 0, 78.57),
            ('Jon Jones', 'Light Heavyweight', 1.93, 215, 26, 1, 0, 96.30),
            ('Amanda Nunes', 'Bantamweight', 1.73, 69, 21, 4, 0, 84.00)
        ''')

        # Insert synthetic data into the Fight table
        cursor.execute('''
            INSERT INTO Fight (event_id, fighter1_id, fighter2_id, winner_id, referee_id, start_time, end_time, duration_minutes, result) 
            VALUES 
            (1, 1, 2, 2, 1, '2021-01-23 20:00:00', '2021-01-23 20:15:00', 15, 'Jon Jones wins via TKO'),
            (2, 2, 3, 2, 2, '2021-02-15 19:30:00', '2021-02-15 19:40:00', 10, 'Jon Jones wins via submission'),
            (3, 3, 1, 3, 3, '2021-03-10 21:00:00', '2021-03-10 21:15:00', 15, 'Amanda Nunes wins via decision')
        ''')

        # Insert synthetic data into the CornerTeam table
        cursor.execute('''
            INSERT INTO CornerTeam (team_name) 
            VALUES 
            ('SBG Ireland'),
            ('Jackson Wink MMA'),
            ('American Top Team')
        ''')

        # Insert synthetic data into the FighterCornerTeam table
        cursor.execute('''
            INSERT INTO FighterCornerTeam (fighter_id, team_id) 
            VALUES 
            (1, 1),
            (2, 2),
            (3, 3)
        ''')
        
        print("Database populated successfully.")

    except mysql.connector.Error as err:
        print("Error:", err)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'cnx' in locals():
            cnx.commit()
            cnx.close()

def register_fighter_for_fight(fighter_id, fight_id, host, user, password, database_name):
    try:
        cnx = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=database_name
        )

        cursor = cnx.cursor()

        # Check if the fight exists
        cursor.execute("SELECT event_id FROM Fight WHERE fight_id = %s", (fight_id,))
        event_id = cursor.fetchone()

        if event_id:
            event_id = event_id[0]

            # Check if the fighter is already registered for the fight
            cursor.execute("SELECT * FROM Fight WHERE (fighter1_id = %s OR fighter2_id = %s) AND fight_id = %s", (fighter_id, fighter_id, fight_id))
            existing_registration = cursor.fetchone()

            if not existing_registration:
                # If the fighter is not registered, ask the user if they want to replace one of the fighters
                replace_fighter = input("Fighter is not registered for this fight. Do you want to replace one of the fighters? (yes/no): ")

                if replace_fighter.lower() == "yes":
                    fighter_to_replace = input("Enter the fighter ID you want to replace: ")
                    cursor.execute("UPDATE Fight SET fighter1_id = %s WHERE fight_id = %s OR fighter2_id = %s", (fighter_id, fight_id, fighter_to_replace))
                    cnx.commit()
                    print("Fighter successfully registered for the fight.")
                else:
                    print("Registration canceled.")

            else:
                print("Fighter is already registered for the fight.")

            # Display the Fight Information and Corresponding Event with EventID
            cursor.execute("SELECT * FROM Fight WHERE fight_id = %s", (fight_id,))
            fight_info = cursor.fetchone()
            print("Fight Information:")
            print(fight_info)
            print("Corresponding Event with EventID:", event_id)

        else:
            print("Fight does not exist.")

    except mysql.connector.Error as err:
        print("Error:", err)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'cnx' in locals():
            cnx.close()

def display_fighter_info(fighter_id, host, user, password, database_name):
    try:
        cnx = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=database_name
        )

        cursor = cnx.cursor()

        # Check if the fighter exists
        cursor.execute("SELECT * FROM Fighter WHERE fighter_id = %s", (fighter_id,))
        fighter_info = cursor.fetchone()

        if fighter_info:
            print("Fighter Information:")
            print(fighter_info)
        else:
            print("Fighter with ID {} does not exist.".format(fighter_id))

    except mysql.connector.Error as err:
        print("Error:", err)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'cnx' in locals():
            cnx.close()

def alter_fighter_wc(fighter_id, new_weight_class, host, user, password, database_name):
    try:
        cnx = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=database_name
        )

        cursor = cnx.cursor()

        # Check if the fighter exists
        cursor.execute("SELECT * FROM Fighter WHERE fighter_id = %s", (fighter_id,))
        fighter_info = cursor.fetchone()

        if fighter_info:
            # Update the fighter's weight class
            cursor.execute("UPDATE Fighter SET weight_class = %s WHERE fighter_id = %s", (new_weight_class, fighter_id))
            cnx.commit()
            print("Fighter's weight class updated successfully.")
        else:
            print("Fighter with ID {} does not exist.".format(fighter_id))

    except mysql.connector.Error as err:
        print("Error:", err)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'cnx' in locals():
            cnx.close()

def main():


    database_name = "Fighter"
    password = input("Insert password: ")
    host = "localhost"
    user = "root"

    build_database(host, user, password, database_name)
    populate_database(host, user, password, database_name)

    while True:
        print("1. Register Fighter for Fight")
        print("2. Display Fighter Information")
        print("3. Alter Fighter Weight class")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            valid_input = False
            while not valid_input:
                try:
                    fighter_id = int(input("Enter Fighter ID: "))
                    fight_id = int(input("Enter Fight ID: "))
                    register_fighter_for_fight(fighter_id, fight_id, host, user, password, database_name)
                    valid_input = True
                except ValueError:
                    print("Error: Invalid input. Please enter valid integer values for Fighter ID and Fight ID.")
        elif choice == '2':
            valid_input = False
            while not valid_input:
                try:
                    fighter_id = int(input("Enter Fighter ID: "))
                    display_fighter_info(fighter_id, host, user, password, database_name)
                    valid_input = True
                except ValueError:
                    print("Error: Invalid input. Please enter a valid integer value for Fighter ID.")
        elif choice == '3':
            valid_input = False
            while not valid_input:
                try:
                    fighter_id = int(input("Enter Fighter ID: "))
                    new_weight_class = input("Enter new weight class: ")
                    alter_fighter_wc(fighter_id, new_weight_class, host, user, password, database_name)
                    valid_input = True
                except ValueError:
                    print("Error: Invalid input. Please enter a valid integer value for Fighter ID.")
        elif choice == '4':
            print("Exiting the application...")
            break
        else:
            print("Error: Invalid choice. Please enter a number from 1 to 4.")

main()