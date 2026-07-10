from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    source = Column(String(100), nullable=True)
    course_service = Column(String(255), nullable=True)
    stage = Column(String(100), nullable=True)
    gender = Column(String(50), nullable=True)
    location = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    referral_id = Column(Integer, ForeignKey("referrals.id"), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=True)
    contacted_at = Column(DateTime, nullable=True)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    amount = Column(Numeric(12, 2), nullable=True)
    paid_at = Column(DateTime, nullable=True)
    status = Column(String(50), nullable=True)


class SalePaymentRecord(Base):
    __tablename__ = "sales_payment_records"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    invoice_no = Column(String(100), nullable=True)
    due_date = Column(Date, nullable=True)
    amount_due = Column(Numeric(12, 2), nullable=True)
    amount_paid = Column(Numeric(12, 2), nullable=True)
    status = Column(String(50), nullable=True)


class SalePaymentInstallment(Base):
    __tablename__ = "sales_payment_installments"

    id = Column(Integer, primary_key=True, index=True)
    sales_payment_record_id = Column(
        Integer, ForeignKey("sales_payment_records.id"), nullable=True
    )
    installment_no = Column(Integer, nullable=True)
    due_date = Column(Date, nullable=True)
    amount = Column(Numeric(12, 2), nullable=True)
    status = Column(String(50), nullable=True)


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    created_at = Column(DateTime, nullable=True)


class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    source = Column(String(100), nullable=True)

