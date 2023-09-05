from typing import Optional

from pydantic import BaseModel


# Классы на основе базовой модели
class DataOptimization(BaseModel):
    name: Optional[str]
    variables: Optional[str]
    matrix: Optional[str]
    obj: Optional[str]
    options: Optional[str]


class Optmizers(BaseModel):
    name: Optional[str]
    description: Optional[str]

