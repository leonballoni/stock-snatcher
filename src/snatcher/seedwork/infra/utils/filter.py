from datetime import date, datetime
from sqlalchemy.orm import Query
from sqlalchemy import text
from seedwork.infra.schemas.pagination import PydanticModel


class Filtering:

    def __init__(self, query: Query, input_schema: PydanticModel):
        self.query: Query = query
        self.input_schema: PydanticModel = input_schema
        self.input_dict: dict = input_schema.model_dump(
            exclude={"page", "page_size"}, exclude_none=True
        )
        if self.input_dict:
            self._filter_conditions()
            self._add_filter()

    def _add_filter(self) -> None:
        "Generate the filtered query"
        self.query = self.query.filter(
            text(self.filter_result).params(self.filter_value)
        )

    @property
    def filter_result(self):
        return self.filters.get("filter")

    @property
    def filter_value(self):
        return self.filters.get("values")

    def _filter_conditions(self) -> dict:
        """
        Main function that generates filter conditions and parameter values.
        """
        filter_conditions = []
        values = {}

        for i, (key, value) in enumerate(self.input_dict.items()):
            param_key = f"value_{i}"
            condition, param_value = self._get_condition_for_type(key, value, param_key)
            if condition:
                filter_conditions.append(condition)
                values[param_key] = param_value

        # Join conditions into a filter string
        filter_str = " AND ".join(filter_conditions) if filter_conditions else ""
        self.filters = {"filter": filter_str, "values": values}

    def _get_condition_for_type(self, key: str, value, param_key: str) -> tuple:
        """
        Returns the SQL condition and parameter value based on the type of the value.
        This function can be easily extended for more types.
        """
        if isinstance(value, (int, float, bool)):
            return f"{key} = :{param_key}", value

        elif isinstance(value, str):
            # Handles pattern matching for strings
            return f"{key} LIKE :{param_key}", f"%{value}%"

        elif isinstance(value, (date, datetime)):
            # Handles date and datetime comparisons
            return f"{key} >= :{param_key}", value

        else:
            # Unsupported data type
            raise ValueError(f"Unsupported data type for key: {key}, value: {value}")
