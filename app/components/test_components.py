"""
Component Integration Tests

This module provides integration tests for all components.
Run with: python -m pytest app/components/test_components.py -v
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import pytest
from dataclasses import dataclass


class TestImports:
    """Test that all components can be imported successfully."""

    def test_import_layout_components(self):
        """Test importing layout components."""
        from app.components.layout import (
            SessionManager,
            page_template,
            tabbed_layout,
            column_layout,
            section_layout,
        )
        assert SessionManager is not None
        assert page_template is not None
        assert tabbed_layout is not None
        assert column_layout is not None
        assert section_layout is not None

    def test_import_ui_components(self):
        """Test importing UI components."""
        from app.components.ui import (
            page_header,
            metrics_card,
            metrics_grid,
            data_table,
            stat_card,
            stats_chart,
            info_box,
        )
        assert page_header is not None
        assert metrics_card is not None
        assert metrics_grid is not None
        assert data_table is not None
        assert stat_card is not None
        assert stats_chart is not None
        assert info_box is not None

    def test_import_form_components(self):
        """Test importing form components."""
        from app.components.forms import (
            FormField,
            text_input,
            number_input,
            select_input,
            multiselect_input,
            checkbox_input,
            form_group,
            crud_form,
            confirm_dialog,
            search_box,
        )
        assert FormField is not None
        assert text_input is not None
        assert number_input is not None
        assert select_input is not None
        assert multiselect_input is not None
        assert checkbox_input is not None
        assert form_group is not None
        assert crud_form is not None
        assert confirm_dialog is not None
        assert search_box is not None

    def test_import_helpers(self):
        """Test importing helper functions."""
        from app.components.helpers import (
            format_number,
            format_currency,
            format_percentage,
            validate_email,
            validate_phone,
            truncate_text,
            calculate_change,
        )
        assert format_number is not None
        assert format_currency is not None
        assert format_percentage is not None
        assert validate_email is not None
        assert validate_phone is not None
        assert truncate_text is not None
        assert calculate_change is not None

    def test_import_from_package(self):
        """Test importing from package __init__."""
        from app.components import (
            SessionManager,
            PageTemplate,
            PageHeader,
            MetricsGrid,
            DataTable,
            FormField,
            TextInput,
            CRUDForm,
            format_number,
            format_currency,
        )
        assert SessionManager is not None
        assert PageTemplate is not None
        assert PageHeader is not None
        assert MetricsGrid is not None
        assert DataTable is not None
        assert FormField is not None
        assert TextInput is not None
        assert CRUDForm is not None
        assert format_number is not None
        assert format_currency is not None


class TestFormField:
    """Test FormField dataclass."""

    def test_create_text_field(self):
        """Test creating text input field."""
        from app.components.forms import FormField

        field = FormField(
            name="username",
            label="사용자명",
            type="text",
            required=True,
            placeholder="username@example.com",
        )

        assert field.name == "username"
        assert field.label == "사용자명"
        assert field.type == "text"
        assert field.required is True

    def test_create_select_field(self):
        """Test creating select field."""
        from app.components.forms import FormField

        field = FormField(
            name="category",
            label="분류",
            type="select",
            options=["A", "B", "C"],
            default="A",
        )

        assert field.name == "category"
        assert field.type == "select"
        assert field.options == ["A", "B", "C"]
        assert field.default == "A"

    def test_invalid_field_type(self):
        """Test that invalid field type raises error."""
        from app.components.forms import FormField

        with pytest.raises(ValueError):
            FormField(
                name="test",
                label="Test",
                type="invalid_type",
            )

    def test_select_field_requires_options(self):
        """Test that select field requires options."""
        from app.components.forms import FormField

        with pytest.raises(ValueError):
            FormField(
                name="category",
                label="분류",
                type="select",
                # Missing options
            )


class TestHelpers:
    """Test helper functions."""

    def test_format_number(self):
        """Test number formatting."""
        from app.components.helpers import format_number

        assert format_number(1234567.89, 2) == "1,234,567.89"
        assert format_number(1000, 0) == "1,000"
        assert format_number(50.5, 1) == "50.5"

    def test_format_currency(self):
        """Test currency formatting."""
        from app.components.helpers import format_currency

        assert format_currency(1000, "₩") == "₩1,000"
        assert format_currency(1234567, "₩", 0) == "₩1,234,567"

    def test_format_percentage(self):
        """Test percentage formatting."""
        from app.components.helpers import format_percentage

        assert format_percentage(75.5) == "75.5%"
        assert format_percentage(50, 0) == "50%"

    def test_validate_email(self):
        """Test email validation."""
        from app.components.helpers import validate_email

        assert validate_email("user@example.com") is True
        assert validate_email("invalid.email") is False
        assert validate_email("test@domain.co.kr") is True

    def test_validate_phone(self):
        """Test phone number validation."""
        from app.components.helpers import validate_phone

        assert validate_phone("010-1234-5678") is True
        assert validate_phone("02-123-4567") is False  # Wrong format
        assert validate_phone("01012345678") is False  # Missing dashes

    def test_truncate_text(self):
        """Test text truncation."""
        from app.components.helpers import truncate_text

        long_text = "This is a very long text that should be truncated"
        result = truncate_text(long_text, 20)

        assert len(result) <= 20
        assert result.endswith("...")

    def test_calculate_change(self):
        """Test change calculation."""
        from app.components.helpers import calculate_change

        # Positive change
        change, direction = calculate_change(120, 100)
        assert change == 20.0
        assert direction == "up"

        # Negative change
        change, direction = calculate_change(80, 100)
        assert change == 20.0
        assert direction == "down"

        # No change
        change, direction = calculate_change(100, 100)
        assert change == 0.0
        assert direction == "neutral"

    def test_batch_list(self):
        """Test list batching."""
        from app.components.helpers import batch_list

        result = batch_list([1, 2, 3, 4, 5], 2)
        assert result == [[1, 2], [3, 4], [5]]

        result = batch_list([1, 2, 3, 4], 2)
        assert result == [[1, 2], [3, 4]]

    def test_flatten_dict(self):
        """Test dictionary flattening."""
        from app.components.helpers import flatten_dict

        nested = {"a": {"b": 1, "c": 2}, "d": 3}
        result = flatten_dict(nested)

        assert result == {"a_b": 1, "a_c": 2, "d": 3}

    def test_deep_merge_dict(self):
        """Test deep dictionary merging."""
        from app.components.helpers import deep_merge_dict

        base = {"a": 1, "b": {"c": 2}}
        override = {"b": {"d": 3}, "e": 4}
        result = deep_merge_dict(base, override)

        assert result == {"a": 1, "b": {"c": 2, "d": 3}, "e": 4}


class TestComponentCompatibility:
    """Test component compatibility and naming."""

    def test_backwards_compatibility_names(self):
        """Test that old function names still work."""
        from app.components.layout import PageTemplate, TabbedLayout, ColumnLayout
        from app.components.ui import (
            PageHeader,
            MetricsCard,
            MetricsGrid,
            DataTable,
            StatCard,
            StatsChart,
        )
        from app.components.forms import (
            FormGroup,
            TextInput,
            SelectInput,
            MultiSelectInput,
            CRUDForm,
            ConfirmDialog,
        )

        # These are function aliases for backwards compatibility
        assert PageTemplate is not None
        assert TabbedLayout is not None
        assert ColumnLayout is not None
        assert PageHeader is not None
        assert MetricsCard is not None
        assert MetricsGrid is not None
        assert DataTable is not None
        assert StatCard is not None
        assert StatsChart is not None
        assert FormGroup is not None
        assert TextInput is not None
        assert SelectInput is not None
        assert MultiSelectInput is not None
        assert CRUDForm is not None
        assert ConfirmDialog is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
