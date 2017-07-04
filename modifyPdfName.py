#coding=utf-8
import sys
import importlib
importlib.reload(sys)

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') 



def parse(path,file_name):
    full_path = path+file_name
    fp = open(full_path, 'rb') 

    praser = PDFParser(fp)

    doc = PDFDocument()

    praser.set_document(doc)
    doc.set_parser(praser)

    doc.initialize()

    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:

        rsrcmgr = PDFResourceManager()
 
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    print(x.get_text())
                    return x.get_text()[0:-1]


import os
def rename():
    count = 0
    path = './'
    filelist = os.listdir(path) 
    for files in filelist:  
        Olddir = os.path.join(path, files) 
        if os.path.isdir(Olddir):
            continue
        filename = os.path.splitext(files)[0] 
        filetype = os.path.splitext(files)[1]  
        if filetype =='.pdf' or filetype =='.PDF':
            new_name =  parse(path,files).replace("\n"," ")
            Newdir = os.path.join(path, new_name + filetype)  
            os.rename(Olddir, Newdir)
        count += 1
 
rename()
