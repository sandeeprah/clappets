import pdfkit

options = {
'page-size' : 'A4',
'margin-top':'25mm',
'margin-bottom':'19mm',
'margin-left':'19mm',
'margin-right':'19mm',
'encoding':'UTF-8',
'print-media-type' : None,
'header-html' : 'header.html',
'header-spacing' : '5',
'footer-left' : "template_url : http://www.clappets.com/htm/document/tpl/mec/dat/pmp/c01/",
'footer-line' : None,
'footer-font-size' : '8',
'footer-font-name' : 'Calibri',
'footer-spacing' : '5',
'disable-smart-shrinking' : None,
}

toc = {
'xsl-style-sheet' : 'toc.xsl'
}

cover = 'cover.html'

pdfkit.from_url('http://127.0.0.1:5000/htm/document/db/1122-mec-dat-pmp-c01-1/', 'out.pdf',options=options)
# pdfkit.from_url('http://127.0.0.1:5000/test/demo/', 'out.pdf',options=options,  toc=toc, cover=cover, cover_first=True)
