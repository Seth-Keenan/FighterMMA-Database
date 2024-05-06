# FighterMMA-Database
This Python script is designed to interact with a MySQL database containing tables related to an MMA fighting scenario. It allows users to register fighters for specific fights, check if fighters are already registered for a fight, and replace fighters if necessary.

#Prerequisites:
Python installed on your machine (version 3 or higher)
MySQL server installed and running
MySQL Connector/Python library installed (pip install mysql-connector-python)
Instructions:

#Database Setup:
Ensure MySQL server is running.
Execute the provided SQL script to create the necessary database and tables. You can do this using a MySQL client like MySQL Workbench or through command-line tools like mysql or mysqlsh.

#Install Dependencies:
Install the MySQL Connector/Python library if you haven't already. Run pip install mysql-connector-python in your terminal or command prompt.

#Configuration:
Update the MySQL connection details in the Python script (host, user, passwd) to match your MySQL server setup.

#Running the Script:
Run the Python script (mma_fighter_registration.py).
Enter the Fighter ID and Fight ID when prompted.
Follow the on-screen instructions to register fighters for fights.

#Usage Examples:
#Example 1: Registering a Fighter for a Fight
Enter Fighter ID: 1
Enter Fight ID: 2
Fighter is not registered for this fight. Do you want to replace one of the fighters? (yes/no): yes
Enter the fighter ID you want to replace: 3
Fighter successfully registered for the fight.

#Example 2: Trying to Register an Already Registered Fighter
Enter Fighter ID: 2
Enter Fight ID: 3
Fighter is already registered for the fight.

#Example 3: Providing Invalid Inputs
Enter Fighter ID: abc
Error: Invalid input. Please enter valid integer values for Fighter ID and Fight ID.

#Notes:
Ensure the MySQL server is running and accessible from the host specified in the script.
Make sure to provide valid integer inputs for Fighter ID and Fight ID.
Follow proper MySQL security practices, such as not hardcoding passwords in scripts and restricting database user permissions appropriately.
