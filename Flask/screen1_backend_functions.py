# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 00:30:53 2021

@author: aaina.c
"""
import os
import json

def read_folder(path):
    '''DOCSTRING : Reads a folder selected from front end screen 1 browse button'''
    global q, path_list
    path_list = []
    q = ""
    directory = os.path.normpath(path)
    for subdir, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt") or file.endswith(".sql"):
                path_list.append(os.path.join(subdir, file))
                f=open(os.path.join(subdir, file),'r')
                a = f.read()
                q = q+a
                f.close()
                q = q+"||"
    return q
 

#path = r"C:\Users\aaina.c\Downloads\New folder\test_upload_folder" 
#read_folder(path)
#print(q)
#print(path_list)

def read_specific_file(file_addr):
    '''DOCSTRING : Reads a file selected from front end screen 1 browse button'''
    global q
    q = ""
    if file_addr.endswith('.txt') or file_addr.endswith('.sql'):
        try:
            file=open(file_addr,"r")
            a = file.read()
            q = q+a
            file.close()
            #q=q+"||"
            return(q)
        except IOError:
            print('There is no file address named,', file_addr)

#path = r"C:\Users\aaina.c\Downloads\New folder\test_upload_folder\DDL (3).txt" 
#read_specific_file(path)
#!read_specific_file
#help(read_specific_file)
    
def kv_file(path):
    '''
        DOCSTRING : Reads the json file pair for the option selected from front end screen 1 source & target database;
          for instance, if hive is selected as source database & snowflake is selected as target database, 
          then this function will read the hive_to_snowflake json file, i.e.
          This will return the "KV pair" from the provided directoy/path.
          -----
    '''
    try:
        file = open(path,"r")
        text = file.read()
        kv = json.loads(text)
        file.close()
        return(kv)
    except IOError:
        print('There is no file address named,', path)
        
def remove_files(folder):
    '''
        DOCSTRING : Removes the files from the mentioned folder taken as input
        -----
    '''
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
            
def write_file(folder, query, filename):
    '''
        DOCSTRING : Writes a file and saves it within a folder
        -----
    '''
    if filename == "":
        file_save_path = os.path.join(folder, "query.txt")
    else:
        file_save_path = os.path.join(folder, filename)
    text_file = open(file_save_path, "w")
    text_file.write(query)
    text_file.close()
  
'''def check_DDL(query):
    statements=sqlparse.split(query)
    print(statements)
    for statement in statements:
        parsed = sqlparse.parse(statement)
        #if not parsed.is_group:
        #    return False
        for item in parsed.tokens:
            if item.ttype is DDL:
                return(item)
        return False

query="CREATE DATABASE customers;create table _name (name varchar2(50)); select name, age, 'Hello World; Testing' from customer;"
#check_DDL(query)
statements=sqlparse.split(query)
print(statements)
for statement in statements:
        parsed = sqlparse.parse(statements)[0]
        print(parsed.tokens)
        check_DDL(parsed)
def check_DDL(parsed):
        #if not parsed.is_group:
        #    return False
        for item in parsed.tokens:
            if item.ttype is DDL:
                return(item)
        return False'''
    