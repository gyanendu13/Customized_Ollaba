from flask import Flask, render_template, request
from llama3 import llama3  # Assuming llama3 is a custom module you have

app = Flask(__name__)

def suggest_investments(income, age, marital_status, risk_appetite, fixed_expenses):
    # Example prompt for the LLaMA3 model
    prompt = (f"Income: {income}, Age: {age}, Marital Status: {marital_status}, "
              f"Risk Appetite: {risk_appetite}, Fixed Monthly Expenses: {fixed_expenses}\n"
              "Based on these attributes, suggest suitable investments.")
    result = llama3(prompt)
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        income = request.form['income']
        age = request.form['age']
        marital_status = request.form['marital_status']
        risk_appetite = request.form['risk_appetite']
        fixed_expenses = request.form['fixed_expenses']
        result = suggest_investments(income, age, marital_status, risk_appetite, fixed_expenses)
        return render_template('result.html', result=result)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
