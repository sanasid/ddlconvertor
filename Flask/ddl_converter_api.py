# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 12:58:28 2021

@author: aaina.c
"""

from oracle_exceptional import ALTER_COMMENT_FOLDER, oracle_preprocessing
import os
import shutil
import json
from flask import Flask, request
from werkzeug.utils import secure_filename
from flask_cors import CORS
import glob
import re
from os.path import join, isfile, islink
import shutil

from screen1_backend_functions import read_specific_file, remove_files, write_file
from screen2_backend_functions import get_tables_all, audit_columns_query
from screen3_backend_functions import query_parser_folder, query_separator_folder, dict_format, final_change_pair, change_diff, query_replacement
from screen4_backend_functions import filename, filename_key, rename_files, conversion, final_query_form
from oracle_exceptional import replace_name_alter_comment_queries

APP = Flask(__name__)
APP.secret_key = "12345"
CORS(APP)

########### SCREEEN 1 #############
# Get current path
PATH = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(PATH, 'uploads')
JSON_FOLDER = os.path.join(PATH, 'json')
JSON_SAVE_FOLDER = os.path.join(PATH, 'kv_match_json')

# Allowed extension you can set your own
ALLOWED_EXTENSIONS = {'txt', 'sql'}
ALLOWED_IN_DB = {'Hive', 'Oracle', 'Teradata'}
ALLOWED_OUT_DB = {'Snowflake'}

select_output=""
select_input=""

def allowed_file(filename):
    '''
        DOCSTRING : Checks if filename extension is allowed.
        -----
    '''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_input(input_db):
    '''
        DOCSTRING : Checks if input database is allowed.
        -----
    '''
    return input_db in ALLOWED_IN_DB

def allowed_output(output_db):
    '''
        DOCSTRING : Checks if output database is allowed.
        -----
    '''
    return output_db in ALLOWED_OUT_DB


@APP.route("/screen1", methods=['POST'])
def next_screen1():
    '''
        DOCSTRING : Returns "Success" if all 3 functions of screen 1 below are working correctly.
        -----
    '''
    upload_out = json.loads(upload_file())
    print(upload_out)
    dialog_out = json.loads(copy_paste_dialogbox())
    print(dialog_out)
    kv_out = json.loads(kv_match())
    print(kv_out)
    remove_files(ALTER_QUERY_FOLDER)

    if kv_out["status"] == "Success_1" and (upload_out["status"] == "Success_2" or dialog_out["status"] == "Success_3"):
        return json.dumps({
            "status" :"Success",
            "kv_match"              : kv_out,
            "upload_file"           : upload_out,
            "copy_paste_dialogbox"  : dialog_out
            }, indent=4)
    else:
        return json.dumps({
            "status":"Failure",
            "error" :{
                "statement"             :"Check if keys for both INPUT and OUTPUT DB and either 'files' or 'text' KEY are entered",
                "kv_match"              : kv_out,
                "upload_file"           : upload_out,
                "copy_paste_dialogbox"  : dialog_out
                }
            }, indent=4)


@APP.route('/kv_match', methods=['POST'])
def kv_match():
    '''
        DOCSTRING : Returns a json output containing json file and status as 'Success_1'
                    if the function is working correctly.
        -----
    '''
    if not os.path.isdir(JSON_SAVE_FOLDER):
        os.mkdir(JSON_SAVE_FOLDER)
    else:
        remove_files(JSON_SAVE_FOLDER)


    if 'input_database' not in request.form or 'output_database' not in request.form:
        return json.dumps({
            "status":"Failure",
            "error" :"Please enter KEY for both INPUT and OUTPUT DB"
            }, indent=4)
    
    global select_input
    global select_output

    select_input = request.form.get("input_database")
    select_output = request.form.get("output_database")
    if (select_input and allowed_input(select_input)) and (select_output and allowed_output(select_output)):
        if select_input == "Hive" and select_output == "Snowflake":
            json_file = os.path.join(JSON_FOLDER, "hive_to_snowflake.json")
            shutil.copy(json_file, JSON_SAVE_FOLDER)
            return json.dumps({
                "status" :"Success_1"
                }, indent=4)
        elif select_input == "Oracle" and select_output == "Snowflake":
            json_file = os.path.join(JSON_FOLDER, "oracle_to_snowflake.json")
            shutil.copy(json_file, JSON_SAVE_FOLDER)
            
            # pre - processing for Oracle to Snowflake case
            print(oracle_preprocessing(UPLOAD_FOLDER))

            return json.dumps({
                "status" :"Success_1"
                }, indent=4)
        else:
            json_file = os.path.join(JSON_FOLDER, "teradata_to_snowflake.json")
            shutil.copy(json_file, JSON_SAVE_FOLDER)
            return json.dumps({
                "status" :"Success_1"
                }, indent=4)
    else:
        return json.dumps({
            "status":"Failure",
            "error" :"Select source and target database from list"
            }, indent=4)

@APP.route('/upload', methods=['POST'])
def upload_file():
    '''
            DOCSTRING : This function saves the file uploaded from frontend to a folder.
                        Returns a json output containing status as 'Success_2' if the
                        function is working correctly.
            -----
    '''
    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    else:
        remove_files(UPLOAD_FOLDER)

    if 'files' not in request.files:
        return json.dumps({
            "status":"Failure",
            "error" :"Check if 'files' KEY is mentioned"
            }, indent=4)

    files = request.files.getlist('files')

    for ind in range(len(files)):
        if not(files[ind] and allowed_file(files[ind].filename)):
            return json.dumps({
                "status":"Failure",
                "error" :"File not entered or file extension not allowed! Extensions allowed : txt,sql"
                }, indent=4)
        else:
            filename = secure_filename(files[ind].filename)
            if len(os.listdir(UPLOAD_FOLDER)) != 0 and ind == 0:
                remove_files(UPLOAD_FOLDER)
                files[ind].save(os.path.join(UPLOAD_FOLDER, filename))
                
            else:
                files[ind].save(os.path.join(UPLOAD_FOLDER, filename))
    return json.dumps({
        "status" :"Success_2"
        }, indent=4)


@APP.route('/dialogbox', methods=['POST'])
def copy_paste_dialogbox():
    '''
        DOCSTRING : Returns a json output containing query and status as 'Success_3'
        -----
    '''
    if 'text' not in request.form:
        return json.dumps({
            "status":"Failure",
            "error" :"Check if 'text' KEY is mentioned"
            }, indent=4)
    text = request.form['text']
    if text.strip() != "":
        if len(os.listdir(UPLOAD_FOLDER)) == 0:
            write_file(UPLOAD_FOLDER, text, "")    
        else:
            remove_files(UPLOAD_FOLDER)
            write_file(UPLOAD_FOLDER,text, "")
        return json.dumps({
            "status" :"Success_3"
            }, indent=4)
    else:
        return json.dumps({
            "status":"Failure",
            "error" :"Enter some query"
            }, indent=4)

def kv_flag():
    kv_filename = os.listdir(JSON_SAVE_FOLDER)
    print("kv_filname",kv_filename)

    if kv_filename[0] == "hive_to_snowflake.json":
        return 1
    elif kv_filename[0] == "oracle_to_snowflake.json":
        return 2
    elif kv_filename[0] == "teradata_to_snowflake.json":
        return 3
    else:
        pass
        print("No KV match file in folder")
# if __name__ == "__main__":
#     APP.run(host='127.0.0.1', port=7000, debug=True, threaded=True)
    
########### SCREEN 2 #############


# PATH = os.getcwd()
ALTER_QUERY_FOLDER = os.path.join(PATH, 'alter query')
EDITED_QUERY_FOLDER = os.path.join(PATH, 'edited query')


if not os.path.isdir(ALTER_QUERY_FOLDER):
    os.mkdir(ALTER_QUERY_FOLDER)

'''QUERY = SELECT * FROM employees ORDER BY Department;
        CREATE TABLE emp ( eid int, name String,
        salary String, destination String)
        COMMENT ‘Employee details’
        ROW FORMAT DELIMITED
        FIELDS TERMINATED BY ‘\t’
        LINES TERMINATED BY ‘\n’
        STORED AS TEXTFILE;
        select * from emps;
        select * from a;'''

'''QUERY=create table tredence (Id int,name varchar);
         create table john (city varchar);'''


@APP.route('/audit_tables', methods=['POST'])
def list_audit_tables():
    '''
        DOCSTRING : Returns list of tables in which audit columns are to be added.
        -----
    '''
    if 'option_tables' not in request.form:
        return json.dumps({
            "status":"Failure",
            "error" :"Check if option_tables KEY is mentioned"
            }, indent=4)
    option = request.form['option_tables']
    if option not in ['All tables', 'Specific tables', 'No']:
        return json.dumps({
            "status":"Failure",
            "error" :"Enter from the options : All tables, Specific tables, No"
            }, indent=4)
    files = glob.glob('edited query\*')
    query = ""
    for file in files:
        file_read = read_specific_file(file)
        query += file_read
        query += "|| "
    #print(query)
    tables_all = list(get_tables_all(query))
    if option == 'No':
        return json.dumps({
            "status" :"Success",
            "returns":option
            }, indent=4)
    elif option == 'All tables':
        tables = tables_all
    elif option == 'Specific tables':
        if 'specific_tables' not in request.form:
            return json.dumps({
                "status":"Failure",
                "error" :"Check if specific_tables KEY is mentioned"
                }, indent=4)
        text = request.form['specific_tables']
        if text.strip() == "":
            tables_sp = []
        else:
            tables_sp = text.replace(" ", "")
            tables_sp = tables_sp.split(",")
        if len(tables_sp) == 0:
            return json.dumps({
                "status":"Failure",
                "error" :"Please enter a table"
                }, indent=4)
        else:
            val = False
            for i in tables_sp:
                if i not in tables_all:
                    if len(tables_sp) == 1:
                        val = True
                        break
                    return json.dumps({
                        "status":"Failure",
                        "error" :"Only tables from the query are allowed!",
                        }, indent=4)
            tables = tables_sp
            if val == True:
                regex = re.compile(tables_sp[0])
                tables = list(filter(regex.match, tables_all))
                if len(tables) == 0:
                    return json.dumps({
                        "status":"Failure",
                        "error" :"Please enter a valid regex/table that match tables in query"
                        }, indent=4)
    if option != 'No':
        return json.dumps({
            "status" :"Success",
            "returns":tables
            }, indent=4)


@APP.route('/audit_columns_test', methods=['POST'])
def audit_columns_test():
    '''
        DOCSTRING : This function will input column names and table list(to be altered)
        and return new columns in alter table query
        -----
    '''
    if 'columns' not in request.form:
        return json.dumps({
            "status":"Failure",
            "error" :"Check if 'columns' KEY is mentioned"
            }, indent=4)
    column_data = request.form['columns']
    print(column_data)
    if column_data.strip() == "":
        return json.dumps({
            "status":"Failure",
            "error" :"Please enter audit column data"
            }, indent=4)
    column_data = json.loads(column_data)
    print(column_data)
    #print(type(column_data))
    #column_values = column_data[0].values()
    #column_val_list = []
    #for item in column_values:
        #val_item = list(item.values())
        #column_val_list.append(val_item)
    return json.dumps({
        "status" :"Success",
        "returns":column_data
        }, indent=4)


@APP.route('/audit_columns', methods=['POST'])
def audit_columns():
    '''
        DOCSTRING : This function will input column names and table list(to be altered)
        and return new columns in alter table query
        -----
    '''
    if 'columns' not in request.form:
        return json.dumps({
            "status":"Failure",
            "error" :"Check if 'columns' KEY is mentioned"
            }, indent=4)
    column_data = request.form['columns']
    if column_data.strip() == "":
        return json.dumps({
            "status":"Failure",
            "error" :"Please enter audit column data"
            }, indent=4)
    column_data = json.loads(column_data)
    #column_values = list(column_data[0].values())
    #column_val_list = []
    #for item in column_values:
        #val_item = list(item.values())
        #column_val_list.append(val_item)
    list_audit_tables_out = json.loads(list_audit_tables())
    print(list_audit_tables_out)
    if list_audit_tables_out["status"] == "Success":
        if list_audit_tables_out["returns"] == "No":
            return json.dumps({
                "status":"Success",
                "returns" :"No audit columns need to be added"
                }, indent=4)
        tables_list = list_audit_tables_out["returns"]
        alter_query = audit_columns_query(column_data, tables_list)
        folder = os.listdir(ALTER_QUERY_FOLDER)
        if len(folder) == 0:
            file_save_path = os.path.join(ALTER_QUERY_FOLDER, "alter_query.txt")
            text_file = open(file_save_path, "w")
            alter_query_str='\n'.join(alter_query)
            text_file.write(alter_query_str)
            text_file.close()
        else:
            for file_name in os.listdir(ALTER_QUERY_FOLDER):
                file_path = os.path.join(ALTER_QUERY_FOLDER, file_name)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            file_save_path = os.path.join(ALTER_QUERY_FOLDER, "alter_query.txt")
            text_file = open(file_save_path, "w")
            alter_query_str='\n'.join(alter_query)
            text_file.write(alter_query_str)
            text_file.close()
        return json.dumps({
            "status" :"Success",
            "returns":alter_query
            }, indent=4)
    else:
        return json.dumps({
            "status" :"Failure",
            "error":list_audit_tables_out["error"]
            }, indent=4)

@APP.route('/screen2', methods=['POST'])
def next_screen2():
    '''
        DOCSTRING : This function will input column names and table list(to be altered)
        and return new columns in alter table query
        -----
    '''
    list_audit_tables_out = json.loads(list_audit_tables())
    #print(list_audit_tables_out)
    if list_audit_tables_out["status"] == "Success":
        if list_audit_tables_out["returns"] == "No":
            return json.dumps({
                "status":"Success",
                "returns" :"No audit columns need to be added"
                }, indent=4)
        tables_list = list_audit_tables_out["returns"]
        audit_columns_out = json.loads(audit_columns_test())["returns"]
        print(type(audit_columns_out))
        print(audit_columns_out)
        alter_query = audit_columns_query(audit_columns_out, tables_list)
        folder = os.listdir(ALTER_QUERY_FOLDER)
        if len(folder) == 0:
            file_save_path = os.path.join(ALTER_QUERY_FOLDER, "alter_query.txt")
            text_file = open(file_save_path, "w")
            alter_query_str='\n'.join(alter_query)
            text_file.write(alter_query_str)
            text_file.close()
        else:
            for file_name in os.listdir(ALTER_QUERY_FOLDER):
                file_path = os.path.join(ALTER_QUERY_FOLDER, file_name)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            file_save_path = os.path.join(ALTER_QUERY_FOLDER, "alter_query.txt")
            text_file = open(file_save_path, "w")
            alter_query_str='\n'.join(alter_query)
            text_file.write(alter_query_str)
            text_file.close()
        return json.dumps({
            "status" :"Success",
            "returns":alter_query
            }, indent=4)
    else:
        return json.dumps({
            "status" :"Failure",
            "error":list_audit_tables_out["error"]
            }, indent=4)

# if __name__ == "__main__":
#     APP.run(host='127.0.0.1', port=5000, debug=True, threaded=True)


########### SCREEN 3 #############


# PATH = os.getcwd()
DIRECTORY = os.path.join(PATH, 'uploads')
EDITED_QUERY_FOLDER = os.path.join(PATH, 'edited query')
PRE_PROCESSED_FOLDER = os.path.join(PATH, 'pre_processed')

if not os.path.isdir(EDITED_QUERY_FOLDER):
    os.mkdir(EDITED_QUERY_FOLDER)

@APP.route('/screen3', methods=['GET', 'POST'])
def next_screen3():
    '''
        DOCSTRING : calls below mentioned functions: query_parser() & final_query_changes(),
            and returns their output
        -----
    '''
    if request.method == 'GET':
        parser_out = json.loads(query_parser())
        print(parser_out)
        return json.dumps({
            "status":"Success",
            "returns":parser_out["returns"]
            }, indent=4)
    if request.method == 'POST':
        query_changes_out = json.loads(final_query_changes())
        if  query_changes_out["status"] == "Success":
            return json.dumps({
                "status":"Success",
                "returns":query_changes_out["returns"]
                }, indent=4)
        else:
            return json.dumps({
                "status":"Failure",
                "error":query_changes_out["error"]
                }, indent=4)


@APP.route('/query_parser', methods=['GET'])
def query_parser():
    '''
        DOCSTRING : Returns json output containing tables, databases, schemas and views.
        -----
    '''

    result = ""
    flag = kv_flag()
    print("kv_flag",flag)

    if flag == 1:     #hive
        result = query_parser_folder(DIRECTORY)
    elif flag == 2:     #oracle
        result = query_parser_folder(PRE_PROCESSED_FOLDER)
    else:           #teradata
        result = query_parser_folder(DIRECTORY)
    print("old_dict",result)
    # return json.dumps({
    #     "status"  : "Success",
    #     "returns" : result
    #     }, indent=4)
    return json.dumps(result)


@APP.route('/final_query_changes', methods=['POST'])
def final_query_changes():
    '''
        DOCSTRING : Returns final query after any editing from frontend.
        -----
    '''
    flag = kv_flag()
    print("kv_flag",flag)

    if flag == 1:     #hive
        old_dict = query_parser_folder(DIRECTORY)     # KV pair with component name only
    elif flag == 2:     #oracle
        old_dict = query_parser_folder(PRE_PROCESSED_FOLDER)     # KV pair with component name only
    else:
        pass
    
    if 'dict_edit' not in request.form:
        return json.dumps({
            "status":"Failure",
            "error" :"Check if 'dict_edit' KEY is mentioned"
            }, indent=4)
    
    new_dict = request.form['dict_edit']
    if new_dict.strip() == "":
        return json.dumps({
            "status":"Failure",
            "error" :"PLease enter changed dictionary of components"
            }, indent=4)
    new_dict = json.loads(new_dict)
    print("\nold_dict:  ",old_dict)
    print("\nnew_dict:  ",new_dict)
    old_dict = dict_format(old_dict)
    new_dict = dict_format(new_dict)
    changes = change_diff(old_dict, new_dict)      #changes and removed components diff
    print("\nCHANGES:  ",changes)
    
    if flag == 1:     #hive
        query_dict = query_separator_folder(DIRECTORY,changes)    # KV pair with component name and query
    elif flag == 2:     #hive
        query_dict = query_separator_folder(PRE_PROCESSED_FOLDER,changes)    # KV pair with component name and query
        print("\nQUERY_DICT_oracle:  ",query_dict)
        updated_alter_comment_query = replace_name_alter_comment_queries(changes)   
        print("updated",updated_alter_comment_query)
    else:
        pass
    print("\nQUERY_DICT:  ",query_dict)
    # ref_rep_data = final_change_pair(query_dict,old_dict)     # KV pair with component name and query only
    # print("\nREF_REP_DATA:  ",ref_rep_data)
    edited_query = query_replacement(query_dict, changes)    # replacement of above with changes from change_diff
    print("\nEDITED QUERY",edited_query)
    
    # if flag == 1:     #hive
    #     filenames = filename(DIRECTORY)
    # elif flag == 2:     #oracle
    #     filenames = filename(PRE_PROCESSED_FOLDER)
    # else:
    #     pass
    
    edited_queries_filename = "query_generateBy_DDLConverter"+".txt"
    # for ind in range(len(edited_queries_filename)):
    if len(os.listdir(EDITED_QUERY_FOLDER)) != 0 :
        remove_files(EDITED_QUERY_FOLDER)
        write_file(EDITED_QUERY_FOLDER, edited_query, edited_queries_filename)    
    else:
        write_file(EDITED_QUERY_FOLDER, edited_query, edited_queries_filename)
    
    if str(edited_query).strip() == "":
        return json.dumps({
        "status"  : "Failure",
        "returns" : "edited_query is Blank"
        }, indent=4)
    else:
        return json.dumps({
            "status"  : "Success",
            "returns" : edited_query
            }, indent=4)

# if __name__ == "__main__":
#     APP.run(host='127.0.0.1', port=6000, debug=True, threaded=True)

########### SCREEN 4 #############

# PATH = os.getcwd()
INPUT_DIRECTORY = os.path.join(PATH, 'input query')
OUTPUT_DIRECTORY = os.path.join(PATH, 'output query')
KV_MATCH_FILE = os.path.join(PATH, 'kv_match_json')
ALTER_QUERY_FOLDER = os.path.join(PATH, 'alter query')
UPLOAD_FOLDER = os.path.join(PATH, 'uploads')
EDITED_QUERY_FOLDER = os.path.join(PATH, 'edited query')


@APP.route('/input_query', methods=['GET'])
def rename_input_query():
    '''
        DOCSTRING : Returns renamed input files in case of multiple files and 
            file content in case of single file
        -----
    '''
    #delete any previous placed files in Input_query folder.
    if not os.path.isdir(INPUT_DIRECTORY):
        os.mkdir(INPUT_DIRECTORY)
    else:
        remove_files(INPUT_DIRECTORY)

    # copy from upload folder to input query folder
    if len(filename(UPLOAD_FOLDER)) >= 1:
        for i in filename(UPLOAD_FOLDER):
            #print(i)
            file_with_path=os.path.join(UPLOAD_FOLDER,i)
            #print(file_with_path)
            shutil.copy(file_with_path, INPUT_DIRECTORY)

    #query = ""
    output = []
    input_files = filename(INPUT_DIRECTORY)
    print(input_files)
    kv_file = filename(KV_MATCH_FILE)
    print(kv_file)
    kv_file = kv_file[0]
    
    # Adding prefix to the files placed in Input_query folder & return output
    if kv_file != "":
        attach_word= kv_file.split("_")[0] + "_"
        rename_files(INPUT_DIRECTORY, attach_word)
        if len(input_files) == 1:
            for file in os.listdir(INPUT_DIRECTORY):
                file_read = read_specific_file(join(INPUT_DIRECTORY, file))
                #query +=file_read
                output.append({"url":file_read})  
        else:
            rename_files_list = filename_key(INPUT_DIRECTORY)
            print(rename_files_list)
            output = rename_files_list
    if output== "":
        return json.dumps({
            "status":"Failure",
            "error" :"Input scripts are Blank/Not expected, or path is incorrect"
            }, indent=4)
    #return '[{'+output+'}]'
    return json.dumps(output)
        


@APP.route('/conversion', methods=['GET'])
def query_conversion():
    '''
        DOCSTRING : Returns converted snowflake query from either of input databases:
            (HIVE, ORACLE, TERADATA)
        -----
    '''

    flag = kv_flag()

    filename_list = []
    conversion_list = []
    for file in os.listdir(KV_MATCH_FILE):
        kv_file = join(KV_MATCH_FILE, file)
        print(kv_file)
    if not os.path.isdir(OUTPUT_DIRECTORY):
        os.mkdir(OUTPUT_DIRECTORY)  
    for file_name in os.listdir(OUTPUT_DIRECTORY):
        file_path = os.path.join(OUTPUT_DIRECTORY, file_name)
        if isfile(file_path) or islink(file_path):
            os.unlink(file_path)
    # for file in os.listdir(EDITED_QUERY_FOLDER):
    #     input_file = join(EDITED_QUERY_FOLDER, file)
    #     shutil.copy(input_file, OUTPUT_DIRECTORY)
    
    for file in os.listdir(EDITED_QUERY_FOLDER):
        print(file)
        filename_list.append(file)
        file_addr = join(EDITED_QUERY_FOLDER, file)
        query = read_specific_file(file_addr)
        #print(query)
        converted_query = conversion(query, kv_file)
        
        if flag == 1:
            converted_query_alter = final_query_form(ALTER_QUERY_FOLDER,converted_query)
        elif flag == 2:
            converted_query_alter_oracle = final_query_form(ALTER_COMMENT_FOLDER,converted_query)
            converted_query_alter = final_query_form(ALTER_QUERY_FOLDER,converted_query_alter_oracle)
            
        conversion_list.append(converted_query_alter)
        # write updated converted query to output_directory
        file_save_path = os.path.join(OUTPUT_DIRECTORY, file)
        text_file = open(file_save_path, "w")
        text_file.write(converted_query_alter)
        text_file.close()
    
    #renaming to 
    word = kv_file.split("_")[-1]
    attach_word = word.split(".")[0] + "_"
    #for file in os.listdir(OUTPUT_DIRECTORY):
    print(attach_word)
    rename_files(OUTPUT_DIRECTORY, attach_word)
    output_filename_list=[]
    for file in os.listdir(OUTPUT_DIRECTORY):
        output_filename_list.append(file)
    
    # single and mutiple files scenarios
    if len(os.listdir(INPUT_DIRECTORY)) == 1:
        conversion_result = conversion_list[0]
    elif len(os.listdir(INPUT_DIRECTORY)) > 1:
        # filename_output_query = list(zip(filename_list, conversion_list))
        # conversion_result = dict(filename_output_query)
        multiple_file_list = []
        
        for k,file_name in enumerate(output_filename_list):
            multiple_file_dict={}
            print(file_name)
            print(k)
            multiple_file_dict["filename"] = file_name
            multiple_file_dict["data"] = conversion_list[k]
            multiple_file_list.append(multiple_file_dict)
        conversion_result=multiple_file_list
    else:
        conversion_result = "No data to convert"
    
    # if conversion_result.strip() == "":
    #     return json.dumps({
    #         "status":"Failure",
    #         "error" :"Conversion result are Blank/ Not expected"
    #         }, indent=4)
    #else:
    return json.dumps(conversion_result)  

if __name__ == "__main__":
    APP.run(host='127.0.0.1', port=8000, debug=True, threaded=True)