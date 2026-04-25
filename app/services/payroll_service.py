from sqlmodel import Session
from app.models.payroll import Payroll
from app.schemas.payroll_schema import PayrollInput

PF_WAGE_CEILING = 15000
PF_RATE = 0.12

def calculate_tds(annual_taxable: float) -> float:
    if annual_taxable <= 400000:
        return 0
    elif annual_taxable <= 800000:
        tax = (annual_taxable - 400000) * 0.05
    elif annual_taxable <= 1200000:
        tax = (400000 * 0.05) + (annual_taxable - 800000) * 0.10
    elif annual_taxable <= 1600000:
        tax = (400000 * 0.05) + (400000 * 0.10) + (annual_taxable - 1200000) * 0.15
    elif annual_taxable <= 2000000:
        tax = (400000 * 0.05) + (400000 * 0.10) + (400000 * 0.15) + (annual_taxable - 1600000) * 0.20
    else:
        tax = (400000 * 0.05) + (400000 * 0.10) + (400000 * 0.15) + (400000 * 0.20) + (annual_taxable - 2000000) * 0.30
    return round(tax / 12, 2)

def validate_and_calculate_payroll(data: PayrollInput, session: Session):
    basic = data.basic
    da = data.da
    ctc = data.ctc
    was_adjusted = False
    is_fifty_rule_violated = False

    if basic + da < 0.5 * ctc:
        is_fifty_rule_violated = True
        basic = ctc * 0.4
        da = ctc * 0.1
        was_adjusted = True

    pf_base = min(basic, PF_WAGE_CEILING)
    pf_employee = round(pf_base * PF_RATE, 2)
    pf_employer = round(pf_base * PF_RATE, 2)

    monthly_gross = ctc / 12
    annual_taxable = (monthly_gross - pf_employee) * 12
    tds = calculate_tds(annual_taxable)

    gross_salary = round(monthly_gross, 2)
    net_salary = round(gross_salary - pf_employee - tds, 2)

    payroll = Payroll(
        employee_id=data.employee_id,
        month=data.month,
        year=data.year,
        ctc=ctc,
        basic=basic,
        da=da,
        pf_employee=pf_employee,
        pf_employer=pf_employer,
        tds=tds,
        gross_salary=gross_salary,
        net_salary=net_salary,
        is_fifty_rule_violated=is_fifty_rule_violated,
        was_adjusted=was_adjusted,
        status="processed"
    )
    session.add(payroll)
    session.commit()
    session.refresh(payroll)
    return payroll