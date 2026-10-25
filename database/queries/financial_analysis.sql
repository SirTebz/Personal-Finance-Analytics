-- Top spending categories and their share of total expense (GROUP BY, CTE, window function).
WITH CategorySpend AS (SELECT c.Name, SUM(t.Amount) Amount FROM Transactions t INNER JOIN Categories c ON c.CategoryId=t.CategoryId WHERE t.TransactionType='Expense' AND t.IsDeleted=0 GROUP BY c.Name)
SELECT Name, Amount, CAST(100.0 * Amount / SUM(Amount) OVER () AS DECIMAL(5,2)) PercentageOfExpenses FROM CategorySpend ORDER BY Amount DESC;
-- Monthly income, expenses, and net cash flow (CASE/date functions).
SELECT DATEFROMPARTS(YEAR(TransactionDate),MONTH(TransactionDate),1) MonthStart, SUM(CASE WHEN TransactionType='Income' THEN Amount ELSE 0 END) Income, SUM(CASE WHEN TransactionType='Expense' THEN Amount ELSE 0 END) Expenses FROM Transactions WHERE IsDeleted=0 GROUP BY YEAR(TransactionDate),MONTH(TransactionDate) HAVING SUM(Amount)>0 ORDER BY MonthStart;
-- Five largest expense transactions (ORDER BY / TOP).
SELECT TOP 5 TransactionDate, Description, Amount FROM Transactions WHERE TransactionType='Expense' AND IsDeleted=0 ORDER BY Amount DESC;
