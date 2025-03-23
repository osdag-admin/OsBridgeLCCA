import importlib
import sys
sys.stdout.reconfigure(encoding='utf-8')

# List of required packages
REQUIRED_PACKAGES = [
    "django",
    "djangorestframework",
    "pyqt5",
    "plotly",
    "pylatex",
    "pytest",
    "matplotlib",
    "pandas",
    "numpy",
    "sqlite3",
    "psycopg2",
    "requests",
    "flask",
    "gunicorn"
]


def check_package(package):
    """Check if a package is installed."""
    try:
        importlib.import_module(package)
        print(f"[✔] {package} is installed.")
    except ImportError:
        print(f"[✖] {package} is MISSING. Install it using `pip install {package}`")


def main():
    print("\n=== Verifying Installation ===\n")

    # Check each package
    for package in REQUIRED_PACKAGES:
        check_package(package)

    # Check Python version
    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 9:
        print(f"\n[✔] Python {python_version.major}.{python_version.minor} detected.")
    else:
        print(f"\n[✖] Python 3.9+ is required. Detected: {python_version.major}.{python_version.minor}")

    print("\nVerification complete!\n")


if __name__ == "__main__":
    main()
