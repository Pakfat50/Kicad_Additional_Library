# -*- coding: utf-8 -*-
"""
Created on Sun Dec 26 02:51:12 2021

@author: hirar
"""
import glob
import os
from os import path as op

KICAD_DIR_NAME = "ADD_LIB_DIR"

def make_fp_lib_line(dir_name):
    sym_lib_line = '  (lib (name "%s")(type "KiCad")(uri "${%s}/%s")(options "")(descr ""))\n'%(dir_name, KICAD_DIR_NAME, dir_name)
    return sym_lib_line

def make_fp_lib_line_old_rev(dir_name, lib_name):
    sym_lib_line = '  (lib (name "%s")(type "Legacy")(uri "${%s}/%s/%s.mod")(options "")(descr ""))\n'%(dir_name, KICAD_DIR_NAME, dir_name, lib_name)
    return sym_lib_line

def chekc_library_in_dir(name):
    if(op.exists("%s"%name)):
        temp_list = glob.glob("%s/*.kicad_mod"%name)
        if len(temp_list) != 0:
            return True
    else:
        return False

def get_library_list_old_rev(name):
    if(op.exists("%s"%name)):
        temp_list = glob.glob("%s/*.mod"%name)
        ret_list = []
        for elem in temp_list:
            temp_lib = elem.split("\\")[-1]
            temp_lib = temp_lib.replace(".mod", "")
            ret_list.append([name,temp_lib]) #dir_name, lib_name
        return ret_list
    else:
        return []

if __name__ == "__main__":
    f = open("ignore.txt", 'r')
    ignore_list = f.readlines()
    f.close()
    
    cur_dir = os.getcwd()
    f = open("target/fp-lib-table",'r')
    sym_lib_table_old = f.readlines()
    sym_lib_table_new = sym_lib_table_old.copy()
    f.close()
    
    os.chdir("..")
    dir_list = os.listdir()
    
    lib_list = []
    
    for elem in dir_list:
        if not elem in ignore_list:
            if(chekc_library_in_dir(elem)): #kicad_mod形式の場合、ディレクトリをそのまま追加
                lib_list.append(make_fp_lib_line(elem))
            else:
                temp_lib = get_library_list_old_rev(elem) #.mod形式（古い）場合、.modを追加
                if len(temp_lib) != 0:
                    for lib in temp_lib:
                        lib_list.append(make_fp_lib_line_old_rev(lib[0], lib[1]))
    
    for elem in lib_list:
        if not elem in sym_lib_table_old:
            sym_lib_table_new.insert(-1, elem)
        else:
            print(elem)
    os.chdir(cur_dir)
    os.chdir("new_item")
    f = open("fp-lib-table",'w')
    f.writelines(sym_lib_table_new)
    f.close()
    
    