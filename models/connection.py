import psycopg2
import uuid
import datetime
from utils.hash_passwords import hash_password
from models.parameters import database_user, database_password, database_host, database_port, database_name



conn = psycopg2.connect(
                user=database_user,
                password=database_password,
                host=database_host,
                port=database_port,
                database=database_name
        )
cursor = conn.cursor()


class DataBase:
    
    def initialize_password_id(fun):

        def function(self, table):
            
            if table != 'file' and table != 'session':
                setattr(self, f"{table}_id", str(uuid.uuid4()))
                print(self.__dict__)

            if 'password' in self.__dict__:
                self.password = hash_password(self.password)
            
            return fun(self, table)

        return function


    @initialize_password_id
    def create_element(self, table):
        """ insert new elements in a specific table in database """
        #try:

        columns = ""
        values = ""
        count = 0
        length = len(self.__dict__)

            
        for key, value in self.__dict__.items():
            columns += key
            values += f"'{value}'"
            if count + 1 < length:
                columns += ", "
                values += ", "
            count += 1


        sql_statment = f"""insert into {table}  ({columns}) values ({values})"""
        cursor.execute(sql_statment)

        if cursor.rowcount > 0:

            return "The element is added"

        #except (Exception, psycopg2.Error) as e:
            #print(f"The error is {e}")

        return None

    def update_element(self, table, Dictionary, modifier):
        """ update values of a specific element """
        try:

            if modifier[0] == 'id':
                modifier[0] = f'{table}_id'
            allowed_attributes = [
                    'user_name', 
                    'password', 
                    'phone_number', 
                    'first_name', 
                    'last_name',
                    'country_code',
                    'result_date',
                    'file_path',
                    'status',
                    'image_path',
                    'text',
                    'respond'
            ]
            count = 0
            attributes = ""
            new_dictionary = {}

            if 'password' in Dictionary:
                Dictionary['password'] = hash_password(Dictionary['password'])

            for key in Dictionary:
                if key in allowed_attributes:
                    new_dictionary[key] = Dictionary[key]

            length = len(new_dictionary)

            for key, value in new_dictionary.items():
                attributes += f"{key} = '{value}'"
                if count + 1 < length:
                    attributes += ", "
                count += 1
            

            sql_statment = f"""update {table} set {attributes} where {modifier[0]} = '{modifier[1]}'"""

            cursor.execute(sql_statment)

            if cursor.rowcount > 0:

                return "the element is successfully updated """

        except (Exception, psycopg2.Error) as e:
            print(f"The error is {e}")
        
        return None


    def get_element(self, table, modifiers):
        """ get a specific element with its modifier """
        try:
            statment = ""
            count = 0
            length = len(modifiers)

            for element in modifiers:
                
                if element[0] == 'id':
                    element[0] = f'{table}_id'

                statment += f"{element[0]} = '{element[1]}' "

                if count + 1 < length:
                    statment += "and "
                count += 1


            sql_statment = f""" select * from {table} where {statment} """
            cursor.execute(sql_statment)
            
            data = cursor.fetchall()

            if len(data) != 0:
                return data

        except (Exception, psycopg2.Error) as e:
            print(f"The error is {e}")

        return None


    def delete_element(self, table, modifier):
        """ delete a specific element with its modifier """
        try:
            if modifier[0] == 'id':
                modifier[0] = f'{table}_id'

            sql_statment = f""" delete from {table} where {modifier[0]} = '{modifier[1]}' """
            cursor.execute(sql_statment)

            if cursor.rowcount > 0:
                return "the element is successfully deleted "

        except (Exception, psycopg2.Error) as e:
            print(f"The error is {e}")

        return None


    def get_all_elements(self, table):
        """ get all elements of a specific table """
        try:
            sql_statment = f""" select * from {table} """
            
            cursor.execute(sql_statment)
            data = cursor.fetchall()
            
            if len(data) != 0:
                return data

        except (Exception, psycopg2.Error) as e:
            print(f"The error is {e}")

        return None


    def save_changes(self):
        """ commit all the changes """
        conn.commit()


    def close_connection(self):
        """ close the the cursor and the connection """
        if (conn):
            cursor.close()
            conn.close()

obj = DataBase()
