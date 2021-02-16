from reportlab.lib.units import mm
from reportlab.graphics.barcode import *
from reportlab.graphics.shapes import Drawing, String

class MyBarcodeDrawing(Drawing):
    def __init__(self, text_value, *args, **kw):
        barcode = createBarcodeDrawing('Code128', value=text_value, barHeight=10*mm, humanReadable=True)
        Drawing.__init__(self,barcode.width,barcode.height,*args,**kw)
        self.add(barcode, name='barcode')


