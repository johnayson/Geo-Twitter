import sqlite3
from sqlite3 import Error
import glob 
import json
import os


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn

 
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    print("createproj")
    #sql = "INSERT INTO `projects` VALUES(1,'Cool App with SQLite & Python', '2015-01-01', '2015-01-30'); "
    sql = """ INSERT INTO `projects`(name,begin_date,end_date)
              VALUES(?,?,?) """
    
    cur = conn.cursor()
    #count = cur.execute(sql)
    cur.execute(sql,project)
    conn.commit()#persist the data
    print("Record inserted successfully into projects  table ", cur.rowcount)
    return cur.lastrowid

def insert_tweets(conn,row):
    sql = """ INSERT OR IGNORE INTO `geo_tweets`(tweet_id, text, created_at, location, coordinate_x, coordinate_y)
              VALUES(?,?,?,?,?,?) """ 
    cur = conn.cursor()
    cur.execute(sql,row)
    conn.commit()
    print("Record inserted successfully into tweets table", cur.rowcount)
    return cur.lastrowid

def refine(name):
        with open(name) as data_file:
                print(name)
                data = json.load(data_file)
                print(data)
        for keys in data:
                data[keys]['text'] = clean_tweets(data[keys]['text'])
        print(data)
        dict_to_json(data,os.path.basename(name))
        return True


def main():
    with open('/Users/~/Desktop/projects/data_eng/geo_twitter/config/config.json') as data_file:
          data = json.load(data_file)
    print(data)
    os.chdir(data['TWITTER_DIR'])
    database = "tweets.db" 
    #database = r"C:\sqlite\db\pythonsqlite.db"
    sql_create_tweets_table = """ CREATE TABLE IF NOT EXISTS geo_tweets (
                                        tweet_id integer PRIMARY KEY,
                                        text text NOT NULL,
                                        created_at text NOT NULL,
                                        location text NOT NULL,
                                        coordinate_x DECIMAL(3,8) NOT NULL,
					coordinate_y DECIMAL(3,8) NOT NULL
                                    ); """
 
 
    # create a database connection
    conn = create_connection(database)
    print(conn) 
    # create tables
    if conn is not None:
        create_table(conn, sql_create_tweets_table)
    
        files = glob.glob('files/ref*.json')
        for file in files:
            with open(file) as data_file:
                data = json.load(data_file)
            for key in data:
                print(key)
                tweet = ( data[key]['tweet_id'] ,data[key]['text'] , data[key]['created_at'] , data[key]['location'], data[key]['coordinate_x'], data[key]['coordinate_y'])
                print(tweet)
                x = insert_tweets(conn,tweet)
            mv_cmd = 'mv ' + file + ' ' + file + '.done'
            os.system(mv_cmd)
        
 
        #create tweets table
        create_table(conn, sql_create_tweets_table)
 
        # create tasks table
        #create_table(conn, sql_create_tasks_table)

        #project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
        #project_id = create_project(conn, project)
    else:
        print("Error! cannot create the database connection.")
main() 
#if __name__ == '__main__':
#   create_connection(r"C:\sqlite\db\pythonsqlite.db")
