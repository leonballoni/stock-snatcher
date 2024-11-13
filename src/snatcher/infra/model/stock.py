from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from seedwork.infra.defaults import AbstractModel
from seedwork.infra.defaults.base import Base


class StockModel(Base, AbstractModel):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_company_id = Column(Integer, ForeignKey("stock_company.id"), nullable=False)
    status = Column(String, nullable=False)
    purchased_amount = Column(Integer, nullable=False)
    purchased_status = Column(String, nullable=False)
    request_date = Column(Date, nullable=False, index=True)

    stock_company = relationship("StockCompany", back_populates="stocks", uselist=True)
    stock_values = relationship("StockValues", back_populates="stock", uselist=False)
    performance_data = relationship(
        "PerformanceData", back_populates="stock", uselist=False
    )
    competitors = relationship("Competitor", back_populates="stock", uselist=True)


class StockCompany(Base, AbstractModel):
    __tablename__ = "stock_company"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False, index=True)
    url = Column(String, nullable=True)
    sector = Column(String, nullable=True)

    competitors = relationship(
        "Competitor", back_populates="stock_company", uselist=True
    )
    stocks = relationship("StockModel", back_populates="stock_company", uselist=True)


class StockValues(Base, AbstractModel):
    __tablename__ = "stock_values"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_id = Column(Integer, ForeignKey("stock.id"), nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)

    stock = relationship("StockModel", back_populates="stock_values")


class PerformanceData(Base, AbstractModel):
    __tablename__ = "performance_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_id = Column(Integer, ForeignKey("stock.id"), nullable=False)
    five_days = Column(Float, nullable=False)
    one_month = Column(Float, nullable=False)
    three_months = Column(Float, nullable=False)
    year_to_date = Column(Float, nullable=False)
    one_year = Column(Float, nullable=False)

    stock = relationship("StockModel", back_populates="performance_data")


class Competitor(Base, AbstractModel):
    __tablename__ = "competitor"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_id = Column(Integer, ForeignKey("stock.id"), nullable=False)
    stock_company_id = Column(Integer, ForeignKey("stock_company.id"), nullable=False)
    company_name = Column(
        String, nullable=True, comment="No caso de não identificar o stock_company_id"
    )
    currency = Column(String, nullable=False)
    value = Column(Float, nullable=False)

    stock_company = relationship("StockCompany", back_populates="competitors")
    stock = relationship("StockModel", back_populates="competitors")
