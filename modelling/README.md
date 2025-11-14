# Modelling Eurostat Data

## Prerequisites

Make sure you have the following installed:
- [Python 3.8+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)

## How to Run the Notebook

### 1. Clone the Repository
```bash
git clone https://github.com/Grena30/Exploratory-Data-Analysis
cd Exploratory-Data-Analysis/Modelling
```

### 2. Create and Activate a Virtual Environment

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch Jupyter Notebook
**If Jupyter is not yet installed, install it with:**
```bash
pip install jupyter
```
**Then run:**
```bash
jupyter notebook
```

**Alternatively, you can use VSCode's interface to open the notebooks**

### 5. Project structure

**model.ipynb** - code related to data imputation, feature selection, model training/evaluation
