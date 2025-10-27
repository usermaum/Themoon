"""
Layout Components

Provides high-level layout management components:
- SessionManager: Centralized session state and service initialization
- PageTemplate: Standard page structure
- TabbedLayout: Tab-based navigation
- ColumnLayout: Multi-column layouts
- SectionLayout: Organized content sections
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
import streamlit as st


class SessionManager:
    """
    Centralized session state and service initialization.

    Manages initialization of database connections, services, and state variables
    to eliminate repetitive initialization code across pages.

    Usage:
        services = SessionManager.init_services(["bean_service", "blend_service"])
        db = services["db"]
        bean_service = services["bean_service"]
    """

    @staticmethod
    def init_services(required_services: List[str]) -> Dict[str, Any]:
        """
        Initialize required services and return them as a dictionary.

        Args:
            required_services: List of service names to initialize
                - "db": Database connection (SQLAlchemy)
                - "bean_service": Bean management service
                - "blend_service": Blend management service
                - "inventory_service": Inventory management service
                - "transaction_service": Transaction management service
                - "report_service": Report generation service
                - "cost_service": Cost calculation service

        Returns:
            Dictionary containing initialized services

        Example:
            >>> services = SessionManager.init_services(["db", "bean_service"])
            >>> db = services["db"]
        """
        # Initialize database connection
        if "db" not in st.session_state:
            from app.services.database import SessionLocal
            st.session_state.db = SessionLocal()

        services = {"db": st.session_state.db}

        # Initialize requested services
        for service_name in required_services:
            if service_name == "bean_service" and "bean_service" not in st.session_state:
                from app.services.bean_service import BeanService
                st.session_state.bean_service = BeanService(st.session_state.db)

            elif service_name == "blend_service" and "blend_service" not in st.session_state:
                from app.services.blend_service import BlendService
                st.session_state.blend_service = BlendService(st.session_state.db)

            elif service_name == "inventory_service" and "inventory_service" not in st.session_state:
                from app.services.inventory_service import InventoryService
                st.session_state.inventory_service = InventoryService(st.session_state.db)

            elif service_name == "transaction_service" and "transaction_service" not in st.session_state:
                from app.services.transaction_service import TransactionService
                st.session_state.transaction_service = TransactionService(st.session_state.db)

            elif service_name == "report_service" and "report_service" not in st.session_state:
                from app.services.report_service import ReportService
                st.session_state.report_service = ReportService(st.session_state.db)

            elif service_name == "cost_service" and "cost_service" not in st.session_state:
                from app.services.cost_service import CostCalculationService
                st.session_state.cost_service = CostCalculationService(st.session_state.db)

        # Add all available services to return dictionary
        if hasattr(st.session_state, 'bean_service'):
            services["bean_service"] = st.session_state.bean_service
        if hasattr(st.session_state, 'blend_service'):
            services["blend_service"] = st.session_state.blend_service
        if hasattr(st.session_state, 'inventory_service'):
            services["inventory_service"] = st.session_state.inventory_service
        if hasattr(st.session_state, 'transaction_service'):
            services["transaction_service"] = st.session_state.transaction_service
        if hasattr(st.session_state, 'report_service'):
            services["report_service"] = st.session_state.report_service
        if hasattr(st.session_state, 'cost_service'):
            services["cost_service"] = st.session_state.cost_service

        return services

    @staticmethod
    def init_page_state(page_name: str, initial_state: Dict[str, Any] = None) -> None:
        """
        Initialize page-specific state variables.

        Args:
            page_name: Name of the page (used as session state prefix)
            initial_state: Dictionary of initial state values
        """
        prefix = f"{page_name}_"

        if initial_state:
            for key, value in initial_state.items():
                state_key = f"{prefix}{key}"
                if state_key not in st.session_state:
                    st.session_state[state_key] = value

    @staticmethod
    def get_page_state(page_name: str, key: str, default: Any = None) -> Any:
        """Get a page-specific state variable."""
        state_key = f"{page_name}_{key}"
        return st.session_state.get(state_key, default)

    @staticmethod
    def set_page_state(page_name: str, key: str, value: Any) -> None:
        """Set a page-specific state variable."""
        state_key = f"{page_name}_{key}"
        st.session_state[state_key] = value


def page_template(
    title: str,
    subtitle: str = None,
    show_refresh: bool = True,
    refresh_callback: Callable = None,
    content_func: Callable = None,
) -> None:
    """
    Standard page template component.

    Provides consistent page structure with header, refresh button, and content area.

    Args:
        title: Page title
        subtitle: Page subtitle (optional)
        show_refresh: Whether to show refresh button
        refresh_callback: Function to call on refresh
        content_func: Function that renders page content

    Example:
        >>> def render_content():
        ...     st.write("Page content here")
        >>> page_template("Dashboard", "System Overview", content_func=render_content)
    """
    # Header
    col1, col2 = st.columns([10, 1])

    with col1:
        st.markdown(f"<h1 style='color: #1F4E78;'>{title}</h1>", unsafe_allow_html=True)
        if subtitle:
            st.markdown(f"<p style='color: #666; font-size: 16px;'>{subtitle}</p>", unsafe_allow_html=True)

    with col2:
        if show_refresh and refresh_callback:
            if st.button("🔄 새로고침", key="page_refresh_btn"):
                refresh_callback()
                st.rerun()

    st.divider()

    # Content
    if content_func:
        content_func()


def tabbed_layout(tabs: Dict[str, Callable], icons: Dict[str, str] = None) -> None:
    """
    Tab-based layout component.

    Creates a tabbed interface with multiple content sections.

    Args:
        tabs: Dictionary of {tab_name: content_function}
        icons: Dictionary of {tab_name: icon_emoji} (optional)

    Example:
        >>> tabs = {
        ...     "목록": lambda: st.write("List content"),
        ...     "추가": lambda: st.write("Add content"),
        ... }
        >>> icons = {"목록": "📋", "추가": "➕"}
        >>> tabbed_layout(tabs, icons)
    """
    # Prepare tab labels with icons
    tab_labels = []
    for tab_name in tabs.keys():
        if icons and tab_name in icons:
            tab_labels.append(f"{icons[tab_name]} {tab_name}")
        else:
            tab_labels.append(tab_name)

    # Create tabs
    tab_objects = st.tabs(tab_labels)

    # Render content in each tab
    for tab, (tab_name, content_func) in zip(tab_objects, tabs.items()):
        with tab:
            content_func()


def column_layout(columns: int, content_funcs: List[Callable]) -> None:
    """
    Multi-column layout component.

    Creates a layout with specified number of columns.

    Args:
        columns: Number of columns
        content_funcs: List of functions that render content in each column

    Example:
        >>> content = [
        ...     lambda: st.write("Column 1"),
        ...     lambda: st.write("Column 2"),
        ...     lambda: st.write("Column 3"),
        ... ]
        >>> column_layout(3, content)
    """
    cols = st.columns(columns)

    for col, content_func in zip(cols, content_funcs):
        with col:
            content_func()


def section_layout(title: str, content_func: Callable, collapsible: bool = False) -> None:
    """
    Section layout component.

    Creates an organized content section with optional collapsible behavior.

    Args:
        title: Section title
        content_func: Function that renders section content
        collapsible: Whether section is collapsible

    Example:
        >>> section_layout("기본 정보", lambda: st.write("Content here"))
    """
    if collapsible:
        with st.expander(f"📋 {title}"):
            content_func()
    else:
        st.subheader(f"📋 {title}")
        content_func()


# Backwards compatibility
PageTemplate = page_template
TabbedLayout = tabbed_layout
ColumnLayout = column_layout
SectionLayout = section_layout
