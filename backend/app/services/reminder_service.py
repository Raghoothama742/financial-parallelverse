from datetime import date, datetime, timedelta
import calendar
from typing import List, Dict, Any, Tuple
from .emi_calculator import EMICalculator, round_curr

def add_months_clamped(orig_date: date, months_to_add: int, preferred_day: int) -> date:
    """Safely calculates future dates accounting for differing month lengths (28, 29, 30, 31)."""
    new_year = orig_date.year + (orig_date.month - 1 + months_to_add) // 12
    new_month = ((orig_date.month - 1 + months_to_add) % 12) + 1
    max_days = calendar.monthrange(new_year, new_month)[1]
    clamped_day = min(preferred_day, max_days)
    return date(new_year, new_month, clamped_day)

class ReminderService:
    @staticmethod
    def generate_installment_schedule(
        purchase_name: str,
        total_amount: float,
        down_payment: float,
        annual_interest_rate: float,
        tenure_months: int,
        start_date: date,
        due_day: int
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Creates loan repayment schedule and generates exact calendar due dates.
        """
        emi_calc = EMICalculator.calculate_emi(
            purchase_price=total_amount,
            down_payment=down_payment,
            annual_interest_rate=annual_interest_rate,
            tenure_months=tenure_months
        )

        payments = []
        today = date.today()

        for item in emi_calc["schedule"]:
            m_idx = item["month"]
            due_d = add_months_clamped(start_date, m_idx - 1, due_day)
            
            # Initial status
            status = "PENDING"
            if due_d < today:
                status = "OVERDUE"

            payments.append({
                "installment_number": m_idx,
                "due_date": due_d,
                "emi_amount": item["payment_amount"],
                "principal_portion": item["principal_paid"],
                "interest_portion": item["interest_paid"],
                "remaining_balance": item["remaining_balance"],
                "status": status,
                "notes": f"Installment {m_idx} of {tenure_months} for {purchase_name}"
            })

        return emi_calc, payments

    @staticmethod
    def update_overdue_statuses(payments: List[Any], today: date = None) -> None:
        """Flags pending payments whose due date has passed as OVERDUE."""
        if today is None:
            today = date.today()
        for p in payments:
            if p.status == "PENDING" and p.due_date < today:
                p.status = "OVERDUE"

    @staticmethod
    def generate_ics_calendar(plan_name: str, payments: List[Any]) -> str:
        """
        Generates standard iCalendar (.ics) RFC 5545 file content
        for importing reminders into Google Calendar, Apple Calendar, or Outlook.
        """
        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Financial Parallelverse//FinTech Reminders//EN",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
            f"X-WR-CALNAME:{plan_name} EMI Reminders"
        ]

        now_str = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

        for p in payments:
            d = p.due_date
            dtstart = f"{d.year:04d}{d.month:02d}{d.day:02d}T090000"
            dtend = f"{d.year:04d}{d.month:02d}{d.day:02d}T100000"
            uid = f"emi-{getattr(p, 'id', 'p')}-{p.installment_number}-{d.strftime('%Y%m%d')}@financial-parallelverse.local"

            lines.extend([
                "BEGIN:VEVENT",
                f"UID:{uid}",
                f"DTSTAMP:{now_str}",
                f"DTSTART:{dtstart}",
                f"DTEND:{dtend}",
                f"SUMMARY:EMI Payment: {plan_name} (₹{p.emi_amount:,.2f})",
                f"DESCRIPTION:Installment #{p.installment_number} due for {plan_name}. Amount: ₹{p.emi_amount:,.2f}. Status: {p.status}.",
                "STATUS:CONFIRMED",
                "BEGIN:VALARM",
                "TRIGGER:-P1D",
                "ACTION:DISPLAY",
                f"DESCRIPTION:Reminder: EMI of ₹{p.emi_amount:,.2f} due tomorrow for {plan_name}",
                "END:VALARM",
                "END:VEVENT"
            ])

        lines.append("END:VCALENDAR")
        return "\r\n".join(lines)
