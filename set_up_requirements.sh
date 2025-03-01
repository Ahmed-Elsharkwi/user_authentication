sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl restart postgresql@12-main.service
sudo systemctl enable postgresql
sudo systemctl start postgresql

#set up database
SQL_FILE="set_up_database.sql"
if [ -f "$SQL_FILE" ]; then
   sudo -u postgres psql -f $SQL_FILE
else
    echo "SQL file not found: $SQL_FILE"
fi

#set up requirements
sudo apt install python3-pip
pip install -r requirements.txt
