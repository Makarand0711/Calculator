# 🧮 Smart Calculator

A professional, feature-rich command-line calculator application written in Python. Designed using clean architecture, Object-Oriented Programming (OOP) principles, modular design, and robust exception handling. This project is optimized for interview portfolios and is fully open-source.

---

## 🌟 Features

### 📐 Comprehensive Operations
- **Basic Math**: Addition, Subtraction, Multiplication, Division, Modulus, Floor Division.
- **Advanced Algebra**: Power (Exponentiation), Square Root, Absolute Value, Factorials, Percentages.
- **Logarithmic**: Natural Logarithm (base $e$) and custom base logarithms.
- **Trigonometric**: Sine, Cosine, and Tangent (supports both Degree and Radian modes).

### 📜 History Management
- **Automatic Logging**: Every calculation is logged with a unique sequential ID, operation name, inputs, result, and timestamp.
- **Data Persistence**: Records are saved in JSON format (`history.json`).
- **Graceful Recovery**: Automatically detects and recovers from corrupted JSON history files by backing them up and creating a clean state.
- **Data Export**: Export calculation history directly into a standard CSV spreadsheet file.

### 🛡️ Robust Validation & Error Handling
- Prevents division/modulo/floor-division by zero with user-friendly warnings.
- Gracefully handles negative square roots and invalid/fractional factorials.
- Validates user input to prevent program crashes due to invalid numbers or menu options.

---

## 📂 Project Structure

```text
SmartCalculator/
│
├── main.py                 # Application entry point & CLI interactive loop
├── calculator.py           # Core math logic & validation (Calculator class)
├── history.py              # History serialization, persistence, & CSV exports
├── utils.py                # Command-line presentation styles & input validators
├── history.json            # Persistent storage for calculations (auto-generated)
├── requirements.txt        # Development dependencies (pytest)
├── README.md               # Extensive project documentation
├── LICENSE                 # MIT License details
├── .gitignore              # Files excluded from git tracking
└── tests/
    └── test_calculator.py  # Automated unit test suite

