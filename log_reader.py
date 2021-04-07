#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse
import re
import fileinput
import json

def main():
    parser = argparse.ArgumentParser(description='log reader')
    ## registrar parametros
    parser.add_argument('-f','--filename',
                        help='Arquivo a ser parseado')
    parser.add_argument('-r', '--regex',
                        help="Expressão a ser procurada pelo regex")
    parser.add_argument('-u', '--url',
                        help="URL a ser usada para o endpoint")
    parser.add_argument('-l', '--flags',
                        help="flags válidas: 'a', 'i', 'L', 'm', 's', 'u', 'x'")
    parser.add_argument('-c', '--config',
                        help="config.json")

    ## setar args
    args = parser.parse_args()

    ## ler "config.json"
    if args.config:
        with open(args.config, 'r') as f:
            conf = json.load(f)
        regex_word = conf.get('regex_word')
        integrador_url = conf.get('integrador_url')
        regex_flags = conf.get("regex_flags")

    ## dict de regex flags
    flags_dict = {
        "a": re.ASCII,
        "i": re.IGNORECASE,
        "L": re.LOCALE,
        "m": re.MULTILINE,
        "s": re.DOTALL,
        "u": re.UNICODE,
        "x": re.VERBOSE,
    }

    ## verifica se existe "args.regex"
    if args.regex:
        regex_word = args.regex

    ## verifica se existe "args.url"
    if args.url:
        integrador_url = args.url

    ## verifica se existe "args.flags" e trabalha a quantidade de flags a serem pesquisadas
    if args.flags:
        regex_flags = args.flags
        flag_list = []
        for sing_flag in regex_flags:
            flag_list.append(str(flags_dict[sing_flag]))
        new_flags = []
        for flag in flag_list:
            replaced_flag = flag.replace("RegexFlag", "re")
            new_flags.append(replaced_flag)
        regex_true = '|'.join('{}'.format(sing_data) for sing_data in new_flags)
        argregex = re.compile(r'{}'.format(regex_word), eval(regex_true))

    ## verifica se existe a variável "regex_flags" e trabalha a quantidade de flags a serem pesquisadas
    elif regex_flags:
        flag_list = []
        for sing_flag in regex_flags:
            flag_list.append(str(flags_dict[sing_flag]))
        new_flags = []
        for flag in flag_list:
            replaced_flag = flag.replace("RegexFlag", "re")
            new_flags.append(replaced_flag)
        regex_true = '|'.join('{}'.format(sing_data) for sing_data in new_flags)
        argregex = re.compile(r'{}'.format(regex_word), eval(regex_true))

    ## se não existir args nem parametros faz a pesquisa sem argumentos
    else:
        argregex = re.compile(r'{}'.format(regex_word))

    ## codigo input e stdin
    if args.filename:
        for line in fileinput.input(args.filename):
            if argregex.search(line):
                print("check")
                ## codigo de request (endpoint)
                ## url como string para o integrador com a informação que precisamos
            print(line)
    else:
        for line in sys.stdin:
            if argregex.search(line):
                print("check")
                ## codigo de request (endpoint)
                ## url como string para o integrador com a informação que precisamos
            print(line)
    return 0

if __name__ == '__main__':
    sys.exit(main())
