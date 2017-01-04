'read local pdf file'
__author__ = 'hawrk'
__date__ = '2017.1.4'

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator

def pdf2text(path,save_file):
    '''
    读取本地pdf文档，并保存到txt文件中
    :param path: 源pdf 文件
    :param save_file:  保存txt文件名，无路径则保存到脚本同一目录
    :return: 无
    '''
    #创建分析器
    parser = PDFParser(path)
    #文档存储结构
    document = PDFDocument(parser)

    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        rsrcmgr = PDFResourceManager()

        laparams = LAParams()

        device = PDFPageAggregator(rsrcmgr,laparams = laparams)

        interpreter = PDFPageInterpreter(rsrcmgr,device)
        #处理每一页
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)

            layout = device.get_result()

            for line in layout:
                if(isinstance(line,LTTextBoxHorizontal)):
                    with open('%s' %(save_file),'a') as f:
                        f.write(line.get_text().encode('utf-8'))


if __name__ == 'main':

    path = open('/home/hawrk/doc/data_report.pdf','rb')
    pdf2text(path,'outdata.txt')
    path.close()

