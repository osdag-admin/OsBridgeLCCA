# OsBridgeLCCA

OsBridgeLCCA (Open Source Bridge Life Cycle Cost Assessment) is an open-source software for evaluating the life cycle costs of bridges. It provides a user-friendly interface for cost estimation, traffic analysis, emissions calculations, and financial assessment, supporting decision-making in bridge infrastructure projects.

## Features
- **Life Cycle Cost Analysis (LCCA)**: Calculate total costs over a bridge's lifespan.
- **Traffic Analysis**: Assess vehicle impact and cost implications.
- **Emissions Estimation**: Evaluate environmental impact.
- **Data Visualization**: Generate plots and charts with Plotly.
- **Report Generation**: Export results to PDF, Excel, and LaTeX reports.
- **Cross-Platform**: Supports Windows, macOS, and Linux.
- **Standalone & Web-Based**: Available as a PyQt desktop app and a React-based web application.

## Technology Stack

| Component       | Technology             |
|----------------|------------------------|
| **Backend**    | Django (REST API)      |
| **Database**   | SQLite (desktop), PostgreSQL (web) |
| **API**        | Django REST Framework  |
| **Desktop UI** | PyQt5                  |
| **Web UI**     | React.js               |
| **Visualization** | Plotly, Matplotlib  |
| **Reports**    | PyLaTeX                |
| **Testing**    | pytest                 |
| **Deployment** | Docker, Gunicorn       |
| **Version Control** | GitHub            |

## Installation

### Prerequisites
- **Miniconda** (Recommended for environment management)
- **Python 3.9+**
- **Git**

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/OsBridgeLCCA.git
cd OsBridgeLCCA
```

### 2️⃣ Set Up the Environment
#### **For Linux/macOS**
```sh
bash install.sh
```

#### **For Windows**
```bat
install.bat
```

### 3️⃣ Verify Installation
```sh
python scripts/verify_installation.py
```

## Running the Application

### 🖥️ **Running the Desktop Application**
```sh
python src_web/osbridgelcca/desktop/app.py
```

### 🌐 **Running the Web Application**
#### **Start the Backend Server**
```sh
python src_web/osbridgelcca/backend/manage.py runserver
```
#### **Start the Frontend**
```sh
cd src_web/osbridgelcca/web
npm install
npm start
```

## Directory Structure
```
OsBridgeLCCA/
|-- src/osbridgelcca  # Main source code
|   |-- backend/  # Django backend
|   |-- desktop/  # PyQt5 desktop app
|   |-- web/  # React web app
|   |-- core/  # Core logic for calculations
|-- scripts/  # Utility scripts
|-- tests/  # Unit & integration tests
|-- docs/  # Documentation
|-- LICENSE  # License file
|-- README.md  # Project overview
```

## Contributing
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`.
3. Commit your changes: `git commit -m 'Add new feature'`.
4. Push to your fork: `git push origin feature-branch`.
5. Submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For queries or collaboration, contact: contact-osdag@fossee.in or raise an issue on GitHub.

