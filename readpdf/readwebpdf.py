'read web pdf file only for python2.7'
__author__ = 'hawrk'
__date__ = '2017.1.6'

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator
import urllib2
from cStringIO import StringIO

url = "http://pythonscraping.com/pages/warandpeace/chapter1.pdf"

def pdf2txt(data,save_path):

    parser = PDFParser(data)

    document = PDFDocument(parser)

    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        #
        rsrcmgr = PDFResourceManager()

        laparams = LAParams()

        device = PDFPageAggregator(rsrcmgr,laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr,device)
        #
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            layout = device.get_result()
            for line in layout:
                try:
                    if(isinstance(line,LTTextBoxHorizontal)):
                        with open('%s'%(save_path),'a') as f:
                            f.write(line.get_text().encode('utf-8') + '\n')
                except:
                    print "failed!"

if __name__ == "__main__":

    html = urllib2.urlopen(urllib2.Request(url)).read()
    dataIO = StringIO(html)
    pdf2txt(dataIO,'b2.txt')

