from typing import Optional
from sqlmodel import SQLModel, Field


class GDPGrowthModel(SQLModel):
    gdp_per_capita: float = Field(default=0.0)
    unemployment_rate: float = Field(default=0.0)
    gdp_growth_rate_lag: float = Field(default=0.0)
    gdp_growth_rate_ma: float = Field(default=0.0)


class InflationModel(SQLModel):
    inflation_rate_lag: float = Field(default=0.0)
    inflation_rate_monthly: float = Field(default=0.0)
    unemployment_rate: float = Field(default=0.0)


class UnemploymentModel(SQLModel):
    unemployment_rate_lag: float = Field(default=0.0)
    gdp_growth_rate_ma: float = Field(default=0.0)
