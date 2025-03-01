sudo apt update
sudo apt install -y gcc make libreadline-dev zlib1g-dev wget
wget https://ftp.postgresql.org/pub/source/v9.6.24/postgresql-9.6.24.tar.gz
tar -xvzf postgresql-9.6.24.tar.gz
cd postgresql-9.6.24
./configure --prefix=/usr/local/pgsql9.6
make -j$(nproc)
sudo make install
sudo useradd -m -d /usr/local/pgsql9.6 postgres
sudo passwd Ahmede2*
sudo mkdir /usr/local/pgsql9.6/data
sudo chown postgres:postgres /usr/local/pgsql9.6/data
sudo systemctl daemon-reload
sudo systemctl enable postgresql9.6
sudo systemctl start postgresql9.6

#set up database
SQL_FILE="setup_mysql_dev.sql"
if [ -f "$SQL_FILE" ]; then
    sudo mysql -u root -p'root' < "$SQL_FILE"
else
    echo "SQL file not found: $SQL_FILE"
fi

#set up requirements
sudo apt install python3-pip
pip install -r requirements.txt
