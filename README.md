
(.venv) @Venkatasaikumarkethala ➜ /workspaces/Midterm (main) $ python3 main.py repl
2025-03-13 18:46:10,422 - root - INFO - Environment mode: Unknown
2025-03-13 18:46:10,422 - root - INFO - Calculator Application Launched.
2025-03-13 18:46:10,422 - root - INFO - Running: main
2025-03-13 18:46:10,423 - root - INFO - Plugin loaded: subtract_command
2025-03-13 18:46:10,423 - root - INFO - Plugin loaded: divide_command
2025-03-13 18:46:10,423 - root - INFO - Plugin loaded: add_command
2025-03-13 18:46:10,424 - root - INFO - Plugin loaded: multiply_command
2025-03-13 18:46:10,424 - root - INFO - Running: start_repl
Calculator REPL started. Type 'exit' to quit.
Append 'mp' at the end of a command to use multiprocessing.

# Advanced Python Calculator

An interactive, plugin-based Python calculator designed for flexibility, extensibility, and high code quality. It supports arithmetic and statistical operations, maintains a history, and includes logging and multiprocessing support.

---

## 🚀 Key Features

- **Interactive REPL**: Perform calculations live in a terminal session.
- **Plugin Architecture**: Easily extend functionality with custom plugins.
- **Calculation History**: View, filter, save, and load history using Pandas.
- **Logging System**: Monitors operations, errors, and environment status via Python logging.
- **Multiprocessing Support**: Optional multiprocessing for heavy operations.
- **Test Coverage**: 99% test coverage with `pytest` and `pytest-cov`.

---

## 📂 Project Structure

```
/app
  /plugins
    add_command.py
    subtract_command.py
    multiply_command.py
    divide_command.py
    mean_command.py
    standard_deviation_command.py
  calculation.py
  calculations.py
  command.py
  operations.py
  pandas_facade.py
/tests
  test_calculation.py
  test_calculations.py
  test_command.py
  test_operations.py
  test_plugins.py
main.py
README.md
requirements.txt
```

---

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8+
- Virtualenv (Recommended)

### Installation

```bash
git clone https://github.com/Venkatasaikumarkethala/Midterm.git
cd Midterm
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file at the project root:

```
ENVIRONMENT=Development
LOG_LEVEL=INFO
LOG_FILE=logs/application.log
```

---

## ▶️ How to Run

### REPL Mode

```bash
python3 main.py repl
```

### Sample Session

```bash
>> menu
Available Commands:
- subtract
- divide
- add
- multiply

>> add 10 5
2025-03-13 18:50:00,000 - root - INFO - Result for add: 15
10 add 5 = 15

>> history
  operation operand1 operand2 result
0       add       10        5     15
```

### CLI One-Liners

```bash
python3 main.py 5 3 add
python3 main.py 10 2 divide mp
```

---

## 💾 History Commands

- `history`: Displays calculation history.
- `clear_history`: Clears history.
- `save_history <filename>`: Saves history to a CSV file.
- `load_history <filename>`: Loads history from a CSV file.
- `delete_history <index>`: Deletes a record by index.
- `filter_with_operation <operation>`: Filters history by operation.

---

## 🧪 Run Tests

```bash
pytest --cov=app --cov-report=term-missing
```

#### Example Coverage Result

```
---------- coverage: platform linux, python 3.12.1-final-0 -----------
Name                                        Stmts   Miss  Cover
---------------------------------------------------------------
app/calculation.py                             12      0   100%
app/calculations.py                            27      0   100%
app/pandas_facade.py                           21      0   100%
app/plugins/add_command.py                     10      0   100%
...
TOTAL                                         147      2    99%
```

---

## 🏗️ Design Patterns Used

- **Command Pattern**: Encapsulates operations into commands.
- **Facade Pattern**: Simplifies interaction with Pandas history management.
- **Factory Method**: Dynamically loads plugins.
- **Strategy Pattern**: Allows selection of different calculation strategies.
- **Singleton Pattern**: Ensures one instance for key services.

---

## ⚙️ Logging

Logs are generated based on your `.env` configuration.

```
2025-03-13 18:49:49,054 - root - INFO - Plugin loaded: add_command
2025-03-13 18:49:49,054 - root - INFO - Calculator Application Launched.
```

---

## 📝 Author

Venkatasaikumarkethala  
🔗 [GitHub Profile](https://github.com/Venkatasaikumarkethala)

---

## 📺 Video Demo


---

## 📜 License

MIT License


