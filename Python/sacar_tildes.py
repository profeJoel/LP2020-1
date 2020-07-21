import codecs

archivo = codecs.open("Python/lemario-general-del-espanol.txt","r","utf-8")
"""
trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'),None)
for x in archivo:
    print(">> "+normalize('NFKC', normalize('NFKD',archivo.readline().translate(trans_tab))))
"""

a,b = 'áéíóúü','aeiouu'
trans = str.maketrans(a,b)
for x in archivo:
    print(">> "+archivo.readline().translate(trans))
