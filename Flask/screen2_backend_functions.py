# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 11:58:28 2021

@author: aaina.c
"""

import sqlparse
import sql_metadata
from screen3_backend_functions import extract_tables
#screen3_backend_functions import extract_tables

def get_tables_all(query):
    global ld
    q = query.split(";")
    ld = []
    for i in q:
        ld.append(i.replace("\n", ""))
    if ld[len(ld)-1]=='' or ld[len(ld)-1]==' ':
        ld = ld[0:len(ld)-1]
    else:
        ld = ld

    def ext(quer,ph,sc):
        ext_dat = extract_tables(quer,'CREATE',sc)
        #ph.append(ext_dat)
        return ext_dat    
    global tab
    tab = []   
    tables_list = []
    for k in ld:
        table = ext(k,tab,"TABLE") 
        tables_list += table
    return set(tables_list)


def get_tables_all_prev(query):
    '''
        DOCSTRING : Returns list of tables present in query
        -----
    '''
    statements = sqlparse.split(query)
    tables_all = []
    for i in statements:
        table = sql_metadata.get_query_tables(i)
        tables_all += table
    return tables_all


def audit_columns_query(column_data, tables_list):
    '''
        DOCSTRING : Returns an alter table query taking columns data and table list as input
        -----
    '''
    #global li
    lis = []
    new_alt = ""
    #table_name=['a','b','c','d','e']
    table_name = tables_list
    #this columns must be in json format
    #column_values = list(column_data[0].values())
    print(column_data)
    column_val_list = []
    for ele in column_data:
        column_values = list(ele.values())
        column_val_list.append(column_values)
    print(column_val_list)
    # print(column_values[2])
    # print(type(column_values[2]))
    # column_val_list = []
    # for item in column_values:
        # val_item = list(item.values())
        # column_val_list.append(val_item)
    col = column_val_list
    #col=[[],[]]

    #this loop will only handle column name, datatype and value
    for i in col:
        var = i
        # print(var[i])
        # print(type(var[2]))
        if var[1].lower() in ['varchar', 'int', 'float', 'datetime'] and var[2] == True:
            new_alt = '''alter table table_name add column {} {};'''.format(var[0], var[1])
            lis.append(new_alt)
        elif var[1].lower() in ['varchar', 'int', 'float', 'datetime'] and var[2] == False:
            new_alt = '''alter table table_name add column {} {} NOT NULL;'''.format(var[0], var[1])
            lis.append(new_alt)
        else:
            print("Issue in datatype")


    #form a final query and implement table name
    #global new_li
    new_li = []
    final_list = []
    for j in table_name:
        for data in lis:
            data = data.replace("table_name", j)
            new_li.append(data)
    for i in new_li:
        stat_format = sqlparse.format(i, reindent=True, keyword_case='upper')
        final_list.append(stat_format)
    return final_list
