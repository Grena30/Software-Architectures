from typing import Optional
from sqlmodel import SQLModel, Field


class GDPGrowthModel(SQLModel):
    gdp_per_capita: int = Field(default=None)
    unemployment_rate: int = Field(default=None)
    gdp_growth_rate_lag: int = Field(default=None)
    gdp_growth_rate_ma: int = Field(default=None)


class InflationModel(SQLModel):
    inflation_rate_lag: int = Field(default=None)
    inflation_rate_monthly: int = Field(default=None)
    unemployment_rate: int = Field(default=None)


class UnemploymentModel(SQLModel):
    unemployment_rate_lag: int = Field(default=None)
    gdp_growth_rate_ma: int = Field(default=None)
