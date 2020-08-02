from pdfminer import high_level as pdf_reader

text = pdf_reader.extract_text('sample.pdf')

with open('output2.txt','w') as fp:
    fp.write(text)

