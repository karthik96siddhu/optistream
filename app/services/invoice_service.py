import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from app.models.order import Order

class InvoiceService:

    @staticmethod
    def generate_pdf_invoice(order: Order) -> str:
        """"
        Generates a PDF invoice locally on the server.
        Returns the absolute local file path of the generated PDF.
        """

        # Ensure a temporary directory exists to hold local files
        output_dirs = '/tmp/invoices'
        os.makedirs(output_dirs, exist_ok=True)
        file_path = f"{output_dirs}/invoice_order_{order.id}.pdf"

        # Initiatize the document structure 
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        story = []

        # configure typography and styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'InvoiceTitle',
            parent=styles['Heading1'],
            fontSize=24,
            leading=28,
            spaceAfter=20
        )

        # Construct PDF content programatically
        story.append(Paragraph(f"INVOICE FOR ORDER #{order.id}", title_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"<b>Customer Email:</b> {order.customer_email}", styles['Normal']))
        story.append(Paragraph(f"<b>Product SKU:</b> {order.product_sku}", styles['Normal']))
        story.append(Paragraph(f"<b>Quantity:</b> {order.quantity}", styles['Normal']))
        story.append(Paragraph(f"<b>Total amount paid:</b> ${order.total_price}", styles['Normal']))
        story.append(Spacer(1,20))
        story.append(Paragraph("Thank you for your purchase!", styles['Italic']))

        # Build and render the document
        doc.build(story)

        print(f"[BACKGROUND WORKER] PDF successfully compiled at : {file_path}")
        return file_path