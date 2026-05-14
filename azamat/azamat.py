import pandas as pd

df = pd.read_csv("bank_advanced_dataset.csv")

# ── Задача 1 ──────────────────────────────────
print("=" * 60)
print("Задача 1 — Загрузка и первичный просмотр")
print("=" * 60)

print("\nПервые 5 строк:")
print(df.head())

print(f"\nКоличество строк: {df.shape[0]}, столбцов: {df.shape[1]}")

print("\nТипы данных:")
print(df.dtypes)

print("\nКоличество пропусков в каждой колонке:")
print(df.isnull().sum())

# ── Задача 2 ──────────────────────────────────
print("\n" + "=" * 60)
print("Задача 2 — Уникальные значения и списки")
print("=" * 60)

types_list = df["Account_Type"].unique().tolist()
regions_list = df["Region"].unique().tolist()

print(f"\nУникальные типы счетов: {types_list}")
print(f"Уникальные регионы:     {regions_list}")

# ── Задача 3 ──────────────────────────────────
print("\n" + "=" * 60)
print("Задача 3 — Работа со строками")
print("=" * 60)

ids_upper = [cid.upper() for cid in df["Customer_ID"]]
ids_lengths = [len(cid) for cid in df["Customer_ID"]]
avg_length = sum(ids_lengths) / len(ids_lengths)

print(f"\nПервые 5 ID в верхнем регистре: {ids_upper[:5]}")
print(f"Первые 5 длин ID: {ids_lengths[:5]}")
print(f"Средняя длина идентификатора: {avg_length:.2f}")

# ── Задача 4 ──────────────────────────────────
print("\n" + "=" * 60)
print("Задача 4 — Фильтрация по кредитному баллу")
print("=" * 60)

top_customers = df[df["Credit_Score"] >= 750].copy()

print(f"\nКоличество клиентов с Credit_Score >= 750: {len(top_customers)}")
print("\nПервые 10 клиентов (Age, Balance):")
print(top_customers[["Customer_ID", "Age", "Balance"]].head(10).to_string(index=False))

# ── Задача 5 ──────────────────────────────────
print("\n" + "=" * 60)
print("Задача 5 — Расчет финансовых показателей")
print("=" * 60)

df["net_worth"] = df["Balance"] - df["Loan_Amount"]
top10_net = df.nlargest(10, "net_worth")[["Customer_ID", "Balance", "Loan_Amount", "net_worth"]]

print("\nТоп-10 клиентов с максимальным net_worth:")
print(top10_net.to_string(index=False))

# ── Задача 6 ──────────────────────────────────
print("\n" + "=" * 60)
print("Задача 6 — Сохранение промежуточных результатов")
print("=" * 60)

top_customers.to_csv("student1_top_customers.csv", index=False)

# ── Задача 7 ──────────────────────────────────
print("\n" + "=" * 60)
print('Задача 7 — Поиск по ключевому слову "CUST_01"')
print("=" * 60)

found = df[df["Customer_ID"].str.contains("CUST_01")]
print(f"\nНайдено клиентов: {len(found)}")
print(found[["Customer_ID", "Account_Type", "Balance"]].to_string(index=False))

# ── Задача 8 ──────────────────────────────────
print("\n" + "=" * 60)
print("Задача 8 — Сортировка клиентов")
print("=" * 60)

print("\nТоп-10 по Balance (убывание):")
print(df.sort_values("Balance", ascending=False)[["Customer_ID", "Balance"]].head(10).to_string(index=False))

print("\n10 самых молодых клиентов:")
print(df.sort_values("Age")[["Customer_ID", "Age"]].head(10).to_string(index=False))

# ── Задача 9 ──────────────────────────────────
print("\n" + "=" * 60)
print("Задача 9 — Создание нового признака")
print("=" * 60)

df["income_per_transaction"] = df["Income"] / (df["Transactions_Last_Month"] + 1)
top5_ipt = df.nlargest(5, "income_per_transaction")[["Customer_ID", "Income", "Transactions_Last_Month", "income_per_transaction"]]

print("\nТоп-5 по income_per_transaction:")
print(top5_ipt.to_string(index=False))

# ── Задача 10 ─────────────────────────────────
print("\n" + "=" * 60)
print("Задача 10 — Генератор по активности")
print("=" * 60)

def online_clients(dataframe):
    for _, row in dataframe[dataframe["Online_Banking"] == 1].iterrows():
        yield row

gen = online_clients(df)
print("\nПервые 20 клиентов с Online_Banking = 1:")
print(f"{'Customer_ID':<15} {'Balance':>12} {'Transactions_Last_Month':>25}")
for i, row in enumerate(gen):
    if i >= 20:
        break
    print(f"{row['Customer_ID']:<15} {row['Balance']:>12.2f} {row['Transactions_Last_Month']:>25}")