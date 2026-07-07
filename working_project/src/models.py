from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from sqlalchemy import Numeric, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class WeatherModel(BaseModel):
    """
    pydantic fields data is  validated against 
    """

    
    pressure: Decimal = Field(max_digits=12, decimal_places=4)   
    geopheight: Decimal = Field(max_digits=12, decimal_places=4)
    temperature: Decimal = Field(max_digits=12, decimal_places=4)
    dewpoint: Decimal = Field(max_digits=12, decimal_places=4)   
    humidity: Decimal = Field(max_digits=12, decimal_places=4)   
    winddirection: Decimal = Field(max_digits=12, decimal_places=4)   
    windspeedms: Decimal = Field(max_digits=12, decimal_places=4)   
    windums: Decimal = Field(max_digits=12, decimal_places=4)   
    windvms: Decimal = Field(max_digits=12, decimal_places=4)   
    precipitationamount: Decimal = Field(max_digits=12, decimal_places=4)   
    totalcloudcover: Decimal = Field(max_digits=12, decimal_places=4)   
    lowcloudcover: Decimal = Field(max_digits=12, decimal_places=4)   
    mediumcloudcover: Decimal = Field(max_digits=12, decimal_places=4)   
    highcloudcover: Decimal = Field(max_digits=12, decimal_places=4)   
    radiationglobal: Decimal = Field(max_digits=12, decimal_places=4)   
    radiationglobalaccumulation: Decimal = Field(max_digits=12, decimal_places=4)   
    radiationnetsurfaceswaccumulation: Decimal = Field(max_digits=12, decimal_places=4)   
    radiationswaccumulation: Decimal = Field(max_digits=12, decimal_places=4)   
    visibility: Decimal = Field(max_digits=12, decimal_places=4)   
    windgust: Decimal = Field(max_digits=12, decimal_places=4)   
    timestamps: datetime  
    




# sqlalchemy



class Base(DeclarativeBase):
    pass

class WeatherTable(Base):
    """
    orm model that is persisted in the sql data base
    """


    __tablename__ = 'weather_table'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)   
    pressure: Mapped[Decimal] = mapped_column(Numeric(12, 4))   
    geopheight: Mapped[Decimal] = mapped_column(Numeric(12, 4))
    temperature: Mapped[Decimal] = mapped_column(Numeric(12, 4))
    dewpoint: Mapped[Decimal] = mapped_column(Numeric(12, 4))   
    humidity: Mapped[Decimal] = mapped_column(Numeric(12, 4))   
    winddirection: Mapped[Decimal] = mapped_column(Numeric(12, 4))   
    windspeedms: Mapped[Decimal] = mapped_column(Numeric(12, 4))   
    windums: Mapped[Decimal] = mapped_column(Numeric(12, 4))   
    windvms: Mapped[Decimal] = mapped_column(Numeric(12, 4))   
    precipitationamount: Mapped[Decimal] = mapped_column(Numeric(12, 4))   
    totalcloudcover: Mapped[Decimal] = mapped_column(Numeric(12, 4))   
    lowcloudcover: Mapped[Decimal] = mapped_column(Numeric(12, 4))   
    mediumcloudcover: Mapped[Decimal] = mapped_column(Numeric(12, 4))   
    highcloudcover: Mapped[Decimal] = mapped_column(Numeric(12, 4))   
    radiationglobal: Mapped[Decimal] = mapped_column(Numeric(12, 4))   
    radiationglobalaccumulation: Mapped[Decimal] = mapped_column(Numeric(12, 4))   
    radiationnetsurfaceswaccumulation: Mapped[Decimal] = mapped_column(Numeric(12, 4))   
    radiationswaccumulation: Mapped[Decimal] = mapped_column(Numeric(12, 4))   
    visibility: Mapped[Decimal] = mapped_column(Numeric(12, 4))   
    windgust: Mapped[Decimal] = mapped_column(Numeric(12, 4))   
    timestamps: Mapped[datetime] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())