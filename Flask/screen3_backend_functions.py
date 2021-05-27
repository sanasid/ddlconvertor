# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 13:28:00 2021

@author: abhinash.mishra
"""

import os
import json
import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML

def is_subselect(parsed, first_keyword):
    if not parsed.is_group:
        return False
    for item in parsed.tokens:
        if item.ttype is DML and item.value.upper() == first_keyword:
            return True
    return False
def extract_from_part(parsed, first_keyword, second_keyword):
    from_seen = False
    for item in parsed.tokens:
        if from_seen:
            if is_subselect(item, first_keyword):
                yield from extract_from_part(item,first_keyword, second_keyword)
            elif item.ttype is Keyword:
                return
            else:
                yield item
        elif item.ttype is Keyword and item.value.upper() == second_keyword:
            from_seen = True
def extract_table_identifiers(token_stream):
    for item in token_stream:
        if isinstance(item, IdentifierList):
            for identifier in item.get_identifiers():
                yield identifier.get_name()
        elif isinstance(item, Identifier):
            yield item.get_name()
        # It's a bug to check for Keyword here, but in the example
        # above some tables names are identified as keywords...
        elif item.ttype is Keyword:
            yield item.value
def extract_tables(sql,first_keyword, second_keyword):
    stream = extract_from_part(sqlparse.parse(sql)[0], first_keyword, second_keyword)
    return list(extract_table_identifiers(stream))


def final_query_separator(query):
    global ld
    q=query.split(";")
    #q store the splited query in form of list
    ld=[]
    for i in q:
        #replace new line from each query and appending in new list as ld
        ld.append(i.replace("\n", ""))
    if ld[len(ld)-1]=='' or ld[len(ld)-1]==' ':
        ld=ld[0:len(ld)-1]
    else:
        ld=ld
        
    def ext(quer,ph,sc):
        ext_dat=extract_tables(quer,'CREATE',sc)
        ph.append(ext_dat)
        print(ph)
        return ext_dat    
    global tab,vi,db,sch  
    tab=[]
    vi=[]
    db=[]
    sch=[]   
    table_query=[]
    database_query=[]
    view_query=[]
    schema_query=[]
    test_case=['TABLE','VIEW','DATABASE','SCHEMA']
    #will read the query list
    for t in test_case:
        for k in ld:
            if t=='TABLE':
                ip=ext(k,tab,t)
                print("Table Parsed: ",ip)
                if len(ip)>0:
                    table_query.append(k)
            elif t=='VIEW':
                ip=ext(k, vi,t)
                if len(ip)>0:
                    view_query.append(k)
            elif t=='DATABASE':
                ip=ext(k,db,t)
                if len(ip)>0:
                    database_query.append(k)
            else:
                ip=ext(k,sch,t) 
                if len(ip)>0:
                    schema_query.append(k)
   
    global data
    data={"table":table_query,
          'database':database_query,
          "view":view_query,
          "schema":schema_query}
    return data    
   
def query_separator_folder(directory,changes):
    global query
    query=""
    global filepath
    filepath=[]    
    for filename in os.listdir(directory):
	    f = os.path.join(directory, filename)
	# checking if it is a file
	    if os.path.isfile(f):
	        filepath.append(f)

    for i in range(0,len(filepath)):
        f=open(r"{}".format(filepath[i],"r"))
        text=f.read()
        query=query+text
    #var1=final_query_separator(query)
    var1=kv_component_query(query,changes)  #now using this to create component name with query pair
    return var1

'''query=CREATE TABLE CUSTOMERS(
   ID   INT              NOT NULL,
   NAME VARCHAR (20)     NOT NULL,
   AGE  INT              NOT NULL,
   ADDRESS  CHAR (25) ,
   SALARY   DECIMAL (18, 2),       
   PRIMARY KEY (ID)
);
   CREATE VIEW Brazil_Customers AS
   (SELECT CustomerName, ContactName, City
   FROM Customers
   WHERE Country = 'Brazil');
   
    CREATE DATABASE testDB;
    CREATE SCHEMA web;
    
   CREATE VIEW Customers AS
   (SELECT CustomerName, ContactName, City
   FROM Customers
   WHERE Country = 'Brazil');
query_dict=final_query_seperator(query)
print(query_dict)'''
   

#================================dialogbox======================

def dialog_box_query_parser(query):
    global ld
    q=query.split(";")
    ld=[]
    for i in q:
        ld.append(i.replace("\n", ""))
    if ld[len(ld)-1]=='' or ld[len(ld)-1]==' ':
        ld=ld[0:len(ld)-1]
    else:
        ld=ld

    def ext(quer,ph,sc):
        ext_dat=extract_tables(quer,'CREATE',sc)
        ph.append(ext_dat)
        return ext_dat    
    global tab,vi,db,sch  
    tab=[]
    vi=[]
    db=[]
    sch=[]   
    test_case=['TABLE','VIEW','DATABASE','SCHEMA']
    #will read the query list
    for t in test_case:
        for k in ld:
            if t=='TABLE':
                ext(k,tab,t) 
            elif t=='VIEW':
                ext(k, vi,t)
            elif t=='DATABASE':
                ext(k,db,t)
            else:
                ext(k,sch,t) 
    print("tab",tab)
    global final_tb,final_db,final_sch,final_vi
    final_tb=[]
    final_db=[]
    final_sch=[]
    final_vi=[]
    dat={"table":tab,"database":db,"view":vi,"schema":sch}
    dat1=dat.keys()
    for i in dat1:
        if i=='table':
            for k in dat[i]:
                for o in k:
                    if o!=None and o!=" " and o!="":
                        final_tb.append(o)
        elif i=='database':
            for k in dat[i]:
                for o in k:
                    if o!=None and o!=" " and o!="":
                        final_db.append(o)
        elif i=='view':
            for k in dat[i]:
                for o in k:
                    if o!=None and o!=" " and o!="":
                        final_vi.append(o)
        else:
            for k in dat[i]:
                for o in k:
                    if o!=None and o!=" " and o!="":
                         final_sch.append(o)
    final_tb = list(set(final_tb))
    final_db = list(set(final_db))
    final_sch = list(set(final_sch))
    final_vi = list(set(final_vi))
        #------- form json object
    data=[{"table":final_tb},
         {"database":final_db},
         {"schema":final_sch},
         {"view":final_vi}]
    #data=json.dumps(data)
    return data

#testing the function


#================================ FOLDER WISE=============================

def query_parser_folder(directory):
    global query
    query=""
    global filepath
    filepath=[]    
    for filename in os.listdir(directory):
	    f = os.path.join(directory, filename)
	# checking if it is a file
	    if os.path.isfile(f):
	        filepath.append(f)

    for i in range(0,len(filepath)):
        f=open(r"{}".format(filepath[i],"r"))
        text=f.read()
        query=query+text
    var1=dialog_box_query_parser(query)
    return var1


def dict_format(lst_dict):
    lst=[]
    for i in lst_dict:
        it= list(i.items())
        lst.append(it)
    #print("\n",lst) 
    join_li=[]
    for i in lst:
        join_li+=i
    #print("\n",join_li)
    final_dict = dict(join_li)
    #print("\n",final_dict)
    return final_dict
    
    
def final_change_pair(query_dict,var):
    '''
    This will create table name with table query key value pair and so on. 
    '''
    ref_data=['table','database','schema','view']
    print("\nfinal_change_pair\nquery_dict", query_dict)
    print("\nold-dict", var)
    print("\ndata", data)
    for i in ref_data:
        if i=="table":
            temp_dict_table={}
            table_query_collection=query_dict[i]
            table_name_collection=var[i]
            for i in table_name_collection:
                ind=table_name_collection.index(i)
                temp_dict_table.update({table_name_collection[ind]:table_query_collection[ind]})
            #print(temp_dict_table)
        elif i=='database':
            temp_dict_database={}
            table_query_collection=query_dict[i]
            table_name_collection=var[i]
            for i in table_name_collection:
                ind=table_name_collection.index(i)
                temp_dict_database.update({table_name_collection[ind]:table_query_collection[ind]})
            #print(temp_dict_database)
        elif i=="schema":
            temp_dict_schema={}
            table_query_collection=query_dict[i]
            table_name_collection=var[i]
            for i in table_name_collection:
                ind=table_name_collection.index(i)
                temp_dict_schema.update({table_name_collection[ind]:table_query_collection[ind]})
            #print(temp_dict_schema)
        elif i=="view":
            temp_dict_view={}
            table_query_collection=query_dict[i]
            table_name_collection=var[i]
            for i in table_name_collection:
                ind=table_name_collection.index(i)
                temp_dict_view.update({table_name_collection[ind]:table_query_collection[ind]})
            #print(temp_dict_view)
        else:
            pass
    ref_replace_dict = {"table":temp_dict_table,"database":temp_dict_database,
                        "schema":temp_dict_schema,"view":temp_dict_view}
    return ref_replace_dict

      
#=============new module use to find diff in dict==================

from deepdiff import DeepDiff
from pprint import pprint
def change_diff(org_qr, chan_qr):
    '''
    this function take two dictionary as input and provide difference in there value
    '''
    print("\noriginal query", org_qr)
    print("\nnew query", chan_qr)
    var1 = DeepDiff(org_qr, chan_qr)
    # print("var1_dict",var1.keys())
    # print("var1",not bool(dict(var1)))
    # # print(not bool(var1['iterable_item_removed']))
    # print(not bool(var1['values_changed']))
    print("var1 keys",list(var1.keys()))
    var_keys = list(var1.keys())
    if 'iterable_item_removed' in var_keys and 'values_changed' not in var_keys:
        #removed componants
        print("removed componants")
        removed = var1['iterable_item_removed'].keys()
        # removed_val = var1['iterable_item_removed'].values()
        # removed_item = var1['iterable_item_removed'].items()
        removed_dict = var1['iterable_item_removed']
        # print("removed_key", removed)
        # print("removed_val", removed_val)
        # print("removed_items", removed_item)
        r_tbb = []
        r_dbb = []
        r_viw = []
        r_sh = []
        for dict_key in removed:
            print("dict_key", dict_key)                       
            if 'table' in dict_key:
                r_tbb.append(removed_dict[dict_key])
            elif 'database' in dict_key:
                r_dbb.append(removed_dict[dict_key])
            elif 'schema'in dict_key:
                r_sh.append(removed_dict[dict_key])
            else:
                r_viw.append(removed_dict[dict_key])
        change = {"old_table":[], "new_change_table":[],
                "old_view":[], "new_change_view":[],
                "old_schema":[], "new_schema":[],
                "old_database":[], "new_change_db":[],
            "removed_table":r_tbb,"removed_view":r_viw,
            "removed_database":r_dbb,"removed_schema":r_sh
            }
        return change
    
    elif 'iterable_item_removed' not in var_keys and 'values_changed' in var_keys:
        print("changed componants")
        ke = var1["values_changed"].keys()
        tbb = []
        dbb = []
        viw = []
        sh = []
        for dict_key in ke:
            if 'table' in dict_key:
                tbb.append(dict_key)
            elif 'database' in dict_key:
                dbb.append(dict_key)
            elif 'schema'in dict_key:
                sh.append(dict_key)
            else:
                viw.append(dict_key)
        
        oldlist = []
        newlist = []
        for list_val in tbb:
            oldlist.append(var1["values_changed"][list_val]["old_value"])
            newlist.append(var1["values_changed"][list_val]["new_value"])

        oldview = []
        newview = []
        for list_val in viw:
            oldview.append(var1["values_changed"][list_val]["old_value"])
            newview.append(var1["values_changed"][list_val]["new_value"])

        oldschema = []
        newschema = []
        for list_val in sh:
            oldschema.append(var1["values_changed"][list_val]["old_value"])
            newschema.append(var1["values_changed"][list_val]["new_value"])

        olddb = []
        newdb = []
        for list_val in dbb:
            olddb.append(var1["values_changed"][list_val]["old_value"])
            newdb.append(var1["values_changed"][list_val]["new_value"])
        

        change = {"old_table":oldlist, "new_change_table":newlist,
                "old_view":oldview, "new_change_view":newview,
                "old_schema":oldschema, "new_schema":newschema,
                "old_database":olddb, "new_change_db":newdb,
                "removed_table":[],"removed_view":[],
                "removed_database":[],"removed_schema":[]
                }
        return change
    elif 'iterable_item_removed' in var_keys and 'values_changed' in var_keys:
        print("changed & removed componants")
        ke = var1["values_changed"].keys()
        tbb = []
        dbb = []
        viw = []
        sh = []
        for dict_key in ke:
            if 'table' in dict_key:
                tbb.append(dict_key)
            elif 'database' in dict_key:
                dbb.append(dict_key)
            elif 'schema'in dict_key:
                sh.append(dict_key)
            else:
                viw.append(dict_key)
        
        oldlist = []
        newlist = []
        for list_val in tbb:
            oldlist.append(var1["values_changed"][list_val]["old_value"])
            newlist.append(var1["values_changed"][list_val]["new_value"])

        oldview = []
        newview = []
        for list_val in viw:
            oldview.append(var1["values_changed"][list_val]["old_value"])
            newview.append(var1["values_changed"][list_val]["new_value"])

        oldschema = []
        newschema = []
        for list_val in sh:
            oldschema.append(var1["values_changed"][list_val]["old_value"])
            newschema.append(var1["values_changed"][list_val]["new_value"])

        olddb = []
        newdb = []
        for list_val in dbb:
            olddb.append(var1["values_changed"][list_val]["old_value"])
            newdb.append(var1["values_changed"][list_val]["new_value"])
        
        #removed componants
        removed = var1['iterable_item_removed'].keys()
        # removed_val = var1['iterable_item_removed'].values()
        # removed_item = var1['iterable_item_removed'].items()
        removed_dict = var1['iterable_item_removed']
        # print("removed_key", removed)
        # print("removed_val", removed_val)
        # print("removed_items", removed_item)
        r_tbb = []
        r_dbb = []
        r_viw = []
        r_sh = []
        for dict_key in removed:
            print("dict_key", dict_key)                       
            if 'table' in dict_key:
                r_tbb.append(removed_dict[dict_key])
            elif 'database' in dict_key:
                r_dbb.append(removed_dict[dict_key])
            elif 'schema'in dict_key:
                r_sh.append(removed_dict[dict_key])
            else:
                r_viw.append(removed_dict[dict_key])

        change = {"old_table":oldlist, "new_change_table":newlist,
                "old_view":oldview, "new_change_view":newview,
                "old_schema":oldschema, "new_schema":newschema,
                "old_database":olddb, "new_change_db":newdb,
                "removed_table":r_tbb,"removed_view":r_viw,
                "removed_database":r_dbb,"removed_schema":r_sh
                    }
        return change
    else:
        print("No change")
        change = {"old_table":[], "new_change_table":[],
                "old_view":[], "new_change_view":[],
                "old_schema":[], "new_schema":[],
                "old_database":[], "new_change_db":[],
                "removed_table":[],"removed_view":[],
                "removed_database":[],"removed_schema":[]
                    }
        return change   



'''d={"table": ["CUSTOMERS"], "database": ["testDB"], 
   "schema": ["web"], "view": ["Brazil_Customers", "Customers"]}
#d1 front end
d1={"table": ["CUSTOMERS1"], "database": ["testDB"], 
   "schema": ["web"], "view": ["Brazil_Customers_con", "Customers"]}
new=change_diff(d,d1)
new'''

#condition: 
def query_replacement(ref_rep_data,new):
    '''this function replace the change in table name, database name,schema name, view name'''
    query_replace = ""
    data_key = list(ref_rep_data.keys())
    for i in data_key:
        if i.lower() == 'table':
            db_info=ref_rep_data["table"]
            if len(new["old_table"]) > 0:
                ref_old=new["old_table"]
                ref_new=new["new_change_table"]
                new_rep_data_key=list(db_info.keys())
                new_rep_data_value=db_info
                #print(new_rep_data_value)
                for k in new_rep_data_key:  
                    if k in ref_old:
                        #for j in ref_old:
                        ind=ref_old.index(k)
                        dbquery = new_rep_data_value[k]
                        if len(dbquery.strip())>0:
                            query_replace=query_replace+dbquery.replace(k,ref_new[ind])+";"
                    else:
                        query_replace=query_replace+db_info[k]+";"
            else:
                if len(list(db_info.values()))>0:
                    query_replace=query_replace+";".join(list(db_info.values()))+';'
                
        elif i.lower() == 'database':
            db_info=ref_rep_data["database"]
            if len(new["old_database"]) > 0:
                ref_old=new["old_database"]
                ref_new=new["new_change_db"]
                new_rep_data_key=list(db_info.keys())
                new_rep_data_value=db_info
                #print(new_rep_data_value)
                for k in new_rep_data_key:  
                    if k in ref_old:
                        #for j in ref_old:
                        ind=ref_old.index(k)
                        dbquery = new_rep_data_value[k]
                        if len(dbquery.strip())>0:
                            query_replace=query_replace+dbquery.replace(k,ref_new[ind])+";"
                    else:
                        query_replace=query_replace+db_info[k]+";"
            else:
                if len(list(db_info.values()))>0:
                    query_replace=query_replace+";".join(list(db_info.values()))+';'
                       
        elif i.lower() == 'schema':
            db_info=ref_rep_data["schema"]
            if len(new["old_schema"]) > 0:
                ref_old=new["old_schema"]
                ref_new=new["new_schema"]
                new_rep_data_key=list(db_info.keys())
                new_rep_data_value=db_info
                #print(new_rep_data_value)
                for k in new_rep_data_key:  
                    if k in ref_old:
                        #for j in ref_old:
                        ind=ref_old.index(k)
                        dbquery = new_rep_data_value[k]
                        if len(dbquery.strip())>0:
                            query_replace=query_replace+dbquery.replace(k,ref_new[ind])+";"
                    else:
                        query_replace=query_replace+db_info[k]+";"
            else:
                if len(list(db_info.values()))>0:
                        query_replace=query_replace+";".join(list(db_info.values()))+';'

        else:   #view
            db_info=ref_rep_data["view"]
            if len(new["old_view"]) > 0:
                ref_old=new["old_view"]
                ref_new=new["new_change_view"]
                new_rep_data_key=list(db_info.keys())
                new_rep_data_value=db_info
                #print(new_rep_data_value)
                for k in new_rep_data_key:  
                    if k in ref_old:
                        #for j in ref_old:
                        ind=ref_old.index(k)
                        dbquery = new_rep_data_value[k]
                        if len(dbquery.strip())>0:
                            query_replace=query_replace+dbquery.replace(k,ref_new[ind])+";"
                    else:
                        query_replace=query_replace+db_info[k]+";"
            else:
                if len(list(db_info.values()))>0:
                    query_replace=query_replace+";".join(list(db_info.values()))+';'
    
    return(query_replace)
                            

#print(query_replacement(data, new))      



def kv_component_query(query,changes):
    global ld
    q=query.split(";")
    #q store the splited query in form of list
    ld=[]
    for i in q:
        #replace new line from each query and appending in new list as ld
        ld.append(i.replace("\n", ""))
    if ld[len(ld)-1]=='' or ld[len(ld)-1]==' ':
        ld=ld[0:len(ld)-1]
    else:
        ld=ld
    
    def ext(quer,ph,sc):
        ext_dat=extract_tables(quer,'CREATE',sc)
        ph.append(ext_dat)
        return ext_dat    
    global tab,vi,db,sch  
    tab=[]
    vi=[]
    db=[]
    sch=[]   
    # table_query=[]
    # database_query=[]
    # view_query=[]
    # schema_query=[]
    table_name_query={}
    database_name_query={}
    view_name_query={}
    schema_name_query={}
    test_case=['TABLE','VIEW','DATABASE','SCHEMA']
    #test_case=['table','view','database','schema']
    
    # changes_dict_key = list(changes.keys())
    # print(changes_dict_key)
    removed_tb_value = changes['removed_table']
    removed_db_value = changes['removed_database']
    removed_vw_value = changes['removed_view']
    removed_sc_value = changes['removed_schema']
    #will read the query list
    for t in test_case:
        for k in ld:
            if t.lower()=='table':
                #new_dict={}
                ip=ext(k,tab,t)    #ip is table name
                new_ip=''.join(ip)
                if len(new_ip)>0 and (len(removed_tb_value) == 0 or new_ip not in removed_tb_value):
                    table_name_query[new_ip]=k
                # else:
                #     table_name_query[" "]=" "
            elif t.lower()=='view' :
                #new_dict={}
                ip=ext(k, vi,t)
                new_ip=''.join(ip)
                if len(new_ip)>0 and (len(removed_vw_value) == 0 or new_ip not in removed_vw_value):
                    view_name_query[new_ip]=k
            elif t.lower()=='database':
                #new_dict={}
                ip=ext(k,db,t)
                new_ip=''.join(ip)
                if len(new_ip)>0 and (len(removed_db_value) == 0 or new_ip not in removed_db_value):
                    database_name_query[new_ip]=k
            else:
                #new_dict={}
                ip=ext(k,sch,t) 
                new_ip=''.join(ip)
                if len(new_ip)>0 and (len(removed_sc_value) == 0 or new_ip not in removed_sc_value):
                    schema_name_query[new_ip]=k
   
    global data
    data={"table":table_name_query,
          'database':database_name_query,
          "view":view_name_query,
          "schema":schema_name_query}
    return data    


# query='''CREATE TABLE CUSTOMERS(
#    ID   INT              NOT NULL,
#    NAME VARCHAR (20)     NOT NULL,
#    AGE  INT              NOT NULL,
#    ADDRESS  CHAR (25) ,
#    SALARY   DECIMAL (18, 2),       
#    PRIMARY KEY (ID)
# );
# CREATE TABLE CUSTOMER_BRAND(
#    NAME VARCHAR (20)     NOT NULL,
#    AGE  INT              NOT NULL,
#    ADDRESS  CHAR (25) ,
#    SALARY   DECIMAL (18, 2),       
#    PRIMARY KEY (ID)
# );
#    CREATE VIEW Brazil_Customers AS
#    (SELECT CustomerName, ContactName, City
#    FROM Customers
#    WHERE Country = 'Brazil');
   
#     CREATE DATABASE testDB;
#     CREATE SCHEMA web;
    
#    CREATE VIEW Customers AS
#    (SELECT CustomerName, ContactName, City
#    FROM Customers
#    WHERE Country = 'Brazil');
#    create database cust;
# '''
# print(kv_component_query(query))
# var=dialog_box_query_parser(query)
# print(var)
