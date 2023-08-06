# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 15:47:42 2021

@author: macie
"""

import glob
import numpy as np
definitions = glob.glob(r'C:\biopal\BioPAL-1\doc\agb\definitions.rst')
list_of_files = glob.glob(r'C:\biopal\BioPAL-1\doc\agb\*diag.rst')+\
    glob.glob(r'C:\biopal\BioPAL-1\doc\agb\*math.rst')



with open(definitions[0],'rt') as fid:
    txt = fid.read()
    fid.close()

lut = [[x.strip() for x in df.split('.. ')[1].split(' replace:: ')] for df in txt.split('\n') if df.find('.. ')>=0]


for diagfile in list_of_files:
    
    with open(diagfile,'rt') as fid:
        txt_icd = fid.read()
        txt_atbd = txt_icd.replace('|int','|name')
        for k in range(10):
            for currlut in lut:
                txt_icd = txt_icd.replace(currlut[0],currlut[1].replace('*',''))

                txt_atbd = txt_atbd.replace(currlut[0],currlut[1].replace('*',''))
        fid.close()
        
    with open(diagfile.replace('.rst','_atbd.rst'),'wt') as fid:
        fid.write(txt_atbd)
        fid.close()
    with open(diagfile.replace('.rst','_icd.rst'),'wt') as fid:
        fid.write(txt_icd)
        fid.close()