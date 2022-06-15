# Fernando Resendiz Bauitsta A01769659
# Jorge Omar López Gemigniani A01769675
# Darío Mejía Castillo A01769961

import shutil
import os
import re
import multiprocessing
import glob
import time
from html import escape

#las funciones get_key determinan a que tipo pertenece un caracter para cada autómata
def get_key_rkt(char):
    if char == ';' or char == '#' or char == '|' or char == '.' or char == '"':
        return char

    if char == '\n':
        return 'br'

    if char.isnumeric():
        return 'd'

    if re.search('[^()\[\]{},"`;#|\\s\\n\\\\]', char):
        return 'w'

    return 's'


def get_key_c(char):

    if char == '/' or char == '*' or char == '.' or char == '"' or char == "'":
        return char

    if char == '\n':
        return 'br'

    if char.isnumeric():
        return 'd'

    if char.isalpha() or char == '_':
        return 'w'

    return 's'


def get_key_py(char):

    if char == '#' or char == '.' or char == '"' or char == "'":
        return char

    if char == '\n':
        return 'br'

    if char.isnumeric():
        return 'd'

    if char.isalpha() or char == '_':
        return 'w'

    return 's'

#matriz de los autómatas para c python y racket
M_rkt = [
    [2, 1, 9, 10, 12, 10, 9, 4, 9],
    [16, 16, 6, 16, 16, 16, 16, 16, 16],
    [2, 2, 2, 2, 2, 2, 2, 2, 3],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 4, 4, 4, 4, 4, 4, 5, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 6, 7, 6, 6, 6, 6, 6, 6],
    [6, 8, 7, 6, 6, 6, 6, 6, 6],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [16, 16, 16, 16, 16, 16, 16, 16, 16],
    [11, 11, 11, 10, 10, 10, 11, 11, 11],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [13, 13, 13, 10, 12, 14, 13, 13, 13],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [15, 15, 15, 10, 14, 10, 15, 15, 15],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

M_c = [
    [1, 9, 10, 12, 9, 9, 4, 9, 17],
    [2, 6, 16, 16, 16, 16, 16, 16, 16],
    [2, 2, 2, 2, 2, 2, 2, 3, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 4, 4, 4, 4, 4, 5, 4, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 7, 6, 6, 6, 6, 6, 6, 6],
    [8, 7, 6, 6, 6, 6, 6, 6, 6],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [16, 16, 16, 16, 16, 16, 16, 16, 16],
    [11, 11, 10, 10, 11, 11, 11, 11, 11],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [13, 13, 13, 12, 14, 13, 13, 13, 13],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [15, 15, 15, 14, 15, 15, 15, 15, 15],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [17, 17, 17, 17, 17, 17, 17, 17, 18],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

M_py = [
    [1, 6, 8, 5, 5, 3, 5, 12],
    [1, 1, 1, 1, 1, 1, 2, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [3, 3, 3, 3, 3, 4, 3, 3],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [7, 6, 6, 7, 7, 7, 7, 7],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [9, 9, 8, 10, 9, 9, 9, 9],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [11, 11, 10, 11, 11, 11, 11, 11],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [12, 12, 12, 12, 12, 12, 12, 13],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

#numero de columnas de la matriz de cada autómta en base al tipo de caracter
cols_rkt = {
    ';': 0,
    '#': 1,
    '|': 2,
    'w': 3,
    'd': 4,
    '.': 5,
    's': 6,
    '"': 7,
    'br': 8
}

cols_c = {
    '/': 0,
    '*': 1,
    'w': 2,
    'd': 3,
    '.': 4,
    's': 5,
    '"': 6,
    'br': 7,
    "'": 8
}

cols_py = {
    '#': 0,
    'w': 1,
    'd': 2,
    '.': 3,
    's': 4,
    '"': 5,
    'br': 6,
    "'": 7
}

#nombres de las clases de css para los diferentes estados del autómata
classes_rkt = {
    '1': 'special_character',
    '2': 'comment',
    '3': 'comment',
    '5': 'string',
    '8': 'multiline_comment',
    '9': 'special_character',
    '10': 'identifier',
    '11': 'identifier',
    '12': 'int',
    '13': 'int',
    '14': 'float',
    '15': 'float',
    '16': 'special_character',
    'r': 'reserved_word'
}

classes_c = {
    '1': 'special_character',
    '2': 'comment',
    '3': 'comment',
    '5': 'string',
    '8': 'multiline_comment',
    '9': 'special_character',
    '10': 'identifier',
    '11': 'identifier',
    '12': 'int',
    '13': 'int',
    '14': 'float',
    '15': 'float',
    '16': 'special_character',
    '18': 'string',
    'r': 'reserved_word'
}

classes_py = {
    '2': 'comment',
    '4': 'string',
    '5': 'special_character',
    '6': 'identifier',
    '7': 'identifier',
    '8': 'int',
    '9': 'int',
    '10': 'float',
    '11': 'float',
    '13': 'string',
    'r': 'reserved_word'
}

#determina los estados en los que se debe regresar un caracter para cada autómata
final_states_rkt = [
    [3, 5, 8],
    [11, 13, 15, 16],
]

final_states_c = [
    [3, 5, 8, 18],
    [11, 13, 15, 16],
]

final_states_py = [
    [2, 4, 5, 13],
    [7, 9, 11],
]

def highliht(file_name, html_file, idx, txt_language=''):

    #lee el archivo a resaltar y lo almacena en una variable
    file = open(file_name, 'r', encoding="utf8")
    program = file.read()
    file.close()

    if re.search('\.c$', file_name):
        language='C'
    elif re.search('\.rkt$', file_name):
        language='Racket'
    elif re.search('\.py$', file_name):
        language='Python'
    elif re.search('\.txt$', file_name):
        language=txt_language
    else:
        raise Exception("The file you selected is not supported")

    
    #determina que autómata usar con base en la extensión del archivo
    if language == 'C':
        file = open('reserved_words_c.txt', 'r', encoding="utf8")
        reserved_words = file.read().split('\n')
        file.close()

        get_key = get_key_c
        M = M_c
        cols = cols_c
        classes = classes_c
        final_states = final_states_c

    elif language == 'Racket':
        file = open('reserved_words_rkt.txt', 'r', encoding="utf8")
        reserved_words = file.read().split('\n')
        file.close()

        get_key = get_key_rkt
        M = M_rkt
        cols = cols_rkt
        classes = classes_rkt
        final_states = final_states_rkt

    elif language == 'Python':
        file = open('reserved_words_py.txt', 'r', encoding="utf8")
        reserved_words = file.read().split('\n')
        file.close()

        get_key = get_key_py
        M = M_py
        cols = cols_py
        classes = classes_py
        final_states = final_states_py

    else:
        raise Exception("The language you selected is not supported")

    state = 0
    lexema = ''

    body = ''

    i = 0

    #ciclo que recorre el programa con el autómata
    while i < len(program):
        char = program[i]

        state = M[state][cols[get_key(char)]]

        lexema += char

        #añade el lexema al html y determina si debe regresar al caracter anterior
        if state in final_states[0]:
            if lexema == '\n':
                body += "<br>"
            else:
                body += f'<pre class="{classes[str(state)]}">{escape(lexema)}</pre>'
            lexema = ''
            state = 0
        elif state in final_states[1]:
            lexema = lexema[:-1]

            if lexema in reserved_words:
                css_class = classes['r']
            else:
                css_class = classes[str(state)]

            if lexema == '\n':
                body += "<br>"
            else:
                body += f'<pre class="{css_class}">{escape(lexema)}</pre>'

            lexema = ''
            state = 0
            i -= 1
        elif i == len(program) - 1:
            if lexema in reserved_words:
                css_class = classes['r']
            else:
                css_class = classes[str(state)]

            if lexema == '\n':
                body += "<br>"
            else:
                body += f'<pre class="{css_class}">{escape(lexema)}</pre>'

        i += 1

    #contenido del archivo html
    html = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    <style>
      body {
        font-size: 1rem;
      }

      pre {
        display: inline;
      }

      body {
        background-color: black;
      }

      .comment {
        color: green;
      }
      .string {
        color: brown;
      }
      .multiline_comment {
        color: green;
      }
      .identifier {
        color: cyan;
      }
      .int {
        color: yellow;
      }
      .float {
        color: yellow;
      }
      .special_character {
        color: white;
      }
      .reserved_word {
        color: magenta;
      }
    </style>
  </head>""" + f"""
<body>
  {body}
</body>
</html>    
"""
    #guarda el html en un archivo
    if not os.path.isdir(os.path.dirname(html_file)):
        os.makedirs(os.path.dirname(html_file), exist_ok=True)

    with open(html_file, "w", encoding="utf8") as f:
        f.write(html)
        f.close()
    print(idx, time.perf_counter())

if __name__ == "__main__":

    #indica el tipo de archivos que es capaz de resaltar el programa
    types = ["/**/*.c", "/**/*.py", "/**/*.rkt", "/**/*.txt"]

    files = []

    #indica la carpeta en la que se guardaran los archivos resaltados
    results = os.path.abspath('./highlighted/')

    #elimina y crea la carpeta
    if os.path.isdir(results):
        shutil.rmtree(results)

    os.mkdir(results)

    #solicita la carpeta con lor archivos a resaltar
    directory = input("Ingrese la dirección de la carpeta con los archivos a resaltar: ")
    directory = os.path.abspath(directory)

    #busca todos los archivos resaltables dentro de la carpeta
    for type in types:
        this_type_files = glob.glob(directory + type, recursive=True)
        files += this_type_files

    processes = [None] * len(files)

    #solicita el lenguaje para resaltar los .txt
    while True:
        print("|===========================================================|")
        print("|        SELECCIONE EL LENGUAJE PARA LOS ARCHIVOS .TXT      |")
        print("|===========================================================|")
        print("|1) C                                                       |")
        print("|2) Racket                                                  |")
        print("|3) Python                                                  |")
        print("|===========================================================|")
        op = input("Indique la opción deseada: ")
        
        if op == '1':
            txt_language = 'C'
            break
        elif op == '2':
            txt_language = 'Racket'
            break
        elif op == '3':
            txt_language = 'Python'
            break
        else:
            print('Opción no válida.')
            input('Presione [ENTER] para continuar...')


    #adapta las direcciones de windows para usarse en regex
    directory_regex = directory.replace("\\","\\\\")
    results_regex = results.replace("\\","\\\\")

    start = time.perf_counter()

    for i, f in enumerate(files):
        html = re.sub(f'^{directory_regex}', results_regex, f)
        highliht(f, html + '.html', i, txt_language)

    finish = time.perf_counter()

    print(len(files), "archivos fueron resaltados")
    print("Tiempo de ejecucion", finish - start)