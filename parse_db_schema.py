#!/usr/bin/env python
# coding: utf-8


import argparse
import re
from collections import OrderedDict as odict
import pprint
from colorama import Fore, Back, Style


def main(dbname, tname=None, list_tname=False):
    def get_table(db_schema):
        with open(db_schema, 'r') as f:
            schema = f.read()
            result = re.findall('CREATE TABLE [^;]+', schema)
            result = [i.split('\n')[:-1] for i in result]
            otable = dict()
            for idx, i in enumerate(result):
                # get table name
                table = re.search('`([^`]+)`', i[0])
                table_name = table.group(1)
                ofield = odict()
                for field in i[1:-1]:
                    field = field.split(' ')[2:]
                    if field[0][0] != '`':
                        continue
                    ofield[(field[0], field[1])] = field[2:]
                otable[table_name] = ofield

        return otable

    db = get_table(dbname)
    if list_tname:
        all_table_name = sorted(list(db.keys()))
        pprint.pprint(all_table_name)
    elif tname:
        list_tname = tname.split(',')
        list_tname = [(cur_tname, db.get(cur_tname, cur_tname))
                      for cur_tname in list_tname]
        for cur_tname, otable in list_tname:
            if not isinstance(otable, str):
                outline = "table[{}]".format(cur_tname)
                print(Fore.GREEN + outline + Style.RESET_ALL)
                pprint.pprint(otable)
            else:
                outline = "table[{}] is not exist.".format(cur_tname)
                print(Fore.RED + outline + Style.RESET_ALL)
    else:
        pprint.pprint(db)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbname", help="database schema file name")
    parser.add_argument("--tname", help="table name")
    parser.add_argument("-l",
                        "--list_tname",
                        action='store_true',
                        help="list all table name")
    args = parser.parse_args()
    if args.dbname:
        main(args.dbname, args.tname, args.list_tname)
    else:
        parser.print_help()
