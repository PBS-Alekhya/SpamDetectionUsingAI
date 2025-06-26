from pydantic import BaseModel, ValidationError, conlist
from typing import List

class ConfigSchema(BaseModel):
    model_name: str
    version: str
    confidence_threshold: float
    labels: conlist(str, min_length=2, max_length=2)
    log_predictions: bool
