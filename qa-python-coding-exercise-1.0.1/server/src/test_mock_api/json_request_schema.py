from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class Data(BaseModel):
    product_name: str
    product_type: str
    product_version: int


class Overall(BaseModel):
    duration: float
    result: str


class RuleA1(BaseModel):
    duration: float
    result: str


class RuleA2(BaseModel):
    duration: float
    result: str


class Decision(BaseModel):
    ruleA1: Optional[RuleA1] = None
    ruleA2: Optional[RuleA2] = None


class Additional(BaseModel):
    overall: Overall
    decisions: List[Decision]


class JsonModel(BaseModel):
    format: str
    data: Data
    additional: Additional