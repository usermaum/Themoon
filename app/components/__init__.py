"""
Reusable Components Module for The Moon Roasting Cost Calculator

This module provides a comprehensive set of reusable UI, Form, and Layout components
to reduce code duplication and ensure consistency across all pages.

Components are organized into three categories:
1. UI Components - Display elements (headers, metrics, tables, charts)
2. Form Components - Input and form handling
3. Layout Components - Page structure and layout management
"""

# Layout Components
from .layout import SessionManager, PageTemplate, TabbedLayout, ColumnLayout, SectionLayout

# UI Components
from .ui import (
    PageHeader,
    MetricsCard,
    MetricsGrid,
    DataTable,
    StatCard,
    StatsChart,
)

# Form Components
from .forms import (
    FormField,
    TextInput,
    SelectInput,
    MultiSelectInput,
    FormGroup,
    CRUDForm,
    ConfirmDialog,
)

# Helpers
from .helpers import format_number, format_currency, validate_email

__all__ = [
    # Layout
    "SessionManager",
    "PageTemplate",
    "TabbedLayout",
    "ColumnLayout",
    "SectionLayout",
    # UI
    "PageHeader",
    "MetricsCard",
    "MetricsGrid",
    "DataTable",
    "StatCard",
    "StatsChart",
    # Forms
    "FormField",
    "TextInput",
    "SelectInput",
    "MultiSelectInput",
    "FormGroup",
    "CRUDForm",
    "ConfirmDialog",
    # Helpers
    "format_number",
    "format_currency",
    "validate_email",
]

__version__ = "1.0.0"
__author__ = "The Moon Roasting Cost Calculator Team"
