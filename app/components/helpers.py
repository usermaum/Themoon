"""
Helper Functions

Provides utility functions for formatting, validation, and data processing.
"""

import re
from typing import Any, List, Dict, Tuple
from datetime import datetime, date
import pandas as pd


def format_number(
    value: float,
    decimal_places: int = 0,
    use_thousands_separator: bool = True,
) -> str:
    """
    Format number with optional thousands separator.

    Args:
        value: Number to format
        decimal_places: Number of decimal places
        use_thousands_separator: Whether to use comma separator

    Returns:
        Formatted number string

    Example:
        >>> format_number(1234567.89, 2)
        '1,234,567.89'
    """
    if value is None:
        return "0"

    if use_thousands_separator:
        return f"{value:,.{decimal_places}f}"
    else:
        return f"{value:.{decimal_places}f}"


def format_currency(
    value: float,
    currency: str = "₩",
    decimal_places: int = 0,
) -> str:
    """
    Format currency value.

    Args:
        value: Value to format
        currency: Currency symbol
        decimal_places: Number of decimal places

    Returns:
        Formatted currency string

    Example:
        >>> format_currency(1234567, "₩", 0)
        '₩1,234,567'
    """
    formatted = format_number(value, decimal_places, use_thousands_separator=True)
    return f"{currency}{formatted}"


def format_percentage(
    value: float,
    decimal_places: int = 1,
) -> str:
    """
    Format percentage value.

    Args:
        value: Value (0-100)
        decimal_places: Number of decimal places

    Returns:
        Formatted percentage string

    Example:
        >>> format_percentage(75.5)
        '75.5%'
    """
    return f"{value:.{decimal_places}f}%"


def format_date(
    value: date,
    format: str = "%Y-%m-%d",
) -> str:
    """
    Format date value.

    Args:
        value: Date object
        format: Date format string

    Returns:
        Formatted date string

    Example:
        >>> format_date(date(2025, 10, 27))
        '2025-10-27'
    """
    if isinstance(value, str):
        return value
    if value is None:
        return ""

    return value.strftime(format)


def parse_date(value: str, format: str = "%Y-%m-%d") -> date:
    """
    Parse date string to date object.

    Args:
        value: Date string
        format: Date format

    Returns:
        Date object

    Example:
        >>> parse_date("2025-10-27")
        date(2025, 10, 27)
    """
    return datetime.strptime(value, format).date()


def validate_email(email: str) -> bool:
    """
    Validate email address format.

    Args:
        email: Email address to validate

    Returns:
        True if valid, False otherwise

    Example:
        >>> validate_email("user@example.com")
        True
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format (Korean format).

    Args:
        phone: Phone number to validate

    Returns:
        True if valid, False otherwise

    Example:
        >>> validate_phone("010-1234-5678")
        True
    """
    pattern = r'^01[0-9]-\d{3,4}-\d{4}$'
    return bool(re.match(pattern, phone))


def truncate_text(
    text: str,
    max_length: int = 50,
    suffix: str = "...",
) -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add

    Returns:
        Truncated text

    Example:
        >>> truncate_text("This is a very long text", 10)
        'This is ...'
    """
    if len(text) > max_length:
        return text[:max_length - len(suffix)] + suffix
    return text


def highlight_text(text: str, pattern: str) -> str:
    """
    Highlight matching pattern in text.

    Args:
        text: Text to highlight
        pattern: Pattern to search for

    Returns:
        HTML string with highlighting

    Example:
        >>> highlight_text("Hello World", "World")
        'Hello <mark>World</mark>'
    """
    highlighted = text.replace(pattern, f"<mark>{pattern}</mark>")
    return highlighted


def calculate_change(
    current: float,
    previous: float,
) -> Tuple[float, str]:
    """
    Calculate change between two values.

    Args:
        current: Current value
        previous: Previous value

    Returns:
        Tuple of (change_percentage, change_direction)

    Example:
        >>> calculate_change(120, 100)
        (20.0, 'up')
    """
    if previous == 0:
        return 0.0, "neutral"

    change = ((current - previous) / previous) * 100

    if change > 0:
        direction = "up"
    elif change < 0:
        direction = "down"
    else:
        direction = "neutral"

    return abs(change), direction


def get_trend_emoji(change: float, direction: str) -> str:
    """
    Get emoji representing trend.

    Args:
        change: Change value
        direction: Change direction ('up', 'down', 'neutral')

    Returns:
        Emoji string

    Example:
        >>> get_trend_emoji(10.5, "up")
        '📈'
    """
    if direction == "up":
        return "📈"
    elif direction == "down":
        return "📉"
    else:
        return "➡️"


def dataframe_to_list(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Convert DataFrame to list of dictionaries.

    Args:
        df: DataFrame to convert

    Returns:
        List of row dictionaries

    Example:
        >>> df = pd.DataFrame({"name": ["A", "B"]})
        >>> dataframe_to_list(df)
        [{"name": "A"}, {"name": "B"}]
    """
    return df.to_dict(orient="records")


def list_to_dataframe(data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Convert list of dictionaries to DataFrame.

    Args:
        data: List of row dictionaries

    Returns:
        DataFrame

    Example:
        >>> data = [{"name": "A"}, {"name": "B"}]
        >>> list_to_dataframe(data)
    """
    return pd.DataFrame(data)


def filter_dataframe(
    df: pd.DataFrame,
    filters: Dict[str, Any],
) -> pd.DataFrame:
    """
    Filter DataFrame by multiple conditions.

    Args:
        df: DataFrame to filter
        filters: Dictionary of column:value filters

    Returns:
        Filtered DataFrame

    Example:
        >>> df = pd.DataFrame({"status": ["A", "B", "A"]})
        >>> filter_dataframe(df, {"status": "A"})
    """
    result = df.copy()

    for column, value in filters.items():
        if column in result.columns:
            if isinstance(value, list):
                result = result[result[column].isin(value)]
            else:
                result = result[result[column] == value]

    return result


def sort_dataframe(
    df: pd.DataFrame,
    column: str,
    ascending: bool = True,
) -> pd.DataFrame:
    """
    Sort DataFrame by column.

    Args:
        df: DataFrame to sort
        column: Column name to sort by
        ascending: Sort order

    Returns:
        Sorted DataFrame

    Example:
        >>> df = pd.DataFrame({"price": [100, 50, 75]})
        >>> sort_dataframe(df, "price", ascending=True)
    """
    return df.sort_values(by=column, ascending=ascending)


def get_summary_stats(df: pd.DataFrame, columns: List[str] = None) -> Dict[str, Dict[str, float]]:
    """
    Get summary statistics for numeric columns.

    Args:
        df: DataFrame
        columns: Specific columns to summarize (all if None)

    Returns:
        Dictionary of column statistics

    Example:
        >>> df = pd.DataFrame({"price": [100, 200, 300]})
        >>> get_summary_stats(df, ["price"])
    """
    if columns is None:
        columns = df.select_dtypes(include=['number']).columns.tolist()

    stats = {}
    for column in columns:
        if column in df.columns:
            stats[column] = {
                "count": df[column].count(),
                "mean": df[column].mean(),
                "std": df[column].std(),
                "min": df[column].min(),
                "max": df[column].max(),
                "sum": df[column].sum(),
            }

    return stats


def create_color_gradient(value: float, min_val: float, max_val: float) -> str:
    """
    Create color gradient based on value.

    Args:
        value: Value to color
        min_val: Minimum value
        max_val: Maximum value

    Returns:
        Hex color string

    Example:
        >>> create_color_gradient(50, 0, 100)
        '#7FFF00'
    """
    # Normalize value to 0-1 range
    normalized = (value - min_val) / (max_val - min_val) if max_val > min_val else 0.5

    # Create gradient from red to green
    red = int(255 * (1 - normalized))
    green = int(255 * normalized)
    blue = 0

    return f"#{red:02X}{green:02X}{blue:02X}"


def batch_list(lst: List[Any], batch_size: int) -> List[List[Any]]:
    """
    Split list into batches.

    Args:
        lst: List to batch
        batch_size: Size of each batch

    Returns:
        List of batches

    Example:
        >>> batch_list([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
    """
    batches = []
    for i in range(0, len(lst), batch_size):
        batches.append(lst[i:i + batch_size])
    return batches


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    """
    Flatten nested dictionary.

    Args:
        d: Dictionary to flatten
        parent_key: Parent key prefix
        sep: Separator for keys

    Returns:
        Flattened dictionary

    Example:
        >>> flatten_dict({"a": {"b": 1}})
        {'a_b': 1}
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def deep_merge_dict(base: Dict, override: Dict) -> Dict:
    """
    Deep merge two dictionaries.

    Args:
        base: Base dictionary
        override: Override dictionary

    Returns:
        Merged dictionary

    Example:
        >>> deep_merge_dict({"a": 1, "b": {"c": 2}}, {"b": {"d": 3}})
        {'a': 1, 'b': {'c': 2, 'd': 3}}
    """
    result = base.copy()

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dict(result[key], value)
        else:
            result[key] = value

    return result
