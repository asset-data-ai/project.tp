import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# ── Задача 1 ── Загрузка данных и проверка корректности ───────────────────
print("=" * 60)
print("ЗАДАЧА 1 — Загрузка и проверка данных")
print("=" * 60)

df = pd.read_csv('../bank_advanced_dataset.csv')
print("\nИнформация о типах данных:")
print(df.dtypes)

missing = df.isnull().sum()
print("\nКолонки с пропусками:")
print(missing[missing > 0] if missing.sum() > 0 else "Пропусков нет.")

num_cols = df.select_dtypes(include=np.number).columns
df[num_cols] = df[num_cols].fillna(df[num_cols].mean())

# ── Задача 2 ── Фильтрация по нескольким условиям ─────────────────────────
print("\n" + "=" * 60)
print("ЗАДАЧА 2 — Клиенты с Income>=80000, Balance>=50000, Credit_Score>=700")
print("=" * 60)

premium = df[
    (df['Income'] >= 80000) &
    (df['Balance'] >= 50000) &
    (df['Credit_Score'] >= 700)
]
print(f"\nКоличество таких клиентов: {len(premium)}")
print(f"Средний Loan_Amount: {premium['Loan_Amount'].mean():.2f}")
print("\nПервые 10 клиентов:")
print(premium[['Customer_ID', 'Income', 'Balance', 'Credit_Score']].head(10).to_string(index=False))

# ── Задача 3 ── Функции для анализа ──────────────────────────────────────
print("\n" + "=" * 60)
print("ЗАДАЧА 3 — Функция high_activity_clients")
print("=" * 60)

def high_activity_clients(df, min_transactions, min_visits):
    return df[
        (df['Transactions_Last_Month'] >= min_transactions) &
        (df['Branch_Visits_Last_Year'] >= min_visits)
    ]

result = high_activity_clients(df, min_transactions=15, min_visits=5)
print(f"\nКлиентов с Transactions>=15 и Branch_Visits>=5: {len(result)}")
print(result[['Customer_ID', 'Transactions_Last_Month', 'Branch_Visits_Last_Year']].head(10).to_string(index=False))

# ── Задача 4 ── Comprehension и условные конструкции ──────────────────────
print("\n" + "=" * 60)
print("ЗАДАЧА 4 — List comprehension: Approved + Balance > 10000")
print("=" * 60)

approved_ids = [
    row['Customer_ID']
    for _, row in df.iterrows()
    if row['Loan_Status'] == 'Approved' and row['Balance'] > 10000
]
print(f"\nКоличество клиентов: {len(approved_ids)}")
print(f"Первые 10: {approved_ids[:10]}")

# ── Задача 5 ── Lambda и новые показатели ─────────────────────────────────
print("\n" + "=" * 60)
print("ЗАДАЧА 5 — financial_stability = Balance/(Loan_Amount+1) + Income/100000")
print("=" * 60)

df['financial_stability'] = df.apply(
    lambda row: row['Balance'] / (row['Loan_Amount'] + 1) + row['Income'] / 100000,
    axis=1
)
top10_fs = df.nlargest(10, 'financial_stability')[
    ['Customer_ID', 'Balance', 'Loan_Amount', 'Income', 'financial_stability']]
print("\nТоп-10 клиентов по financial_stability:")
print(top10_fs.to_string(index=False))

# ── Задача 6 ── Циклы и условия ───────────────────────────────────────────
print("\n" + "=" * 60)
print("ЗАДАЧА 6 — Категория клиента (Premium / Standard / Low)")
print("=" * 60)

categories = []
for fs in df['financial_stability']:
    if fs >= 2:
        categories.append('Premium')
    elif fs >= 1:
        categories.append('Standard')
    else:
        categories.append('Low')

df['client_category'] = categories
print("\nКоличество клиентов по категориям:")
print(df['client_category'].value_counts())

# ── Задача 7 ── OOP и классы ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("ЗАДАЧА 7 — Класс BankClient")
print("=" * 60)

class BankClient:
    def __init__(self, customer_id, balance, loan_amount, income):
        self.customer_id = customer_id
        self.balance = balance
        self.loan_amount = loan_amount
        self.income = income

    def stability(self):
        return self.balance / (self.loan_amount + 1) + self.income / 100000

    def __repr__(self):
        return f"BankClient({self.customer_id}, stability={self.stability():.4f})"

clients = [
    BankClient(
        row['Customer_ID'],
        row['Balance'],
        row['Loan_Amount'],
        row['Income']
    )
    for _, row in df.head(20).iterrows()
]

print("\nStability первых 20 клиентов:")
print(f"{'Customer_ID':<15} {'stability':>12}")
print("-" * 30)
for c in clients:
    print(f"{c.customer_id:<15} {c.stability():>12.4f}")

# ── Задача 8 ── Сводные таблицы и функции ────────────────────────────────
print("\n" + "=" * 60)
print("ЗАДАЧА 8 — Функция pivot_analysis + анализ financial_stability")
print("=" * 60)

def pivot_analysis(df, index_col, value_col):
    return df.pivot_table(index=index_col, columns='Account_Type', values=value_col, aggfunc='mean')

pivot_region = pivot_analysis(df, 'Region', 'financial_stability')
print("\nСредний financial_stability по Region × Account_Type:")
print(pivot_region.round(4))

print("\nСредний financial_stability по Account_Type:")
print(df.groupby('Account_Type')['financial_stability'].mean().round(4))

# ── Задача 9 ── Визуализация Matplotlib с условиями ───────────────────────
print("\n" + "=" * 60)
print("ЗАДАЧА 9 — Scatter: Income vs Balance, цвет по client_category")
print("=" * 60)

cat_colors = {'Premium': 'gold', 'Standard': 'steelblue', 'Low': 'salmon'}
color_list = df['client_category'].map(cat_colors)

fig, ax = plt.subplots(figsize=(10, 6))
for cat, color in cat_colors.items():
    subset = df[df['client_category'] == cat]
    ax.scatter(subset['Income'], subset['Balance'],
               c=color, label=cat, alpha=0.4, s=10)

ax.set_title('Income vs Balance по категории клиента')
ax.set_xlabel('Доход (Income)')
ax.set_ylabel('Баланс (Balance)')
ax.legend(title='Категория')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('student5_matplotlib.png', dpi=120)
plt.close()

# ── Задача 10 ── Визуализация Seaborn ────────────────────────────────────
print("\n" + "=" * 60)
print("ЗАДАЧА 10 — Seaborn: countplot, boxplot, heatmap")
print("=" * 60)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.countplot(data=df, x='Region', hue='client_category', ax=axes[0], palette='Set2')
axes[0].set_title('client_category по Region')
axes[0].set_xlabel('Регион')
axes[0].tick_params(axis='x', rotation=15)

df_capped = df.copy()
q99 = df_capped['financial_stability'].quantile(0.99)
df_capped['financial_stability'] = df_capped['financial_stability'].clip(upper=q99)
sns.boxplot(data=df_capped, x='Account_Type', y='financial_stability', ax=axes[1], palette='Blues')
axes[1].set_title('financial_stability по Account_Type')

fin_act_cols = ['Balance', 'Income', 'Loan_Amount', 'Credit_Score',
                'Transactions_Last_Month', 'Branch_Visits_Last_Year',
                'Complaints_Last_Year', 'Cards_Count']
corr = df[fin_act_cols].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=axes[2], linewidths=0.5)
axes[2].set_title('Корреляция финансовых и активности показателей')

plt.tight_layout()
plt.savefig('student5_seaborn.png', dpi=120)
plt.close()

