# -*- coding: utf-8 -*-
"""
Created on Sun Dec 26 02:51:12 2021

@author: hirar
"""
import glob
import os
from os import path as op

KICAD_DIR_NAME = "ADD_LIB_DIR"

def make_sym_lib_line(dir_name, lib_name):
    sym_lib_line = '  (lib (name "%s")(type "Legacy")(uri "${%s}/%s/%s.lib")(options "")(descr ""))\n'%(lib_name, KICAD_DIR_NAME, dir_name, lib_name)
    return sym_lib_line

def get_library_list(name):
    if(op.exists("%s"%name)):
        temp_list = glob.glob("%s/*lib"%name)
        ret_list = []
        for elem in temp_list:
            temp_lib = elem.split("\\")[-1]
            temp_lib = temp_lib.replace(".lib", "")
            ret_list.append([name,temp_lib]) #dir_name, lib_name
        return ret_list
    else:
        return []

if __name__ == "__main__":
    f = open("ignore.txt", 'r')
    ignore_list = f.readlines()
    f.close()
    
    cur_dir = os.getcwd()
    f = open("target/sym-lib-table",'r')
    sym_lib_table_old = f.readlines()
    sym_lib_table_new = sym_lib_table_old.copy()
    f.close()
    
    os.chdir("..")
    dir_list = os.listdir()
    
    lib_list = []
    
    for elem in dir_list:
        if not elem in ignore_list:
            temp_lib = get_library_list(elem)
            if len(temp_lib) != 0:
                for lib in temp_lib:
                    lib_list.append(make_sym_lib_line(lib[0], lib[1]))
    
    
    for elem in lib_list:
        if not elem in sym_lib_table_old:
            sym_lib_table_new.insert(-1, elem)
        else:
            print(elem)
    os.chdir(cur_dir)
    os.chdir("new_item")
    f = open("sym-lib-table",'w')
    f.writelines(sym_lib_table_new)
    f.close()
    
    