from pydantic import BaseModel, Field
from typing import List, Union, Annotated, Type
from pydantic import BaseModel, ValidationError
from datetime import datetime
from typing import Optional
import pandas as pd


class GooglePlaystore(BaseModel):
    app_name: Optional[str]
    app_id: Optional[str]
    category: Optional[str]
    rating: Optional[float]
    rating_count: Optional[float]
    installs: Optional[str]
    free: Optional[bool]
    price: Optional[float]
    size: Optional[str]
    currency: Optional[str]
    timestamp: Optional[datetime]


class DataFrameValidationError(Exception):
    """Custom exception for DataFrame validation errors."""


def validate_dataframe(df: pd.DataFrame, model: Type[BaseModel]):
    """
    Validates each row of a DataFrame against a Pydantic model.
    Raises DataFrameValidationError if any row fails validation.

    :param df: DataFrame to validate.
    :param model: Pydantic model to validate against.
    :raises: DataFrameValidationError
    """
    errors = []

    for i, row in enumerate(df.to_dict(orient="records")):
        try:
            model(**row)
        except ValidationError as e:
            errors.append(f"Row {i} failed validation: {e}")

    if errors:
        error_message = "\n".join(errors)
        raise DataFrameValidationError(
            f"DataFrame validation failed with the following errors:\n{error_message}"
        )
