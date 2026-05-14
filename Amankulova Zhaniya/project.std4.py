
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('bank_advanced_dataset.csv')

#1
print("=" * 60)
print("ЗАДАЧА 1 — Клиенты с Online_Banking = 1")
print("=" * 60)
print("\nПервые 10 строк:")
print(df.head(10))

online = df[df['Online_Banking'] == 1]
print(f"\nКоличество клиентов с Online_Banking=1: {len(online)}")
print(f"Средний Balance:  {online['Balance'].mean():.2f}")
print(f"Средний Income:   {online['Income'].mean():.2f}")

#2
print("\n" + "=" * 60)
print("ЗАДАЧА 2 — Активные онлайн-клиенты (Transactions>=20, Online_Banking=1)")
print("=" * 60)

active = df[(df['Transactions_Last_Month'] >= 20) & (df['Online_Banking'] == 1)]
active_ids = [cid.upper() for cid in active['Customer_ID']]
print(f"\nТаких клиентов: {len(active)}")
print(f"Первые 5 ID: {active_ids[:5]}")
print(f"Средний баланс: {active['Balance'].mean():.2f}")

#3
print("\n" + "=" * 60)
print("ЗАДАЧА 3 — Генератор savings_clients (Savings + Branch_Visits > 5)")
print("=" * 60)

def savings_clients(dataframe):
    cond = (dataframe['Account_Type'] == 'Savings') & (dataframe['Branch_Visits_Last_Year'] > 5)
    for _, row in dataframe[cond].iterrows():
        yield row

gen = savings_clients(df)
print(f"\nПервые 15 клиентов:")
print(f"{'Customer_ID':<15} {'Balance':>12} {'Branch_Visits':>15}")
print("-" * 45)
for i, client in enumerate(gen):
    if i >= 15:
        break
    print(f"{client['Customer_ID']:<15} {client['Balance']:>12.2f} {client['Branch_Visits_Last_Year']:>15}")

#4
print("\n" + "=" * 60)
print("ЗАДАЧА 4 — Распределение Loan_Status для клиентов с Balance > 0")
print("=" * 60)

pos_bal = df[df['Balance'] > 0]
loan_dict = pos_bal.groupby('Loan_Status').size().to_dict()
print("\nСловарь (Loan_Status → количество):", loan_dict)
top2 = sorted(loan_dict.items(), key=lambda x: x[1], reverse=True)[:2]
print(f"Топ-2 Loan_Status: {top2}")

#5
print("\n" + "=" * 60)
print("ЗАДАЧА 5 — Уникальные (Region, Account_Type) для Online_Banking=1")
print("=" * 60)

online_combo = set(zip(online['Region'], online['Account_Type']))
print(f"\nКоличество уникальных комбинаций: {len(online_combo)}")
print("Комбинации:", sorted(online_combo))

#6
print("\n" + "=" * 60)
print("ЗАДАЧА 6 — activity_score = (Transactions + Branch_Visits) / (Income + 1)")
print("=" * 60)

df['activity_score'] = df.apply(
    lambda row: (row['Transactions_Last_Month'] + row['Branch_Visits_Last_Year']) / (row['Income'] + 1),
    axis=1)

top10_act = df.nlargest(10, 'activity_score')[['Customer_ID', 'Transactions_Last_Month', 'Branch_Visits_Last_Year', 'Income', 'activity_score']]
print("\nТоп-10 по activity_score:")
print(top10_act.to_string(index=False))

#7
print("\n" + "=" * 60)
print("ЗАДАЧА 7 — NumPy массив activity_data")
print("=" * 60)

activity_data = df[['Transactions_Last_Month', 'Branch_Visits_Last_Year', 'Complaints_Last_Year']].to_numpy()
print(f"\nФорма массива: {activity_data.shape}")
print(f"Среднее по показателям: {np.mean(activity_data, axis=0).round(2)}")
print(f"Std по показателям: {np.std(activity_data, axis=0).round(2)}")

total_activity = activity_data.sum(axis=1)
max_idx = np.argmax(total_activity)
print(f"\nИндекс клиента с макс. суммой активности: {max_idx} ({df.iloc[max_idx]['Customer_ID']}, сумма={total_activity[max_idx]})")

#8
print("\n" + "=" * 60)
print("ЗАДАЧА 8 — Сводные таблицы activity_score и Balance")
print("=" * 60)

pivot_act = df.pivot_table(index='Region', columns='Account_Type', values='activity_score', aggfunc='mean')
pivot_bal = df.pivot_table(index='Region', columns='Account_Type', values='Balance', aggfunc='mean')

print("\nСредний activity_score по Region × Account_Type:")
print(pivot_act.round(6))
print("\nСредний Balance по Region × Account_Type:")
print(pivot_bal.round(2))

pivot_act.to_csv('student4_activity_score_pivot.csv')
pivot_bal.to_csv('student4_balance_pivot.csv')

#9
print("\n" + "=" * 60)
print("ЗАДАЧА 9 — Гистограмма Transactions + Scatter Balance vs Income")
print("=" * 60)

colors = {'Business': 'steelblue', 'Checking': 'coral', 'Savings': 'green', 'Loan': 'purple'}
color_list = df['Account_Type'].map(colors)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df['Transactions_Last_Month'], bins=20, color='steelblue', edgecolor='white')
axes[0].set_title('Распределение Transactions_Last_Month')
axes[0].set_xlabel('Транзакции за последний месяц')
axes[0].set_ylabel('Количество клиентов')
axes[0].grid(True, alpha=0.3)

axes[1].scatter(df['Balance'], df['Income'], c=color_list, alpha=0.3, s=8)
axes[1].set_title('Balance vs Income по Account_Type')
axes[1].set_xlabel('Баланс (Balance)')
axes[1].set_ylabel('Доход (Income)')
axes[1].grid(True, alpha=0.3)

from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], marker='o', color='w', label=at,
                          markerfacecolor=c, markersize=8)
                   for at, c in colors.items()]
axes[1].legend(handles=legend_elements, title='Account_Type')

plt.tight_layout()
plt.savefig('student4_matplotlib.png', dpi=120)
plt.close()

#10
print("\n" + "=" * 60)
print("ЗАДАЧА 10 — Seaborn: countplot, boxplot, heatmap")
print("=" * 60)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

online_df = df[df['Online_Banking'] == 1]
sns.countplot(data=online_df, x='Region', ax=axes[0])
axes[0].set_title('Клиенты Online_Banking=1 по Region')

df_capped = df.copy()
q99 = df_capped['activity_score'].quantile(0.99)
df_capped['activity_score'] = df_capped['activity_score'].clip(upper=q99)
sns.boxplot(data=df_capped, x='Account_Type', y='activity_score', ax=axes[1])
axes[1].set_title('activity_score по Account_Type')

act_fin_cols = ['Balance', 'Income', 'Loan_Amount', 'Credit_Score',
                'Transactions_Last_Month', 'Branch_Visits_Last_Year', 'Complaints_Last_Year']
corr = df[act_fin_cols].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=axes[2], linewidths=0.5)
axes[2].set_title('Корреляция активности и финансовых показателей')

plt.tight_layout()
plt.savefig('student4_seaborn.png', dpi=120)
plt.close()