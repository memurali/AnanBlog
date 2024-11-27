# from borb.pdf.document import Document
from borb.pdf import Document
from borb.pdf.page.page import Page
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from decimal import Decimal
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable as Table
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.layout.layout_element import Alignment
from datetime import datetime
import random
from borb.pdf.pdf import PDF
from borb.pdf.canvas.color.color import HexColor, X11Color
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable as Table
from borb.pdf.canvas.layout.table.table import TableCell
from .models import *


def _build_itemized_description_table(inv_id):

    items = invoice_items.objects.filter(invoice_id=inv_id)
    invoice = Inoice.objects.get(id=inv_id)

    item_list = []

    total = 0
    for item in items:
        item_list.append((item.item_name, item.qty, item.unit_price))
        total += item.amount

    total_discounts = total * (invoice.discounts/100)
    total_taxes = total * (invoice.taxes/100)
    sub_total = (total - total_discounts) + total_taxes

    print(len(item_list))

    num_row = len(item_list) + 5
    num_min = num_row - 5

    table_001 = Table(number_of_rows=num_row, number_of_columns=4)  
    for h in ["DESCRIPTION", "QTY", "UNIT PRICE", "AMOUNT"]:  
        table_001.add(  
            TableCell(  
                Paragraph(h, font_color=X11Color("White")),  
                background_color=HexColor("016934"),  
            )  
        )
  
    odd_color = HexColor("BBBBBB")  
    even_color = HexColor("FFFFFF")  
    for row_number, item in enumerate(item_list):  
        c = even_color if row_number % 2 == 0 else odd_color  
        table_001.add(TableCell(Paragraph(item[0]), background_color=c))  
        table_001.add(TableCell(Paragraph(str(item[1])), background_color=c))  
        table_001.add(TableCell(Paragraph("$ " + str(item[2])), background_color=c))  
        table_001.add(TableCell(Paragraph("$ " + str(item[1] * item[2])), background_color=c))  
	  
	# Optionally add some empty rows to have a fixed number of rows for styling purposes
    for row_number in range(num_row, num_min):  
        c = even_color if row_number % 2 == 0 else odd_color  
        for _ in range(0, 4):  
            table_001.add(TableCell(Paragraph(" "), background_color=c))  
  
    table_001.add(TableCell(Paragraph("Subtotal", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT,), col_span=3,))  
    table_001.add(TableCell(Paragraph(f"$ {total}", horizontal_alignment=Alignment.RIGHT)))  
    table_001.add(TableCell(Paragraph("Discounts", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT,),col_span=3,))  
    table_001.add(TableCell(Paragraph(f"$ %.2f" % total_discounts, horizontal_alignment=Alignment.RIGHT)))  
    table_001.add(TableCell(Paragraph("Taxes", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT), col_span=3,))  
    table_001.add(TableCell(Paragraph(f"$ %.2f" % total_taxes, horizontal_alignment=Alignment.RIGHT)))  
    table_001.add(TableCell(Paragraph("Total", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT  ), col_span=3,))  
    table_001.add(TableCell(Paragraph(f"$ %.2f" % sub_total, horizontal_alignment=Alignment.RIGHT)))  
    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))  
    table_001.no_borders()  
    return table_001


def _build_billing_and_shipping_information(inv_id):

    invoice = Inoice.objects.get(id=inv_id)

    table_001 = Table(number_of_rows=7, number_of_columns=1)  
    table_001.add(  
        Paragraph(  
            "BILL TO",  
            background_color=HexColor("ff9800"),  
            font_color=X11Color("White"),  
        )  
    )  
    # table_001.add(  
    #     Paragraph(  
    #         "SHIP TO",  
    #         background_color=HexColor("263238"),  
    #         font_color=X11Color("White"),  
    #     )  
    # )  
    # table_001.add(Paragraph("[Recipient Name]"))          
    table_001.add(Paragraph(invoice.invoice_receipt.receipt_name))         
    table_001.add(Paragraph(invoice.invoice_receipt.company_name))            
    # table_001.add(Paragraph("[Company Name]"))           
    # table_001.add(Paragraph("[Street Address]"))          
    table_001.add(Paragraph(invoice.invoice_receipt.street_address))         
    table_001.add(Paragraph(f"{invoice.invoice_receipt.city}, {invoice.invoice_receipt.state}, {invoice.invoice_receipt.receipt_zip}, "))   
    # table_001.add(Paragraph("[City, State, ZIP Code]"))  
    # table_001.add(Paragraph("[Phone]"))                   
    table_001.add(Paragraph(invoice.invoice_receipt.phone))                  
    table_001.add(Paragraph(invoice.invoice_receipt.email))                  
    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))  
    table_001.no_borders()  
    return table_001


def _build_invoice_information(
    inv_id,

):

    invoice = Inoice.objects.get(id=inv_id)

    table_001 = Table(number_of_rows=6, number_of_columns=3)

    table_001.add(Paragraph(invoice.invoice_sender.sender_name))    
    table_001.add(Paragraph(" "))
    table_001.add(Paragraph(" "))
	
    table_001.add(Paragraph(invoice.invoice_sender.street_address))    
    table_001.add(Paragraph("Date", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))    
    now = datetime.now()    
    table_001.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year)))
	
    table_001.add(Paragraph(f"{invoice.invoice_sender.city}, {invoice.invoice_sender.state}, {invoice.invoice_sender.sender_zip}, "))     
    table_001.add(Paragraph("Due Date", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))

    table_001.add(Paragraph(invoice.due_date))
	
    table_001.add(Paragraph(invoice.invoice_sender.phone)) 
    table_001.add(Paragraph(" "))
    table_001.add(Paragraph(" "))
	
    table_001.add(Paragraph(invoice.invoice_sender.email))    
    table_001.add(Paragraph(" "))
    table_001.add(Paragraph(" "))

    table_001.add(Paragraph(invoice.invoice_sender.company_website))
    table_001.add(Paragraph(" "))
    table_001.add(Paragraph(" "))

    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))    		
    table_001.no_borders()
    return table_001

def createInvoice(
    inv_id,
    companyLogo=" ",
    inv_num=random.randint(1000, 10000),
    order_num=" ",
):
    # Create document
    pdf = Document()

    # Add page
    page = Page()
    pdf.append_page(page)

    page_layout = SingleColumnLayout(page)

    try:
        if companyLogo == " " or companyLogo == "":
            pass
        else:
            
            page_layout.vertical_margin = page.get_page_info().get_height() * Decimal(0.02)
            page_layout.add(    
                Image(        
                    companyLogo,        
                    width=Decimal(128),        
                    height=Decimal(128),    
                ))
    except :
        pass

        
    page_layout.add(Paragraph(f"Invoice # {inv_num}", font="Helvetica-Bold", font_size=20, horizontal_alignment=Alignment.RIGHT))
    page_layout.add(Paragraph(f"Order # {order_num}", font="Helvetica-Bold", font_size=20, horizontal_alignment=Alignment.RIGHT))

    # Invoice information table  
    page_layout.add(_build_invoice_information(
        inv_id
    ))  

    # Empty paragraph for spacing  
    page_layout.add(Paragraph(" "))

    # Billing and shipping information table
    page_layout.add(_build_billing_and_shipping_information(inv_id))

    # Empty paragraph for spacing  
    page_layout.add(Paragraph(" "))

    # Itemized description
    page_layout.add(_build_itemized_description_table(inv_id))

    with open(f"static/images/invoices/{inv_num}.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, pdf)

    # return pdf


# createInvoice(companyLogo="https://s3.stackabuse.com/media/articles/creating-an-invoice-in-python-with-ptext-1.png")