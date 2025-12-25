import sys
try:
    from app.api.deps import get_current_active_superuser
    print("Import OK")
except ImportError as e:
    print(f"Import Failed: {e}")
    sys.exit(1)
