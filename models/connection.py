import psycopg2
import uuid
import datetime
from utils.hash_passwords import hash_password


class DataBase:
    def __init__(self):
        """ initiate the connection with database and create the cursor which will be used to deal with database """
        try:
            self.__conn = psycopg2.connect(user="postgres",
                                  password="Ahmede2*",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="clinc_system")
            self.__cursor = self.__conn.cursor()
        except (Exception, psycopg2.Error) as e:
            print("the error is here ")
            print(f"The error is {e}")


    def create_element(self, table, dictionary):
        """ insert new elements in a specific table in database """
        try:
            allowed_attributes = [
                    'user_name',
                    'password',
                    'phone_number',
                    'first_name',
                    'last_name',
                    'country_code',
                    'result_date',
                    'selected_lab_test',
                    'result_type',
                    'file_path',
                    'status',
                    'doctor_admin_id',
                    'patient_id',
                    'file_id',
                    'role',
                    'session_id',
                    'conversation_id',
                    'image_path',
                    'text',
                    'respond'
            ]
            
            if table != 'file' and table != 'session':
                dictionary[f'{table}_id'] = str(uuid.uuid4())
            if 'password' in dictionary:
                dictionary['password'] = hash_password(dictionary['password'])

            count = 0
            columns = ""
            values = ""
            new_dictionary = {}

            for key in dictionary:
                if key in allowed_attributes:
                    new_dictionary[key] = dictionary[key]

            length = len(new_dictionary)


            for key, value in new_dictionary.items():
                if key in allowed_attributes:
                    columns += key
                    values += f"'{value}'"
                    if count + 1 < length:
                        columns += ", "
                        values += ", "
                count += 1


            sql_statment = f"""insert into {table}  ({columns}) values ({values})"""
            self.__cursor.execute(sql_statment)

            if self.__cursor.rowcount > 0:

                return "The element is added"

        except (Exception, psycopg2.Error) as e:
            print(f"The error is {e}")

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

            self.__cursor.execute(sql_statment)

            if self.__cursor.rowcount > 0:

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
            self.__cursor.execute(sql_statment)
            
            data = self.__cursor.fetchall()

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
            self.__cursor.execute(sql_statment)

            if self.__cursor.rowcount > 0:
                return "the element is successfully deleted "

        except (Exception, psycopg2.Error) as e:
            print(f"The error is {e}")

        return None


    def get_all_elements(self, table):
        """ get all elements of a specific table """
        try:
            sql_statment = f""" select * from {table} """
            
            self.__cursor.execute(sql_statment)
            data = self.__cursor.fetchall()
            
            if len(data) != 0:
                return data

        except (Exception, psycopg2.Error) as e:
            print(f"The error is {e}")

        return None


    def save_changes(self):
        """ commit all the changes """
        self.__conn.commit()


    def close_connection(self):
        """ close the the cursor and the connection """
        if (self.__conn):
            self.__cursor.close()
            self.__conn.close()

obj = DataBase()
