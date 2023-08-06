import os
import sys
sys.path.append(os.path.realpath('.'))
from rel import mod_rel as RelInfo

def main():
    obj_str = 'awt.uno.XInterface'
    ns = 'awt.grid'
    rel = RelInfo.get_rel_import(in_str =obj_str, ns=ns)
    print(f"from {rel.frm} import {rel.imp}")
    
if __name__ == '__main__':
    main()