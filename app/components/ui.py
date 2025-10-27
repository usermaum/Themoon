"""
UI Components

Provides display and visualization components:
- PageHeader: Page title with refresh button
- MetricsCard: Single metric display
- MetricsGrid: Grid of metrics
- DataTable: Data display with filtering and selection
- StatCard: Statistics card with icon
- StatsChart: Chart display wrapper
"""

from typing import List, Dict, Any, Tuple, Optional, Callable
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


def page_header(
    title: str,
    subtitle: str = None,
    show_refresh: bool = True,
    refresh_callback: Callable = None,
) -> None:
    """
    Page header component with title and optional refresh button.

    Args:
        title: Page title
        subtitle: Page subtitle (optional)
        show_refresh: Whether to show refresh button
        refresh_callback: Callback function for refresh button

    Example:
        >>> page_header("원두 관리", "모든 원두의 가격을 관리합니다")
    """
    col1, col2 = st.columns([10, 1])

    with col1:
        st.markdown(f"<h1 style='color: #1F4E78;'>{title}</h1>", unsafe_allow_html=True)
        if subtitle:
            st.markdown(
                f"<p style='color: #666; font-size: 16px;'>{subtitle}</p>",
                unsafe_allow_html=True,
            )

    with col2:
        if show_refresh and refresh_callback:
            if st.button("🔄", key="page_refresh_btn", help="페이지 새로고침"):
                refresh_callback()
                st.rerun()

    st.divider()


def metrics_card(
    label: str,
    value: Any,
    delta: str = None,
    delta_color: str = "normal",  # "normal", "off", "inverse"
    icon: str = None,
    width: Optional[int] = None,
) -> None:
    """
    Single metric card component.

    Args:
        label: Metric label
        value: Metric value
        delta: Change indicator
        delta_color: Color of delta ("normal", "off", "inverse")
        icon: Emoji icon
        width: Optional column width

    Example:
        >>> metrics_card("총 로스팅", 25, "↑ 5", "off", "☕")
    """
    if icon:
        display_label = f"{icon} {label}"
    else:
        display_label = label

    st.metric(
        label=display_label,
        value=value,
        delta=delta,
        delta_color=delta_color,
    )


def metrics_grid(
    metrics: List[Dict[str, Any]],
    columns: int = 5,
) -> None:
    """
    Grid of metrics cards.

    Args:
        metrics: List of metric dictionaries with keys:
            - label: Metric label
            - value: Metric value
            - delta: Optional change indicator
            - icon: Optional emoji icon
        columns: Number of columns in grid

    Example:
        >>> metrics = [
        ...     {"label": "총 로스팅", "value": 25, "delta": "↑ 5", "icon": "☕"},
        ...     {"label": "평균 비용", "value": "2,500원", "icon": "💰"},
        ... ]
        >>> metrics_grid(metrics, columns=3)
    """
    cols = st.columns(columns)

    for idx, metric in enumerate(metrics):
        col_idx = idx % columns

        with cols[col_idx]:
            icon = metric.get("icon")
            label = metric.get("label", "")
            value = metric.get("value")
            delta = metric.get("delta")

            if icon:
                display_label = f"{icon} {label}"
            else:
                display_label = label

            st.metric(
                label=display_label,
                value=value,
                delta=delta,
            )


def data_table(
    data: pd.DataFrame,
    columns: List[str] = None,
    searchable: bool = True,
    selectable: bool = False,
    height: int = 400,
    key: str = None,
) -> Tuple[pd.DataFrame, List[int]]:
    """
    Data table component with optional search and selection.

    Args:
        data: DataFrame to display
        columns: Specific columns to show (all if None)
        searchable: Whether to show search box
        selectable: Whether rows are selectable
        height: Table height in pixels
        key: Streamlit component key

    Returns:
        Tuple of (filtered_data, selected_indices)

    Example:
        >>> df = pd.DataFrame({"이름": ["A", "B"], "가격": [100, 200]})
        >>> filtered_df, selected = data_table(df, searchable=True)
    """
    # Select columns
    if columns:
        display_data = data[columns].copy()
    else:
        display_data = data.copy()

    # Search filter
    search_term = ""
    if searchable:
        search_term = st.text_input(
            "🔍 검색",
            "",
            key=f"table_search_{key}" if key else "table_search",
        )

    # Apply search filter
    if search_term:
        mask = display_data.astype(str).apply(
            lambda x: x.str.contains(search_term, case=False).any(),
            axis=1,
        )
        filtered_data = display_data[mask]
    else:
        filtered_data = display_data

    # Display table
    st.dataframe(
        filtered_data,
        height=height,
        key=f"table_display_{key}" if key else "table_display",
        use_container_width=True,
    )

    # Return filtered data and indices
    selected_indices = list(range(len(filtered_data)))

    return filtered_data, selected_indices


def stat_card(
    title: str,
    value: str,
    description: str = None,
    icon: str = None,
    color: str = "#1F4E78",
) -> None:
    """
    Statistics card with icon and description.

    Args:
        title: Card title
        value: Main value to display
        description: Optional description
        icon: Optional emoji icon
        color: Color of title

    Example:
        >>> stat_card("총 판매량", "1,234 kg", "지난 달 기준", "📦")
    """
    icon_str = f"{icon} " if icon else ""

    html = f"""
    <div style='
        padding: 15px;
        border-radius: 8px;
        background-color: #f0f2f6;
        border-left: 4px solid {color};
    '>
        <h3 style='color: {color}; margin: 0 0 5px 0;'>{icon_str}{title}</h3>
        <h2 style='color: {color}; margin: 10px 0;'>{value}</h2>
        {f"<p style='color: #666; margin: 0;'>{description}</p>" if description else ""}
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


def stats_chart(
    title: str,
    figure: go.Figure = None,
    chart_func: Callable = None,
    height: int = 400,
) -> None:
    """
    Chart display component.

    Args:
        title: Chart title
        figure: Plotly figure object (or use chart_func)
        chart_func: Function that returns Plotly figure
        height: Chart height in pixels

    Example:
        >>> import plotly.graph_objects as go
        >>> fig = go.Figure(data=[go.Bar(x=[1,2], y=[3,4])])
        >>> stats_chart("판매량 추이", figure=fig)
    """
    st.subheader(f"📊 {title}")

    # Get figure from either parameter or function
    if chart_func:
        fig = chart_func()
    else:
        fig = figure

    if fig:
        fig.update_layout(height=height)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("차트 데이터가 없습니다.")


def info_box(
    message: str,
    box_type: str = "info",  # "info", "success", "warning", "error"
    icon: str = None,
) -> None:
    """
    Information box component.

    Args:
        message: Message to display
        box_type: Type of box
        icon: Optional custom icon

    Example:
        >>> info_box("처리가 완료되었습니다", "success", "✅")
    """
    if icon:
        display_message = f"{icon} {message}"
    else:
        display_message = message

    if box_type == "success":
        st.success(display_message)
    elif box_type == "warning":
        st.warning(display_message)
    elif box_type == "error":
        st.error(display_message)
    else:
        st.info(display_message)


def progress_bar(
    current: float,
    total: float,
    label: str = None,
    percentage: bool = True,
) -> None:
    """
    Progress bar component.

    Args:
        current: Current value
        total: Total value
        label: Optional label
        percentage: Whether to show percentage

    Example:
        >>> progress_bar(75, 100, "진행률", True)
    """
    progress = current / total if total > 0 else 0

    if label:
        if percentage:
            st.write(f"{label}: {progress*100:.1f}%")
        else:
            st.write(f"{label}: {current}/{total}")

    st.progress(min(progress, 1.0))


def empty_state(
    message: str,
    icon: str = "📭",
    action_label: str = None,
    action_callback: Callable = None,
) -> None:
    """
    Empty state component for when no data is available.

    Args:
        message: Message to display
        icon: Icon emoji
        action_label: Optional action button label
        action_callback: Optional callback for action button

    Example:
        >>> empty_state("데이터가 없습니다", "📭", "데이터 추가", lambda: st.write("Adding..."))
    """
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(f"<h3 style='text-align: center;'>{icon}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align: center; color: #666;'>{message}</h4>", unsafe_allow_html=True)

        if action_label and action_callback:
            if st.button(action_label, use_container_width=True):
                action_callback()


# Backwards compatibility
PageHeader = page_header
MetricsCard = metrics_card
MetricsGrid = metrics_grid
DataTable = data_table
StatCard = stat_card
StatsChart = stats_chart
