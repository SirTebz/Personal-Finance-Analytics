# Data dictionary

| Field | Type | Meaning |
|---|---|---|
| TransactionDate | DATE | Date on which a financial event occurred. |
| TransactionType | Income/Expense | Determines cash-flow direction. |
| Amount | DECIMAL(18,2) | Positive ZAR monetary value. |
| CategoryId | Foreign key | Links a transaction or budget to its category. |
| BudgetMonth/BudgetYear | Integer | Monthly budget period. |
