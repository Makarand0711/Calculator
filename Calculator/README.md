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
```

---

## 🛠️ Technologies Used

- **Core Language**: Python 3.8+
- **Standard Library Modules**: `math`, `json`, `csv`, `os`, `sys`, `datetime`
- **Testing**: `unittest` / `pytest`
- **Formatting & Linting**: Built to comply with PEP 8 standards

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher installed. Check version via:
  ```bash
  python3 --version
  ```

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/smart-calculator.git
cd smart-calculator
```

### Step 2: Install Development Dependencies (Optional)
If you wish to run the unit tests, install `pytest`:
```bash
pip install -r requirements.txt
```

---

## 💻 Usage

Start the interactive calculator by running:
```bash
python3 main.py
```

### 📋 Example Output

Upon starting, you will see a stylized interactive menu:

```text
✔ Welcome to the Smart Calculator! Choose an option to begin.

===========================
      SMART CALCULATOR     
===========================
1. Addition
2. Subtraction
3. Multiplication
4. Division
5. Modulus
6. Power
7. Floor Division
8. Square Root
9. Factorial
10. Percentage
11. Absolute
12. Logarithm
13. Sine
14. Cosine
15. Tangent
16. View History
17. Delete History
18. Export History to CSV
19. Exit
===========================
Select an option (1-19): 1
Enter first number: 10
Enter second number: 5
✔ Result: 10 addition 5 = 15
```

---

## 🧪 Running Unit Tests

Automated unit tests cover all math functions, percentage calculations, standard division validation, square root, factorials, and history corruption recovery.

Run the test suite using Python's built-in `unittest` runner:
```bash
python3 -m unittest tests/test_calculator.py
```

Or using `pytest`:
```bash
pytest tests/
```

---

## 📸 Screenshots Section

*(Placeholder for adding terminal execution screenshots or recording GIFs showing interaction and colored warning logs)*

---

## 🔮 Future Improvements

Here are some extensions planned for future releases:
- **🖥️ GUI Version**: A desktop graphical interface using Python's standard `tkinter` library.
- **🔬 Scientific Calculator Mode**: Support for physical constants, base conversions (hex/dec/bin), and matrices.
- **🌐 Web Version**: A browser-based calculator powered by a React/Next.js frontend and a Flask/FastAPI backend.
- **🎙️ Voice Calculator**: Integrated speech-to-text allowing hands-free voice-command calculations.
- **🔌 Calculator API**: A RESTful HTTP API allowing remote clients to execute math operations and query history.

---

## 📄 License

Distributed under the MIT License. See [LICENSE](file:///Users/zentech-038/Desktop/Python%20Projects/Calculator/LICENSE) for more information.
