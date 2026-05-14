import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv('bank_advanced_dataset.csv')
#Тапсырмада сұралған бағандар тізімі
columns_to_extract = [
    'Age', 'Income', 'Balance', 'Credit_Score', 'Loan_Amount',
    'Transactions_Last_Month', 'Cards_Count', 'Branch_Visits_Last_Year', 'Complaints_Last_Year'
]
#NumPy массивіне айналдыру
numeric_data = df[columns_to_extract].to_numpy()
#Массивтің формасын шығару
print("Форма массива (қатарлар, бағандар)")
print(numeric_data.shape)
#Алғашқы 5 қатарды шығару
print("\nПервые 5 строк массива")
print(numeric_data[:5])
#2
cols_for_stats = ['Age', 'Income', 'Balance', 'Credit_Score', 'Loan_Amount']
print("КЛИЕНТТЕРДІҢ НЕГІЗГІ КӨРСЕТКІШТЕРІ\n")
# статистика
for col in cols_for_stats:
    mean_val = df[col].mean()
    median_val = df[col].median()
    std_val = df[col].std()
    #читаемый
    print(f"Баған: {col}")
    print(f"  Орташа мән (Среднее)        : {mean_val:.2f}")
    print(f"  Медиана                     : {median_val:.2f}")
    print(f"  Ауытқу (Станд. отклонение)  : {std_val:.2f}")
    print("-" * 40)
#3 Сүзу шарты
condition = (df['Income'] > 80000) & (df['Balance'] > 50000)
# Индекстар
matching_indices = df[condition].index.tolist()
print(f"Шартқа сай келетін клиенттер саны: {len(matching_indices)}")
print(f"Алғашқы 5 индекстің тізімі: {matching_indices[:5]}")
result = df.loc[condition, ['Customer_ID', 'Income', 'Balance']].head(10)
print("\n--- Ең жоғары табысы мен балансы бар алғашқы 10 клиент ---")
print(result)
#4
counts_series = df['Account_Type'].value_counts()
# dict айналдыру
# Ключ = Account_Type, Значение = Количество клиентов
account_counts_dict = counts_series.to_dict()
print("--- Шот түрлері бойынша сөздік (dict) ---")
print(account_counts_dict)
top_2_types = counts_series.head(2)
print("\n--- Клиенттер саны бойынша ТОП-2 шот түрі ---")
print(top_2_types)
#5
region_set = set(df['Region'])
loan_status_set = set(df['Loan_Status'])
print("Уникальды региондар:", region_set)
print("Уникальды несие статустары:", loan_status_set)
print("Региондар саны:", len(region_set))
print("Статустар саны:", len(loan_status_set))
#6
df['loan_ratio'] = df.apply(lambda row: row['Loan_Amount'] / (row['Balance'] +1), axis = 1)
def high_income(dataframe):
    for _, row in dataframe.iterrows():
        if row['Income'] >= 100000:
            yield row
generator = high_income(df)
print(f"{'Customer_ID':<15} {'Income':<12} {'loan_ratio':<10}")
for i, row in enumerate(generator):
    if i >= 10:
        break
    print(f"{row['Customer_ID']:<15} {row['Income']:<12} {row['loan_ratio']:.4f}")
#7
#аймақ пен шот түрі бойынша орташа баланс
pivot = pd.pivot_table(
    df,
    index = 'Region',
    columns = 'Account_Type',
    values = 'Balance',
    aggfunc = 'mean'
)
print(pivot.round(2))
best_region = pivot.mean(axis=1).idxmax()
best_value = pivot.mean(axis=1).max()
best_account = pivot.mean(axis=0).idxmax()
print(f" Ең жоғары орташа балансы бар аймақ : {best_region} ({best_value:.2f})")
print(f" Ең жоғары орташа балансы бар шот түрі: {best_account}")
#8
df['loan_ratio'] = df.apply(lambda row: row['Loan_Amount'] / (row['Balance'] +1), axis = 1)
pivot = pd.pivot_table(
    df,
    index = 'Region',
    columns = 'Account_Type',
    values = 'Balance',
    aggfunc = 'mean'
)
df.to_csv('student2_loan_rstio.csv', index = False)
print("CSV сақталды: student2_loan_ratio.csv")
pivot.to_excel('student2_loan_ratio.xlsx')
print("Excel сақталды: student2_region_account.xlsx")
df_check = pd.read_csv('student2_loan_rstio.csv')
print("~~~ ТЕКСЕРУ ~~~")
print(f"Түпнұсқа жолдар   : {len(df)}")
print(f"Оқылған жолдар    : {len(df_check)}")
print(f"Түпнұсқа бағандар : {len(df.columns)}")
print(f"Оқылған бағандар  : {len(df_check.columns)}")
if df.shape == df_check.shape:
    print("✅")
else:
    print("❌")
print(" After checking")
print(df_check[['Customer_ID', 'Income', 'loan_ratio']].head(3))
#9
plt.figure(figsize = (8, 5))
plt.hist(df['Age'], bins=15, color = 'steelblue', edgecolor = 'black')
plt.title('Клиенттердің жас таралуы')
plt.xlabel('Age')
plt.ylabel('Quantity')
plt.grid(True)
plt.tight_layout()
plt.savefig('histogram_age.png')
plt.show()
print("✅ histogram_age.png saved")

plt.figure(figsize = (8, 5))
plt.scatter(df['Income'], df['Balance'], alpha=0.4, color='coral', edgecolors='black', linewidths=0.3)
plt.title('Табыс пен баланс арасындағы байланыс')
plt.xlabel('Income')
plt.ylabel('Balance')
plt.grid(True)
plt.tight_layout()
plt.savefig('scatter_income_balance.png')
plt.show()
print("✅ scatter_income_balance.png saved")
#10
df['loan_ratio'] = df.apply(lambda row: row['Loan_Amount'] / (row['Balance'] +1), axis = 1)
#COUNTPLOT — Account_Type
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='Account_Type', hue='Account_Type', palette='Set2', legend=False)
plt.title('Шот түрлері бойынша клиенттер саны')
plt.xlabel('Account_Type')
plt.ylabel('Quantity')
plt.grid(True)
plt.tight_layout()
plt.savefig('countplot_account_type.png')
plt.show()
print("✅ countplot_account_type.png saved")
#BOXPLOT — loan_ratio по Region
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x='Region', y='loan_ratio', hue='Region', palette='pastel', legend=False)
plt.title('Аймақтар бойынша несие коэффициенті')
plt.xlabel('Region')
plt.ylabel('Loan_ratio')
plt.grid(True)
plt.tight_layout()
plt.savefig('boxplot_loan_ratio_region.png')
plt.show()
print("✅ boxplot_loan_ratio_region.png saved")
#HEATMAP — корреляция
plt.figure(figsize=(10, 7))
numeric_df = df.select_dtypes(include='number')
correlation = numeric_df.corr()
sns.heatmap(
    correlation,
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    linewidths=0.5
)
plt.title('Сандық бағандар арасындағы корреляция')
plt.tight_layout()
plt.savefig('heatmap_correlation.png')
plt.show()
print("✅ heatmap_correlation.png saved")