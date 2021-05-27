import os
from typing import final
from werkzeug.utils import secure_filename
from os.path import join, isfile, islink
from screen1_backend_functions import read_specific_file, remove_files, write_file

PATH = os.getcwd()
UPLOAD_FOLDER = os.path.join(PATH, 'uploads')
PRE_PROCESSED_FOLDER = os.path.join(PATH, 'pre_processed')
REMOVED_QUERY_FOLDER = os.path.join(PATH, 'removed_queries')
ALTER_COMMENT_FOLDER = os.path.join(PATH, 'alter_comment_queries')


def alter_comment_query_only(query_type,single_query):
    '''
    Keeping the ALTER and COMMENT queries seperate from main script as there is no much changes 
    from ORACLE to SNOWFLAKE for those queries.
    '''
    # query_split = single_query.split(" ")
    result=""
    # if str(query_split[0]).lower() == 'alter' or str(query_split[0]).lower() == 'comment':
    if query_type.lower() == 'alter' or query_type.lower() == 'comment':        
        if single_query!="":
            file_save_path = os.path.join(ALTER_COMMENT_FOLDER, "alter_comment_oracle_queries.txt")
            text_file = open(file_save_path, "a")
            text_file.write(single_query+";\n")
            text_file.close()
    else:
        result = single_query
    return result

def remove_check_constraint(query_type, single_query):
    '''
    Removing the Check constraint Alter quueries for ORACLE, as those are not defined in SNOWFLAKE.
    '''
    new_query=""
    deleted_check_constraint_queries=""
    if query_type.lower() == 'create':   # for check constraint in CREATE queries
        # split using comma 
        split_query = []
        splitted_query = single_query.split(",")
        for i in splitted_query:   #here i is each constraint add in query
            #print()
            s = i.split()
            # print("list of spilit",s)
            if "check" in s or "CHECK" in s:
                deleted_check_constraint_queries=deleted_check_constraint_queries+i
                new_query=""
            else:
                # print("else",i)
                split_query.append(i)
        new_query= ",".join(split_query)

    else:               # for check constraint in ALTER queries
        s = single_query.split()
        #print("list of spilit",s)
        if "check" in s or "CHECK" in s:
            deleted_check_constraint_queries=deleted_check_constraint_queries+single_query
            new_query=""
        else:
            #print("else")
            new_query=single_query
    # write_file(PATH, deleted_check_constraint_queries, "removed_check_constraint_queries.txt")
    
    file_save_path = os.path.join(REMOVED_QUERY_FOLDER, "removed_check_constraint_queries.txt")
    text_file = open(file_save_path, "a")
    text_file.write(deleted_check_constraint_queries)
    text_file.close()
  
    return new_query

def remove_index(single_query):
    new_query=""
    removed_index_queries=""
    s = single_query.split()
    # print("list of INDEX split"," ".join(s[:2]))
    first_two_words=" ".join(s[:2])
    first_three_words=" ".join(s[:3])
    if first_two_words == "CREATE INDEX" or first_three_words == "CREATE UNIQUE INDEX" :
        removed_index_queries=removed_index_queries+single_query
        new_query=""
    else:
        # print("else")
        new_query=single_query
    
    file_save_path = os.path.join(REMOVED_QUERY_FOLDER, "removed_index_queries.txt")
    text_file = open(file_save_path, "a")
    text_file.write(removed_index_queries)
    text_file.close()
  
    return new_query    

def oracle_preprocessing(DIRECTORY):

    # Make directory if foldes  not exists and removing it before creating new.
    if not os.path.isdir(PRE_PROCESSED_FOLDER):
        os.mkdir(PRE_PROCESSED_FOLDER)
    else:
        remove_files(PRE_PROCESSED_FOLDER)

    if not os.path.isdir(REMOVED_QUERY_FOLDER):
        os.mkdir(REMOVED_QUERY_FOLDER)
    else:
        remove_files(REMOVED_QUERY_FOLDER)
        
    if not os.path.isdir(ALTER_COMMENT_FOLDER):
        os.mkdir(ALTER_COMMENT_FOLDER)
    else:
        remove_files(ALTER_COMMENT_FOLDER)
    
    result=""

    for file in os.listdir(DIRECTORY):          #looping Files in a directory
        filename = os.path.join(DIRECTORY, file)
        file_opened=open(filename,"r")
        file_read = file_opened.read()
        q=''
        q = q + file_read
        # print("q\n",q)
        file_opened.close()
        q_split = q.split(";")
        final_query_list=[]
        
        for query in q_split:                   # looping single query in that file
            # for each single query pre- processing for oracle database
            # print("single query",type(query),query)
            
            # Cleaning query
            query_cleaned = query.lstrip().rstrip()
            # query_cleaned = query_cleaned.replace("\n","")
            print("before",query_cleaned)
            query_cleaned = query_cleaned.replace("LOGGING","")
            print("after",query_cleaned)
            
            # calculating "query_type" to pass to later functions
            query_split= query_cleaned.split()
            query_type=""
            if query_cleaned!="":
                if query_split[0].upper()=='CREATE':
                    query_type = 'CREATE'
                elif query_split[0].upper()=='ALTER':
                    query_type = 'ALTER'
                elif query_split[0].upper()=='COMMENT':
                    query_type = 'COMMENT'
                else:
                    pass
            else:
                pass        
            # print("query_type\n",query_type)
            processed_query1 = remove_check_constraint(query_type, query_cleaned)
            processed_query2 = remove_index(processed_query1)
            
            # saving alter and comment files seperateley in folder and returning rest queries.
            updated_query= alter_comment_query_only(query_type,processed_query2)
            # print("updated_query\n",updated_query)
            
            if updated_query!="":
                final_query_list.append(updated_query+";")
                print("updated_query",updated_query)
            # else:
            #     final_query_list.append("")
            #     print("final_query_list_else",updated_query)
        new_query=""
        if len(final_query_list)!=0:
            #print("final_query_list",final_query_list)
            new_query="".join(final_query_list)
            print("final_query",new_query)
            # Saving the processed file in seperate folder
            file_save_path = os.path.join(PRE_PROCESSED_FOLDER, file)
            text_file = open(file_save_path, "w")
            text_file.write(new_query)
            text_file.close()
            result = "All query saved on lan"
        else:
            print("list if blank")

    return result

def replace_name_alter_comment_queries(changes):
    '''
    Replace component names in files in "Alter_comment_queries" folder as per changes made by user in front end 
    
    '''
    q=""
    DIRECTORY = ALTER_COMMENT_FOLDER
    filename = os.path.join(DIRECTORY,"alter_comment_oracle_queries.txt")
    
    # reading alter comments files in this folder.
    if len(os.listdir(DIRECTORY))!=0:          #looping Files in a directory
        file_opened=open(filename,"r")
        file_read = file_opened.read()
        q = q + file_read
        print("q\n",q)
        file_opened.close()
    query_cleaned = q.lstrip().rstrip()
    q_split = query_cleaned.split(";")
    
    old_names = changes['old_table']
    new_names = changes['new_change_table']
    new_query = ""
    final_query_list=[]
    
    for query in q_split:
        if query!="" and len(old_names)!=0 and len(new_names)!=0:
            for i in old_names:
                old_ind = old_names.index(i)
                print("q",query)
                new_query = query.replace(i,new_names[old_ind],1)
        else:
            new_query=query
        final_query_list.append(new_query)
        # print("final_query_list",final_query_list)

    if len(final_query_list)!=0:
        updated_query=";\n".join(final_query_list)
        print("updated_query",updated_query)
        file_save_path = os.path.join(ALTER_COMMENT_FOLDER, filename)
        text_file = open(file_save_path, "w")
        text_file.write(updated_query)
        text_file.close()
    else:
        print("list if blank")

    print("new_replaced_query",updated_query)
    return updated_query


    
# query='''CREATE TABLE EMPLOYEES 
#     (      EMPLOYEE_ID NUMBER (6)  NOT NULL , 
#      FIRST_NAME VARCHAR2 (20 BYTE) , 
#      LAST_NAME VARCHAR2 (25 BYTE)  NOT NULL , 
#      EMAIL VARCHAR2 (25 BYTE)  NOT NULL , 
#      PHONE_NUMBER VARCHAR2 (20 BYTE) , 
#      HIRE_DATE DATE  NOT NULL , 
#      JOB_ID VARCHAR2 (10 BYTE)  NOT NULL , 
#      SALARY NUMBER (8,2) , 
#      COMMISSION_PCT NUMBER (2,2) , 
#      MANAGER_ID NUMBER (6) , 
#      DEPARTMENT_ID NUMBER (4), CONSTRAINT EMP_EMP_ID_PK PRIMARY KEY ( EMPLOYEE_ID ) ,
#       CONSTRAINT EMP_EMP_ID_PK check sale>0 ( EMPLOYEE_ID ) ,
# CONSTRAINT EMP_EMAIL_UK UNIQUE ( EMAIL ), 
# CONSTRAINT EMP_SALARY_MIN 
#     CHECK ( salary > 0) ,
# CONSTRAINT EMP_DEPT_FK FOREIGN KEY 
#     ( 
#      DEPARTMENT_ID
#     ) 
#     REFERENCES DEPARTMENTS 
#     ( 
#      DEPARTMENT_ID
#     ) 
#     NOT DEFERRABLE  ,
# CONSTRAINT EMP_MANAGER_FK FOREIGN KEY 
#     ( 
#      MANAGER_ID
#     ) 
#     REFERENCES EMPLOYEES 
#     ( 
#      EMPLOYEE_ID
#     ) 
#     NOT DEFERRABLE 
#     '''
    
# def ext(quer,ph,sc):
#     ext_dat=extract_tables(quer,'ALTER',sc)
#     ph.append(ext_dat)
#     print(ph)
#     return ext_dat  

# tab=[]
# ip=ext(query,tab,t)
# query = '''
# CREATE TABLE COUNTRIES 
#     ( 
#      COUNTRY_ID CHAR (2 BYTE)  NOT NULL , 
#      COUNTRY_NAME VARCHAR2 (40 BYTE) , 
#      REGION_ID NUMBER 
#     ) LOGGING 
# ;
# '''
query2='''
COMMENT ON COLUMN COUNTRIES.COUNTRY_ID IS 'Primary key of countries table.' 
;
'''
changes =  {'old_table': ['COUNTRIES'], 'new_change_table': ['COUNTRY'], 'old_view': [], 'new_change_view': [], 'old_schema': [], 'new_schema': [], 'old_database': [], 'new_change_db': [], 'removed_table': [], 'removed_view': [], 'removed_database': [], 'removed_schema': []}
# alter_comment_query_only(query2)
#oracle_preprocessing(UPLOAD_FOLDER)

# replace_name_alter_comment_queries(changes)
