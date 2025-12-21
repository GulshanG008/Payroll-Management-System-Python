# reports/pdf_generator.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import datetime


def generate_payslip_pdf(
    file_path,
    emp_id,
    emp_name,
    salary_month,
    basic_salary,
    hra,
    da,
    pf,
    tax,
    gross_salary,
    net_salary
):
    """
    Generates a professional payslip PDF.

    :param file_path: Full path where PDF will be saved
    :param emp_id: Employee ID
    :param emp_name: Employee Name
    :param salary_month: Salary Month (e.g., March-2025)
    :param basic_salary: Basic Salary
    :param hra: House Rent Allowance
    :param da: Dearness Allowance
    :param pf: Provident Fund deduction
    :param tax: Tax deduction
    :param gross_salary: Total earnings
    :param net_salary: Final salary after deductions
    """

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # ---------- HEADER ----------
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 2 * cm, "PAYSLIP")

    c.setFont("Helvetica", 10)
    c.drawCentredString(
        width / 2,
        height - 2.7 * cm,
        "Payroll Management System"
    )

    # ---------- EMPLOYEE DETAILS ----------
    c.setFont("Helvetica", 11)
    y = height - 4 * cm

    c.drawString(2 * cm, y, f"Employee ID   : {emp_id}")
    c.drawString(2 * cm, y - 0.7 * cm, f"Employee Name : {emp_name}")
    c.drawString(2 * cm, y - 1.4 * cm, f"Salary Month  : {salary_month}")
    c.drawString(
        2 * cm,
        y - 2.1 * cm,
        f"Generated On  : {datetime.now().strftime('%d-%m-%Y')}"
    )

    # ---------- LINE ----------
    c.line(2 * cm, y - 2.8 * cm, width - 2 * cm, y - 2.8 * cm)

    # ---------- SALARY DETAILS ----------
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y - 3.8 * cm, "Earnings")
    c.drawString(11 * cm, y - 3.8 * cm, "Deductions")

    c.setFont("Helvetica", 11)

    # Earnings
    c.drawString(2 * cm, y - 4.8 * cm, f"Basic Salary : ₹ {basic_salary}")
    c.drawString(2 * cm, y - 5.6 * cm, f"HRA          : ₹ {hra}")
    c.drawString(2 * cm, y - 6.4 * cm, f"DA           : ₹ {da}")

    # Deductions
    c.drawString(11 * cm, y - 4.8 * cm, f"Provident Fund : ₹ {pf}")
    c.drawString(11 * cm, y - 5.6 * cm, f"Tax            : ₹ {tax}")

    # ---------- TOTALS ----------
    c.setFont("Helvetica-Bold", 12)
    c.line(2 * cm, y - 7.2 * cm, width - 2 * cm, y - 7.2 * cm)

    c.drawString(2 * cm, y - 8.2 * cm, f"Gross Salary : ₹ {gross_salary}")
    c.drawString(11 * cm, y - 8.2 * cm, f"Net Salary : ₹ {net_salary}")

    # ---------- FOOTER ----------
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(
        width / 2,
        2 * cm,
        "This is a system generated payslip. No signature required."
    )

    c.showPage()
    c.save()
