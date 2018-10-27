from PyPDF2 import PdfFileReader, PdfFileWriter

def split_pdf(infn, outfn):
    pdf_output = PdfFileWriter()
    pdf_input = PdfFileReader(open(infn, 'rb'))
    # 获取 pdf 共用多少页
    page_count = pdf_input.getNumPages()
    print(page_count)
    # 将 pdf 第五页之后的页面，输出到一个新的文件
    for i in range(0, page_count):
        pdf_output.addPage(pdf_input.getPage(i))
    pdf_output.write(open(outfn, 'wb'))

def merge_pdf(infnList, outfn):
    pdf_output = PdfFileWriter()
    for infn in infnList:
        pdf_input = PdfFileReader(open(infn, 'rb'))
        # 获取 pdf 共用多少页
        page_count = pdf_input.getNumPages()
        print(page_count)
        for i in range(page_count):
            pdf_output.addPage(pdf_input.getPage(i))
    pdf_output.write(open(outfn, 'wb'))




if __name__ == '__main__':
    inPath =["C:/Users/Anzhi/Desktop/Rademacher1.pdf","C:/Users/Anzhi/Desktop/Rademacher2.pdf"
            ,"C:/Users/Anzhi/Desktop/Rademacher3.pdf","C:/Users/Anzhi/Desktop/Rademacher4.pdf"
            ,"C:/Users/Anzhi/Desktop/svm11.pdf"]
    outPath=inPath[0].split('.')[0]+"_result.pdf"
    # split_pdf(inPath, outPath)
    merge_pdf(inPath[0:4],outPath)