import streamlit as st
from enum import Enum
import pandas as pd
import re
from llama3 import llama3


class RiskLevel(Enum):
    CONSERVATIVE = ("1", "Conservative (Low Risk)")
    MODERATE = ("2", "Moderate (Low-Medium Risk)")
    BALANCED = ("3", "Balanced (Medium Risk)")
    GROWTH = ("4", "Growth (Medium-High Risk)")
    AGGRESSIVE = ("5", "Aggressive (High Risk)")

    def __str__(self):
        return self.value[1]

    @property
    def level(self):
        return self.value[0]


def suggest_investments(
    income: float,
    age: int,
    marital_status: str,
    risk_appetite: str,
    fixed_expenses: float,
    savings: float,
    liabilities: float,
    investment_goals: str,
) -> str:
    prompt = (
        f"Income: {income}, Age: {age}, Marital Status: {marital_status}, "
        f"Risk Appetite: {risk_appetite}, Fixed Monthly Expenses: {fixed_expenses}, "
        f"Current Savings: {savings}, Liabilities: {liabilities}, Investment Goals: {investment_goals}\n"
        "Based on these attributes, suggest suitable investments in tabular format.\n"
        "Each row should include: Investment Type, Name, Risk, Expected Return, Reason."
    )
    try:
        return llama3(prompt)
    except Exception as e:
        return f"An error occurred while generating suggestions: {e}"


def parse_markdown_table(markdown: str):
    try:
        # Extract lines that look like a markdown table
        lines = [line.strip() for line in markdown.split("\n") if "|" in line]
        if len(lines) < 2:
            return None
        headers = [h.strip() for h in lines[0].split("|") if h.strip()]
        rows = []
        for line in lines[2:]:
            values = [cell.strip() for cell in line.split("|") if cell.strip()]
            if len(values) == len(headers):
                rows.append(values)
        if rows:
            return pd.DataFrame(rows, columns=headers)
        return None
    except Exception:
        return None


# Streamlit App Configuration
st.set_page_config(page_title="Deutsche Bank Investment Planner", layout="centered")
st.title("📈 Deutsche Bank - Your Financial Investment Companion")

st.sidebar.header("🔧 Customize Your Profile")

# Sidebar Inputs
income = st.sidebar.number_input("Annual Income (USD)", min_value=100000.0, step=500.0, format="%f")
age = st.sidebar.number_input("Age", min_value=18, format="%d")
marital_status = st.sidebar.radio("Marital Status", ["Single", "Married", "Divorced", "Widowed"])
savings = st.sidebar.number_input("Current Savings (USD)", min_value=0.0, step=1000.0, format="%f")
fixed_expenses = st.sidebar.number_input("Fixed Monthly Expenses (USD)", min_value=1000.0, step=100.0, format="%f")
liabilities = st.sidebar.number_input("Liabilities (USD)", min_value=0.0, step=500.0, format="%f")

investment_goals = st.selectbox(
    "Primary Investment Goal",
    [
        "Retirement",
        "Buying a house",
        "Education fund",
        "Emergency fund",
        "Vacation",
        "Wealth accumulation",
        "Other",
    ],
)

risk_appetite = st.selectbox(
    "Risk Appetite", list(RiskLevel), format_func=lambda x: x.value[1]
)

# Main Button Logic
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🚀 Get Investment Suggestions"):
        with st.spinner("Analyzing your profile..."):
            result = suggest_investments(
                income,
                age,
                marital_status,
                risk_appetite.level,
                fixed_expenses,
                savings,
                liabilities,
                investment_goals,
            )
        
        st.success("📊 Personalized Investment Suggestions")

        # Try to parse markdown table and show as dataframe
        df = parse_markdown_table(result)
        if df is not None:
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("⚠️ Couldn't parse table. Showing raw output instead:")
            st.text_area("Suggestions", result, height=400)

with col2:
    # if st.button("🔄 Reset Inputs"):
    #     st.experimental_rerun()
    if st.button("🔄 Reset Inputs"):
        st.rerun()


# Custom Footer
footer = """
<style>
.footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    text-align: center;
    padding: 12px;
    font-size: 0.8rem;
    color: #888;
    background-color: #f9f9f9;
}
</style>
<div class="footer">
    💡 Created with ❤️ by FundFlow Team
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
