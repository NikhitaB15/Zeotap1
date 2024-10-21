from flask import Flask, request, jsonify, render_template
from rule_engine import RuleEngine, validate_rule_string
from database import save_rule, get_all_rules
import json
import os

static_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static')
template_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')

app = Flask(__name__, static_folder=static_folder_path, template_folder=template_folder_path)
rule_engine = RuleEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
    rule_string = request.json['rule']
    if not validate_rule_string(rule_string):
        return jsonify({"error": "Invalid rule string"}), 400
    
    try:
        rule_ast = rule_engine.create_rule(rule_string)
        ast_json = rule_engine.get_ast_json(rule_ast)
        return jsonify({"message": "Rule created successfully", "rule": ast_json})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/combine_rules', methods=['POST'])
def combine_rules_endpoint():
    rule_strings = request.json['rules']
    try:
        combined_ast = rule_engine.combine_rules(rule_strings)
        rule_id = save_rule(combined_ast)
        return jsonify({"message": "Rules combined successfully", "rule": combined_ast, "rule_id": str(rule_id)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_endpoint():
    rule_ast = request.json['rule']
    user_data = request.json['data']
    try:
        result = rule_engine.evaluate_rule(rule_ast, user_data)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)