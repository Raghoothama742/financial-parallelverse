import pytest
from datetime import date
from backend.app.services.reminder_service import ReminderService, add_months_clamped

def test_add_months_clamped_month_ends():
    # Jan 31 -> Feb 28/29
    d1 = add_months_clamped(date(2026, 1, 31), 1, 31)
    assert d1.month == 2
    assert d1.day in (28, 29)

    # March 31 -> April 30
    d2 = add_months_clamped(date(2026, 3, 31), 1, 31)
    assert d2.month == 4
    assert d2.day == 30

def test_generate_installment_schedule():
    calc, payments = ReminderService.generate_installment_schedule(
        purchase_name="Smart TV",
        total_amount=40000.0,
        down_payment=10000.0,
        annual_interest_rate=12.0,
        tenure_months=6,
        start_date=date(2026, 11, 1),
        due_day=5
    )
    assert len(payments) == 6
    assert payments[0]["due_date"] == date(2026, 11, 5)
    assert payments[1]["due_date"] == date(2026, 12, 5)
    assert payments[0]["installment_number"] == 1
    assert payments[-1]["installment_number"] == 6

def test_generate_ics_calendar():
    _, payments = ReminderService.generate_installment_schedule(
        purchase_name="iPad Air",
        total_amount=50000.0,
        down_payment=10000.0,
        annual_interest_rate=10.0,
        tenure_months=3,
        start_date=date(2026, 11, 1),
        due_day=10
    )
    # mock objects
    class MockPayment:
        def __init__(self, d):
            self.id = d["installment_number"]
            self.installment_number = d["installment_number"]
            self.due_date = d["due_date"]
            self.emi_amount = d["emi_amount"]
            self.status = d["status"]

    mock_objs = [MockPayment(p) for p in payments]
    ics = ReminderService.generate_ics_calendar("iPad Air", mock_objs)
    assert "BEGIN:VCALENDAR" in ics
    assert "END:VCALENDAR" in ics
    assert "iPad Air" in ics
    assert "BEGIN:VEVENT" in ics
