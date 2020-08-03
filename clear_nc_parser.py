from pdfminer import high_level as pdf_reader

def parse_nc_clear(nc_file):
    nc = {'Nr Nota': '????', 'Data Pregão': '????', 'Corretora': 'Clear', 'Conta': '????', 'Transações': [], 'Líquido Operações': '????', 'Taxas e Corretagens': '????'}

    text = pdf_reader.extract_text(nc_file)
    lines = text.splitlines()
    for j, line in enumerate(lines):
        if line.startswith('Folha') and j+2 < len(lines) and nc['Nr Nota'] == '????':
            nc['Nr Nota'] = lines[j+2]
        
        if line.startswith('Data preg') and j+2 < len(lines) and nc['Data Pregão'] == '????':
            nc['Data Pregão'] = lines[j+2]
        
        if line.startswith('Cliente') and j+1 < len(lines) and nc['Conta'] == '????' and len(lines[j+1]) > 2:
            nc['Conta'] = lines[j+1]
        
        if line.startswith('1-BOVESPA'):
            nc['Transações'].append({'Tipo': '?','Nome Ativo': '?', 'Quantidade': '?', 'Preço':'?'})

        if line.startswith('C/V Tipo') and j+len(nc['Transações']) < len(lines):
            for i in range(len(nc['Transações'])):
                nc['Transações'][i]['Tipo'] = lines[j+i][0]

        if line.startswith('Valor Opera') and j+2+len(nc['Transações']) < len(lines):
            for i in range(len(nc['Transações'])):
                nc['Transações'][i]['Nome Ativo'] = lines[j+i+2]
            tr = 0
            while tr < len(nc['Transações']):
                if lines[j+i].isdecimal():
                    nc['Transações'][tr]['Quantidade'] = int(lines[j+i].replace('.',''))
                    tr = tr + 1
                i = i + 1
            tr = 0
            while tr < len(nc['Transações']):
                if ',' in lines[j+i]:
                    nc['Transações'][tr]['Preço'] = float(lines[j+i].replace('.','').replace(',','.'))
                    tr = tr + 1
                i = i + 1
        
            nc['Líquido Operações'] = 0
            for tr in nc['Transações']:
                if tr['Tipo'] == 'C':
                    nc['Líquido Operações'] = nc['Líquido Operações'] + tr['Quantidade'] * tr['Preço']
                else:
                    nc['Líquido Operações'] = nc['Líquido Operações'] - tr['Quantidade'] * tr['Preço']

        if line.startswith('Total correta') and j+5 < len(lines):
            if lines[-3].startswith('C'):
                nc['Taxas e Corretagens'] = -float(lines[j+5].replace('.','').replace(',','.')) - nc['Líquido Operações']
            else:
                nc['Taxas e Corretagens'] = float(lines[j+5].replace('.','').replace(',','.')) - nc['Líquido Operações']
    return nc