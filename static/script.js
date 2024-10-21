document.addEventListener('DOMContentLoaded', () => {
    const createRuleBtn = document.getElementById('createRuleBtn');
    const addRuleBtn = document.getElementById('addRuleBtn');
    const combineRulesBtn = document.getElementById('combineRulesBtn');
    const evaluateRuleBtn = document.getElementById('evaluateRuleBtn');
    const ruleList = document.getElementById('ruleList');

    createRuleBtn.addEventListener('click', handleCreateRule);
    addRuleBtn.addEventListener('click', addRuleInput);
    combineRulesBtn.addEventListener('click', handleCombineRules);
    evaluateRuleBtn.addEventListener('click', handleEvaluateRule);

    addRuleInput(); // Add the first rule input
});

function addRuleInput() {
    const ruleItem = document.createElement('div');
    ruleItem.className = 'rule-item';
    ruleItem.innerHTML = `
        <textarea rows="2" placeholder="Enter rule string"></textarea>
        <button class="remove-rule-btn">Remove</button>
    `;
    ruleItem.querySelector('.remove-rule-btn').addEventListener('click', () => ruleItem.remove());
    document.getElementById('ruleList').appendChild(ruleItem);
}

async function handleCreateRule() {
    const rule = document.getElementById('ruleInput').value;
    const astOutput = document.getElementById('astOutput');

    try {
        const response = await fetch('/create_rule', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rule })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            astOutput.textContent = JSON.stringify(data.rule, null, 2);
        } else {
            astOutput.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        astOutput.textContent = `Error: ${error.message}`;
    }
}

async function handleCombineRules() {
    const ruleInputs = document.querySelectorAll('#ruleList textarea');
    const rules = Array.from(ruleInputs).map(input => input.value).filter(rule => rule.trim() !== '');
    const astOutput = document.getElementById('astOutput');

    if (rules.length < 2) {
        alert('Please enter at least two rules to combine.');
        return;
    }

    try {
        const response = await fetch('/combine_rules', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rules })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            astOutput.textContent = JSON.stringify(data.rule, null, 2);
            alert(`Rules combined successfully. Rule ID: ${data.rule_id}`);
        } else {
            astOutput.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        astOutput.textContent = `Error: ${error.message}`;
    }
}

async function handleEvaluateRule() {
    const ruleAst = JSON.parse(document.getElementById('astOutput').textContent);
    const userData = document.getElementById('dataInput').value;
    const resultDiv = document.getElementById('evaluationResult');

    try {
        const response = await fetch('/evaluate_rule', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                rule: ruleAst,
                data: JSON.parse(userData)
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            resultDiv.textContent = `Result: ${data.result}`;
        } else {
            resultDiv.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        resultDiv.textContent = `Error: ${error.message}`;
    }
}