# Chama-Management-System

This is a simple Chama Management System that aims to transform the pen and paper operations of traditional Chamas with an easy to use interface. 

The web application is built using;-
1. Python.
2. Django.
3. Bootstrap5.
4. Sqlite3, but you can easily change to MySQL, PostgreSQL, etc...

### Features
1. Members Records Management. 
2. Saving Records Management.
3. Meri-Go Round Management and Payments Collection Management.
4. Loans Application, Issuing and Repayment Management.

### Upcoming Features
1. Savings and Payments Collection via Mpesa or Bank.


### How to Run
Disclaimer: Create a folder somewhere in your computer, then using your terminal/command prompt change directory into that folder

for example;
```sql 
cd Desktop
```
Then 
```sql
mkdir ChamaApp
```

Then 
```sql
cd ChamaApp
```

Then while inside the folder, perform the following actions.

Befor you clone the repository, make sure you have Python installed on your computer,
Then create a virtual environment using the following command;-
```sql
python3 -m venv chamaenv
```

Activate the virtual environment using 
```sql 
source chamaenv/bin/activate
```

1. Clone the repository using the commands below;-
```sql
    git clone git@github.com:ndambopaul/Chama-Management-System.git
```
or
```sql
    git clone https://github.com/ndambopaul/Chama-Management-System.git
```

2. Change into the directory
```sql
cd Chama-Management-System
```

3. Install Dependencies
```sql
pip install -r requirements.txt
```

4. Start the server
```sql
python manage.py runserver
```