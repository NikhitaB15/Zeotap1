# Rule Engine with Abstract Syntax Tree (AST)

## Objective
This project implements a 3-tier rule engine application that evaluates user eligibility based on attributes such as age, department, income, and experience. The rule engine dynamically creates, combines, and modifies conditional rules using an Abstract Syntax Tree (AST). The application includes a simple UI, API, and backend for managing these rules.

---

## Features
- **AST-based Rule Representation**: Conditional rules are stored and processed using an Abstract Syntax Tree (AST) for easy modification and combination.
- **Dynamic Rule Creation and Combination**: Rules can be created dynamically and combined to form complex logic.
- **Evaluation of Rules**: The engine evaluates rules against user data to determine eligibility.
- **Error Handling and Validations**: Error handling for invalid rule strings, as well as validations for rule attributes.

---

## Project Structure
- **backend/**: Contains the backend logic of the rule engine including the core logic for rule creation, combination, and evaluation.
- **static/**: Stores static assets such as stylesheets, JavaScript files, etc.
- **templates/**: Contains the HTML templates for the user interface.
- **venv/**: Virtual environment for managing project dependencies.
- **.env**: Configuration file for storing environment variables.
- **README.md**: Documentation for the project.
- **requirements.txt**: Lists the Python dependencies required for the project.

---

## API Design

1. **create_rule(rule_string)**  
   Converts a rule string into an AST.  
   **Input**: Rule string (e.g., `"age > 30 AND department = 'Sales'"`)  
   **Output**: AST representation of the rule.

2. **combine_rules(rules)**  
   Combines multiple rule strings into a single AST efficiently.  
   **Input**: List of rule strings.  
   **Output**: Combined AST.

3. **evaluate_rule(json_data)**  
   Evaluates the given data against the combined AST to check if it matches the rule.  
   **Input**: JSON representing the AST, dictionary with user attributes.  
   **Output**: `True` if the data satisfies the rule, `False` otherwise.

---

## Data Structure
Each rule is represented as a tree structure with nodes:
- **Type**: Specifies the node type ("operator" for AND/OR, "operand" for conditions).
- **Left and Right**: References to the child nodes.
- **Value**: Value for operand nodes (e.g., comparison values).

---

## Sample Rules
- **Rule 1**:  
  `((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)`
  
- **Rule 2**:  
  `((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)`

---

## Database Design
The rules and metadata are stored in a database.  
- **Schema**: The schema supports storing the AST representation of rules along with metadata like creation timestamps and rule identifiers.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/rule-engine.git
   cd rule-engine
