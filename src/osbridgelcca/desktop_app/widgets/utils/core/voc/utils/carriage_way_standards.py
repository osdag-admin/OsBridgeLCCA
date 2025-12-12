from dataclasses import dataclass
from types import MappingProxyType
from typing import Optional, Tuple, List, Union

@dataclass(frozen=True)
class CarriagewayStandards:
    """
    Manages standard carriageway widths for different road types.

    Methods:
    - list_types(): Returns available carriageway types and usage note.
    - get_width(type_name, custom_width=None): Retrieves width for a given type, with type checks.
    """

    _STANDARD_WIDTHS: MappingProxyType = MappingProxyType({
        "SL": 3.75,
        "IL": 5.50,
        "2L": 7.00,
        "4L": 2 * 3.5,
        "6L": 3 * 3.5,
        "8L": 4 * 3.5,
        "EW": None,  # custom input required
    })

    NOTE: str = (
        "Note: 'Expressway (custom width required)' requires user input. "
        "Carriageway width represents the total width of the roadway for vehicular traffic."
    )

    @classmethod
    def list_types(cls) -> Tuple[List[str], str]:
        """
        List all available carriageway types with a usage note.

        Returns:
            tuple: (list of carriageway type names, usage note)
        """
        return list(cls._STANDARD_WIDTHS.keys()), cls.NOTE

    @classmethod
    def get_width(cls, type_name: str, custom_width: Optional[Union[int, float]] = None) -> Tuple[Optional[float], str]:
        """
        Retrieve the width for a given carriageway type, with input type validation.

        Args:
            type_name (str): Name of the carriageway type.
            custom_width (float or int, optional): Custom width for expressways.

        Returns:
            tuple: (width in meters or None, message string)
        """
        # Check type_name
        if not isinstance(type_name, str):
            return None, f"Error: 'type_name' must be a string, got {type(type_name).__name__}."

        if type_name not in cls._STANDARD_WIDTHS:
            return None, f"Error: Unknown carriageway type '{type_name}'."

        width = cls._STANDARD_WIDTHS[type_name]

        # Standard width available
        if width is not None:
            return width, "Standard width applied."

        # Custom width required (Expressway)
        if custom_width is None:
            return None, (
                "Custom width required for this type. "
                "Please provide a width in meters (float or int). "
                "Carriageway width represents the total width of the roadway for vehicular traffic."
            )

        # Validate custom_width type
        if not isinstance(custom_width, (int, float)):
            return None, f"Error: 'custom_width' must be a number (int or float), got {type(custom_width).__name__}."

        # Validate positive width
        if custom_width <= 0:
            return None, "Error: 'custom_width' must be a positive number."

        return float(custom_width), "Custom expressway width applied."
