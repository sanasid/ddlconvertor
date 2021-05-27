import os
import re
from os.path import isfile, join
# import time
# import json
# import pandas as pd
# import numpy as np
import sqlparse
from screen1_backend_functions import kv_file

PATH = os.getcwd()
# INPUT_DIRECTORY = os.path.join(PATH, 'input query')
# OUTPUT_DIRECTORY = os.path.join(PATH, 'output query')
KV_MATCH_FILE = os.path.join(PATH, 'kv_match_json')

if not os.path.isdir(KV_MATCH_FILE):
    os.mkdir(KV_MATCH_FILE)

def filename(DIRECTORY):
    '''
    This will return the files from the provided directoy/path.
    '''
    try:
        list_input_files = [file for file in os.listdir(DIRECTORY) if isfile(join(DIRECTORY, file))]
        return list_input_files
    except OSError:
        print('There is no file/path found,', DIRECTORY)
    

def filename_key(DIRECTORY):
    list_input_files = [{"url":file} for file in os.listdir(DIRECTORY) if isfile(join(DIRECTORY, file))]
    return list_input_files

kv_filenames = filename(KV_MATCH_FILE)
#print(kv_filenames)
if len(os.listdir(KV_MATCH_FILE)) != 0:
    kv_filename = kv_filenames[0]

def rename_files(DIRECTORY, word):
    '''
    This will rename the files in provided directoy/path with provided suffix.
    '''
    try:
        for filename in os.listdir(DIRECTORY):
            dst =  word + filename
            # rename all the files
            os.rename(join(DIRECTORY, filename), join(DIRECTORY, dst))
    except OSError:
            print('There is no file/path found,', DIRECTORY)


def conversion(query,filepath):
    '''
    This will convert the query as per the "KV pair" in the provided directoy/path.
    e.g. for hive_to_snowflake.json, it will convert hive query to snowsql.
    '''
    try:
        kv=kv_file(filepath)
        #print(kv)
        new_query=[]
        new_q=""
        l=[]
        ld=[]
        # l is a list used to store each query when they are breaked
        #pre_list=[]
        line=query.split(";")
        for i in line:
            # replace any text within "<STRING> for HIVE queries""
            i_new = re.sub("[\<].*?[\>]", "", i)
            print("i_new",i_new)
            #replace new line from each query and appending in new list as ld
            ld.append(i_new.replace("\n", "").replace("\tab",""))
        print("ld",ld)
        
        # we are spliting each query using ";"
        for j in range(0,len(ld)):
            ld[j]=ld[j]+' ;'
            split_words=ld[j].split()
            #print(split_words)
            l.append(split_words)
        #print("l before:",l)
        l=l[0:len(l)-1] 
        #print("l after:",l)
        
        if kv_filename == "hive_to_snowflake.json":
            for j in l:
                print("j",j)  #J is single query
                d=[]
                for i in j:
                    print("i before",i)
                # fir check the word in hive if it exist replace it wiht snowflakes
                    if i.lower() in kv["kv"]["HIVE_Query"]:
                        ind=kv["kv"]["HIVE_Query"].index(i.lower())
                        i=kv["kv"]["Snowflake_Query"][ind]
                        d.append(" "+i.lower())
                    elif i.lower() in kv["kv"]["HIVE_Alter"]:
                        ind=kv["kv"]["HIVE_Alter"].index(i.lower())
                        i=kv["kv"]["Snowflake_Alter"][ind]
                        d.append(" "+i.lower())
                    elif i.lower() in kv["kv"]["words_hive"]:
                        ind=kv["kv"]["words_hive"].index(i.lower())
                        i=kv["kv"]["words_snowflake"][ind]
                        d.append(" "+i.lower())
                    elif i.lower() in kv["kv"]["datatype_hive"]:
                        ind=kv["kv"]["datatype_hive"].index(i.lower())
                        i=kv["kv"]["datatype_snowflake"][ind]
                        d.append(" "+i.lower()) 
                        #print("datatype i: ",i.lower())
                    # elif i.lower() in kv["kv"]["undefined_snowflake"]:
                    #     print("undefined snow ",i)
                    #     print("kv",kv["kv"]["undefined_snowflake"])
                    #     #d.append(i.lower().replace(i.lower(), ""))
                    #     pass
                    #commenting undefine snowflake
                    #error undefine
                    # elif i.upper() in kv["kv"]["undefined"]:
                    #     d.append("--"+i.upper())
                    elif i.lower() in kv["kv"]["defined_snowflake"]:
                        d.append(" "+i.lower()) 
                    else:
                        d.append(" "+i)
                        print("else i:",i)
                    #sqlparse.format(d, reindent=True, keyword_case='upper')
                    print("i after",i)
                print("d modified:",d)

                #undefined comment
                hashcount='1'
                for i in range(len(j)):
                    print("d[i].lower()",d[i].lower())
                    if d[i].lower().strip() in kv["kv"]["undefined_snowflake"]:
                        if hashcount=='1':
                            print('d[k] 1',d[i])
                            d[i]="\n"+"//"+d[i]
                            hashcount='0'
                    else:
                        if hashcount=='0' and d[i].strip() == ";":
                            print("terminater")
                            d[i]="\n"+d[i]
                        else:
                            print('d[ki] 0',d[i])
                            d[i]

                print("d after undefined",d)
                new_query.append(d)
            final_query=[]
            for i in new_query:
                final_query=final_query+i

            # here we get list of all query
            # print(type(final_query))
            # print(final_query)
            new_q="".join(final_query)
            #print(new_q)
            conversion_q_formatted=""
            new_q=new_q[:-2]
        
        elif kv_filename == "oracle_to_snowflake.json":
            for j in l:
                print("j",j)  #J is single query
                d=[]
                for i in j:
                    print("i before",i)
                    # fir check the word in hive if it exist replace it wiht snowflakes
                    if i.lower() in kv["kv"]["HIVE_Query"]:
                        ind=kv["kv"]["HIVE_Query"].index(i.lower())
                        i=kv["kv"]["Snowflake_Query"][ind]
                        d.append(" "+i.lower())
                    elif i.lower() in kv["kv"]["HIVE_Alter"]:
                        ind=kv["kv"]["HIVE_Alter"].index(i.lower())
                        i=kv["kv"]["Snowflake_Alter"][ind]
                        d.append(" "+i.lower())
                    elif i.lower() in kv["kv"]["words_hive"]:
                        ind=kv["kv"]["words_hive"].index(i.lower())
                        i=kv["kv"]["words_snowflake"][ind]
                        d.append(" "+i.lower())
                    elif i.lower() in kv["kv"]["datatype_hive"]:
                        ind=kv["kv"]["datatype_hive"].index(i.lower())
                        i=kv["kv"]["datatype_snowflake"][ind]
                        d.append(" "+i.lower()) 
                        #print("datatype i: ",i.lower())
                    # elif i.lower() in kv["kv"]["undefined_snowflake"]:
                    #     print("undefined snow ",i)
                    #     print("kv",kv["kv"]["undefined_snowflake"])
                    #     #d.append(i.lower().replace(i.lower(), ""))
                    #     pass
                    #commenting undefine snowflake
                    #error undefine
                    # elif i.upper() in kv["kv"]["undefined"]:
                    #     d.append("--"+i.upper())
                    elif i.lower() in kv["kv"]["defined_snowflake"]:
                        d.append(" "+i.lower()) 
                    else:
                        d.append(" "+i)
                        print("else i:",i)
                    #sqlparse.format(d, reindent=True, keyword_case='upper')
                    print("i after",i)
                print("d modified:",d)

                #undefined comment
                hashcount='1'
                for i in range(len(j)):
                    print("d[i].lower()",d[i].lower())
                    if d[i].lower().strip() in kv["kv"]["undefined_snowflake"]:
                        if hashcount=='1':
                            print('d[k] 1',d[i])
                            d[i]="\n"+"//"+d[i]
                            hashcount='0'
                    else:
                        if hashcount=='0' and d[i].strip() == ";":
                            print("terminater")
                            d[i]="\n"+d[i]
                        else:
                            print('d[ki] 0',d[i])
                            d[i]

                print("d after undefined",d)
                new_query.append(d)
            final_query=[]
            for i in new_query:
                final_query=final_query+i
        
            # here we get list of all query
            # print(type(final_query))
            # print(final_query)
            new_q="".join(final_query)
            #print(new_q)
            conversion_q_formatted=""
            new_q=new_q[:-2]
        
        else:
            pass #teradata logic
            
        
        # ANSI syntax format
        for i in new_q.split(";"):
            q_format=sqlparse.format(i,keyword_case='upper')
            q_format = q_format.lstrip()
            conversion_q_formatted=conversion_q_formatted+q_format+";"+"\n"
            
    except OSError:
            print('There is no filepath found,', filepath)
    return conversion_q_formatted


# filepath=r"C:\Users\sudeep.kumar\Desktop\Accelerator\accelerator\kv_match_json\hive_to_snowflake.json"
# query= '''CREATE TABLE parquet_test10(
#   id int,
#   str string,
#   mp MAP <STRING,STRING>,
#   lst ARRAY <STRING>,
#   strct STRUCT <A:STRING,B:STRING>) 
# ROW FORMAT SERDE 'parquet.hive.serde.ParquetHiveSerDe'
#   STORED AS
#   INPUTFORMAT 'parquet.hive.DeprecatedParquetInputFormat'
#   OUTPUTFORMAT 'parquet.hive.DeprecatedParquetOutputFormat';
#   CREATE DATABASE testDB; ''' 
# q = conversion(query,KV_MATCH_FILE)
# print(q)
# required_output=''' CREATE TABLE parquet_test10 ( id int 
# , str string 
# , mp Object 
# , lst Variant 
# , strct Array ) /*ROW FORMAT SERDE 'parquet.hive.serde.ParquetHiveSerDe' STORED AS 
# INPUTFORMAT 'parquet.hive.DeprecatedParquetInputFormat' 
# OUTPUTFORMAT 'parquet.hive.DeprecatedParquetOutputFormat'*/ ;
# '''

def final_query_form(directory,query_part1):
    '''
    This will return add the "Alter" commands for "audit columns" placed in provided directory in the main converted query returned by function conversion().
    '''
    #query_part1=conversion(query,filepath)
    #type
    global query1
    global filepath1
    query1=""
    converted_query=""
    filepath1=[]    
    try:
        # add filename in that path with pathname
        for alter_filename in os.listdir(directory):
            f = os.path.join(directory, alter_filename)
            # checking if it is a file
            if os.path.isfile(f):
                filepath1.append(f)

        #reading the filename having ALTER query for audit columns
        for i in range(0,len(filepath1)):
            f=open("{}".format(filepath1[i],"r"))
            text=f.read()
            query1=query1+text
            f.close()
        converted_query=query_part1+"\n"+query1
        print(converted_query)
                    
    except OSError:
            print('There is no filepath found,', directory)
    #print(converted_query_formatted)
    return converted_query

# alter_d=r"C:\Users\sudeep.kumar\Desktop\Accelerator\accelerator\alter query"
# final_query_form(alter_d,q)
