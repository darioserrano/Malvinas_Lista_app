from os import openpty
import os
import fitz
import re
import pandas as pd
from collections import namedtuple
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
from flask import request




def conversor():
    Line = namedtuple('Line', 'BODEGA ARTICULO PRECIO')

    f = request.files['ourfile']
    file = f.filename
    documento = fitz.open(file)

    lines = []
    bodega = re.compile('\w?\d+\s\w+')
    articulos = re.compile('[(]\w?\w?\d+[)]')
    precios = re.compile('\d{3,4}[.]\d{3}')

    for pagina in documento:
        texto = pagina.getText()
        for line in texto.split('\n'):
            if bodega.match(line):
                bod = line
            elif articulos.match(line):
                art = line
            elif precios.match(line):
                pr = line
                lines.append(Line(bod, art, pr))

    df = pd.DataFrame(lines,columns = ['BODEGA', 'ARTICULO', 'PRECIO'])

    df['PRECIO'] = pd.to_numeric(df['PRECIO'])
    df.to_excel('./Archivos PDF/'+file +".xlsx", index=False)
    os.remove('./Archivos PDF/'+file)