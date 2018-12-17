from PyPDF2 import PdfFileReader, PdfFileWriter

def split_pdf(infn, outfn):
    pdf_input = PdfFileReader(open(infn, 'rb'))
    # 获取 pdf 共用多少页
    page_count = pdf_input.getNumPages()
    print(page_count)
    # out = outfn.split('.')[0]
    # 将 pdf 第五页之后的页面，输出到一个新的文件
    for i in range(0, page_count):
        pdf_output = PdfFileWriter()
        pdf_output.addPage(pdf_input.getPage(i))
        pdf_output.write(open(outfn+'{}.pdf'.format(i), 'wb'))

def merge_pdf(infnList, outfn):
    pdf_output = PdfFileWriter()
    count=0
    for infn in infnList:
        count=count+1
        pdf_input = PdfFileReader(open(infn, 'rb'))
        # 获取 pdf 共用多少页
        page_count = pdf_input.getNumPages()
        print(page_count)
        for i in range(page_count):
            pdf_output.addPage(pdf_input.getPage(i))
    pdf_output.write(open(outfn, 'wb'))




if __name__ == '__main__':
    # inPath =["C:/Users/Anzhi/Desktop/操作系统/封面.pdf","C:/Users/Anzhi/Desktop/操作系统/正文.pdf"]
    # outPath=inPath[0].split('.')[0]+"_result.pdf"
    # split_pdf(inPath, outPath)
    # merge_pdf(inPath,outPath)
    infn="C:\\Users\\Anzhi\\Desktop\\1.pdf"
    split_pdf(infn,infn)