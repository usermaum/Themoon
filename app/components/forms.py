"""
Form Components

Provides input and form handling components:
- FormField: Data class for form field definitions
- TextInput: Text input component
- SelectInput: Select dropdown component
- MultiSelectInput: Multi-select dropdown component
- FormGroup: Group of form fields
- CRUDForm: Complete CRUD form component
- ConfirmDialog: Confirmation dialog component
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
import streamlit as st
import pandas as pd


@dataclass
class FormField:
    """
    Data class for form field definition.

    Attributes:
        name: Field name (used as key)
        label: Display label
        type: Field type ("text", "number", "select", "multiselect", "date", "textarea", "checkbox")
        required: Whether field is required
        options: List of options (for select/multiselect types)
        placeholder: Placeholder text
        default: Default value
        validation: Optional validation function
        helper_text: Helper text to display below field
        min_value: Minimum value (for number type)
        max_value: Maximum value (for number type)
        regex_pattern: Regex pattern for validation
    """

    name: str
    label: str
    type: str = "text"
    required: bool = True
    options: List[Any] = field(default_factory=list)
    placeholder: str = None
    default: Any = None
    validation: Callable = None
    helper_text: str = None
    min_value: float = None
    max_value: float = None
    regex_pattern: str = None

    def __post_init__(self):
        """Validate field configuration."""
        valid_types = ["text", "number", "select", "multiselect", "date", "textarea", "checkbox"]
        if self.type not in valid_types:
            raise ValueError(f"Invalid type: {self.type}. Must be one of {valid_types}")

        if self.type in ["select", "multiselect"] and not self.options:
            raise ValueError(f"{self.type} field must have options")


def text_input(
    field: FormField,
    key: str = None,
) -> Any:
    """
    Text input component.

    Args:
        field: FormField configuration
        key: Streamlit component key

    Returns:
        User input value

    Example:
        >>> field = FormField("name", "이름", type="text")
        >>> value = text_input(field)
    """
    required_indicator = " *" if field.required else ""
    label = f"{field.label}{required_indicator}"

    component_key = key or f"input_{field.name}"

    value = st.text_input(
        label=label,
        placeholder=field.placeholder or "",
        value=field.default or "",
        key=component_key,
    )

    if field.helper_text:
        st.caption(f"💡 {field.helper_text}")

    # Validation
    if field.required and not value:
        st.error(f"{field.label}은(는) 필수 항목입니다")
        return None

    if field.regex_pattern:
        import re
        if not re.match(field.regex_pattern, str(value)):
            st.error(f"{field.label} 형식이 올바르지 않습니다")
            return None

    if field.validation:
        try:
            field.validation(value)
        except ValueError as e:
            st.error(str(e))
            return None

    return value


def number_input(
    field: FormField,
    key: str = None,
) -> Any:
    """
    Number input component.

    Args:
        field: FormField configuration (type must be "number")
        key: Streamlit component key

    Returns:
        Numeric value

    Example:
        >>> field = FormField("price", "가격", type="number", min_value=0)
        >>> value = number_input(field)
    """
    required_indicator = " *" if field.required else ""
    label = f"{field.label}{required_indicator}"

    component_key = key or f"number_{field.name}"

    value = st.number_input(
        label=label,
        value=float(field.default) if field.default else 0.0,
        min_value=float(field.min_value) if field.min_value else None,
        max_value=float(field.max_value) if field.max_value else None,
        key=component_key,
    )

    if field.helper_text:
        st.caption(f"💡 {field.helper_text}")

    return value


def select_input(
    field: FormField,
    key: str = None,
) -> Any:
    """
    Select dropdown component.

    Args:
        field: FormField configuration
        key: Streamlit component key

    Returns:
        Selected value

    Example:
        >>> field = FormField("category", "분류", type="select", options=["A", "B", "C"])
        >>> value = select_input(field)
    """
    required_indicator = " *" if field.required else ""
    label = f"{field.label}{required_indicator}"

    component_key = key or f"select_{field.name}"

    value = st.selectbox(
        label=label,
        options=field.options,
        index=0 if field.default is None else field.options.index(field.default),
        key=component_key,
    )

    if field.helper_text:
        st.caption(f"💡 {field.helper_text}")

    if field.required and not value:
        st.error(f"{field.label}은(는) 필수 항목입니다")
        return None

    return value


def multiselect_input(
    field: FormField,
    key: str = None,
) -> List[Any]:
    """
    Multi-select dropdown component.

    Args:
        field: FormField configuration
        key: Streamlit component key

    Returns:
        List of selected values

    Example:
        >>> field = FormField("tags", "태그", type="multiselect", options=["A", "B", "C"])
        >>> values = multiselect_input(field)
    """
    required_indicator = " *" if field.required else ""
    label = f"{field.label}{required_indicator}"

    component_key = key or f"multiselect_{field.name}"

    default = field.default if isinstance(field.default, list) else []

    values = st.multiselect(
        label=label,
        options=field.options,
        default=default,
        key=component_key,
    )

    if field.helper_text:
        st.caption(f"💡 {field.helper_text}")

    if field.required and not values:
        st.error(f"{field.label}은(는) 필수 항목입니다")
        return None

    return values


def checkbox_input(
    field: FormField,
    key: str = None,
) -> bool:
    """
    Checkbox input component.

    Args:
        field: FormField configuration
        key: Streamlit component key

    Returns:
        Boolean value

    Example:
        >>> field = FormField("agree", "동의합니다", type="checkbox")
        >>> value = checkbox_input(field)
    """
    component_key = key or f"checkbox_{field.name}"

    value = st.checkbox(
        label=field.label,
        value=bool(field.default),
        key=component_key,
    )

    if field.helper_text:
        st.caption(f"💡 {field.helper_text}")

    return value


def form_group(
    fields: List[FormField],
    columns: int = 1,
    form_key: str = None,
) -> Dict[str, Any]:
    """
    Form group component containing multiple fields.

    Args:
        fields: List of FormField definitions
        columns: Number of columns for layout
        form_key: Key for Streamlit form container

    Returns:
        Dictionary of field values

    Example:
        >>> fields = [
        ...     FormField("name", "이름"),
        ...     FormField("email", "이메일"),
        ... ]
        >>> values = form_group(fields, columns=2)
    """
    values = {}
    cols = st.columns(columns) if columns > 1 else [st]

    for idx, field_config in enumerate(fields):
        col_idx = idx % columns
        col = cols[col_idx]

        with col:
            if field_config.type == "text":
                values[field_config.name] = text_input(field_config)
            elif field_config.type == "number":
                values[field_config.name] = number_input(field_config)
            elif field_config.type == "select":
                values[field_config.name] = select_input(field_config)
            elif field_config.type == "multiselect":
                values[field_config.name] = multiselect_input(field_config)
            elif field_config.type == "checkbox":
                values[field_config.name] = checkbox_input(field_config)
            elif field_config.type == "textarea":
                required_indicator = " *" if field_config.required else ""
                label = f"{field_config.label}{required_indicator}"
                values[field_config.name] = st.text_area(
                    label=label,
                    value=field_config.default or "",
                    placeholder=field_config.placeholder or "",
                )
            elif field_config.type == "date":
                required_indicator = " *" if field_config.required else ""
                label = f"{field_config.label}{required_indicator}"
                values[field_config.name] = st.date_input(label=label)

    return values


def crud_form(
    title: str,
    fields: List[FormField],
    on_submit: Callable,
    initial_data: Dict[str, Any] = None,
    edit_mode: bool = False,
    columns: int = 2,
) -> None:
    """
    Complete CRUD form component.

    Args:
        title: Form title
        fields: List of FormField definitions
        on_submit: Callback function on form submission
        initial_data: Initial form data (for edit mode)
        edit_mode: Whether form is in edit mode
        columns: Number of columns for field layout

    Example:
        >>> fields = [
        ...     FormField("name", "원두명"),
        ...     FormField("price", "가격", type="number"),
        ... ]
        >>> def on_submit(data):
        ...     print(f"Submitted: {data}")
        >>> crud_form("원두 추가", fields, on_submit)
    """
    st.subheader(title)

    # Update field defaults with initial data
    if initial_data:
        for field_config in fields:
            if field_config.name in initial_data:
                field_config.default = initial_data[field_config.name]

    # Form container
    with st.form(key=f"form_{title.replace(' ', '_')}", clear_on_submit=True):
        # Render form fields
        form_data = form_group(fields, columns=columns)

        # Submit button
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button(
                label="✅ 저장" if edit_mode else "➕ 추가",
                use_container_width=True,
            )

        with col2:
            st.form_submit_button(
                label="❌ 취소",
                use_container_width=True,
            )

        # Handle submission
        if submitted:
            # Filter out None values (from validation failures)
            valid_data = {k: v for k, v in form_data.items() if v is not None}

            if len(valid_data) == len(fields):  # All fields valid
                on_submit(valid_data)
                st.success(f"{'수정' if edit_mode else '추가'}되었습니다!")


def confirm_dialog(
    title: str,
    message: str,
    on_confirm: Callable,
    on_cancel: Callable = None,
    confirm_label: str = "확인",
    cancel_label: str = "취소",
) -> None:
    """
    Confirmation dialog component.

    Args:
        title: Dialog title
        message: Dialog message
        on_confirm: Callback on confirmation
        on_cancel: Callback on cancellation
        confirm_label: Confirm button label
        cancel_label: Cancel button label

    Example:
        >>> confirm_dialog(
        ...     "삭제 확인",
        ...     "정말 삭제하시겠습니까?",
        ...     on_confirm=lambda: print("Confirmed"),
        ... )
    """
    st.warning(f"⚠️ {title}")
    st.write(message)

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"✅ {confirm_label}", use_container_width=True):
            on_confirm()

    with col2:
        if st.button(f"❌ {cancel_label}", use_container_width=True):
            if on_cancel:
                on_cancel()


def search_box(
    placeholder: str = "검색...",
    key: str = None,
) -> str:
    """
    Search input component.

    Args:
        placeholder: Placeholder text
        key: Component key

    Returns:
        Search query

    Example:
        >>> query = search_box("원두 검색")
    """
    return st.text_input(
        label="🔍",
        placeholder=placeholder,
        key=key or "search_box",
    )


# Backwards compatibility
FormGroup = form_group
TextInput = text_input
SelectInput = select_input
MultiSelectInput = multiselect_input
CRUDForm = crud_form
ConfirmDialog = confirm_dialog
