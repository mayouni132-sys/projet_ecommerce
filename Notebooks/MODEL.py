import os
import pandas as pd
import numpy as np
from datetime import timedelta
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_squared_error, r2_score
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

#Data preparation 
#prepation of the ml pipeline

raw_df = pd.read_csv("ventes_clean.csv")

raw_df = raw_df.rename(columns={'ID': 'customer_id', 'Prix': 'order_value'})
if 'order_date' not in raw_df.columns:
    raw_df['order_date'] = pd.to_datetime('2023-01-01') + pd.to_timedelta(raw_df.index, unit='D') # Dummy date

raw_df['order_date'] = pd.to_datetime(raw_df['order_date'])

current_date = raw_df['order_date'].max()
cutoff_date = current_date - timedelta(days=90)

feature_df = raw_df[raw_df['order_date'] < cutoff_date]
target_df = raw_df[raw_df['order_date'] >= cutoff_date]

rfm = feature_df.groupby('customer_id').agg(
    recency=('order_date', lambda x: (cutoff_date - x.max()).days),
    frequency=('customer_id', 'count'),
    monetary_value=('order_value', 'sum'),
    average_order_value=('order_value', 'mean')
).reset_index()

future_sales = target_df.groupby('customer_id').agg(
    target_clv=('order_value', 'sum')
).reset_index()

model_data = pd.merge(rfm, future_sales, on='customer_id', how='left')
model_data['target_clv'] = model_data['target_clv'].fillna(0)

X = model_data[['recency', 'frequency', 'monetary_value', 'average_order_value']]
y = model_data['target_clv']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

alphas_to_test = np.logspace(-3, 4, 100)
ridge_cv = RidgeCV(alphas=alphas_to_test, cv=5, scoring='neg_mean_squared_error')
ridge_cv.fit(X_train_scaled, y_train)

print(f"Model trained. Optimal alpha: {ridge_cv.alpha_:.4f}")

X_all_scaled = scaler.transform(X)
model_data['predicted_clv'] = ridge_cv.predict(X_all_scaled)



os.environ["OPENAI_API_KEY"] = "your-api-key-here"
llm = ChatOpenAI(temperature=0, model="gpt-4-turbo")

agent = create_pandas_dataframe_agent(
    llm,
    model_data,
    verbose=True,
    agent_type="openai-tools",
    allow_dangerous_code=True
)

def run_ecommerce_analysis(user_query: str):
    print(f"\nAnalyzing: {user_query}\n")

    system_prompt = f"""
    You are an expert e-commerce data scientist.
    Analyze the data to answer the following query: {user_query}

    Rules for your response:
    1. Provide the exact quantitative result.
    2. Explain the business implication of this result.
    3. Suggest one strategic action the e-commerce store should take based on this data.
    """

    try:
        result = agent.invoke(system_prompt)
        return result['output']
    except Exception as e:
        return f"Analysis failed. Error: {e}"


if __name__ == "__main__":
    insight = run_ecommerce_analysis(
        "What is the average predicted CLV, and what are the customer IDs of the top 3 customers with the highest predicted CLV?"
    )
    print("Result:\n", insight)