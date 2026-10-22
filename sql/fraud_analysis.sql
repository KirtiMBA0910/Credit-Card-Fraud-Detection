-- Credit Card Fraud Detection: SQL Business Analysis

-- 1. Total transactions
SELECT COUNT(*) AS total_transactions
FROM credit_card_transactions;

-- 2. Fraud transactions
SELECT COUNT(*) AS fraud_transactions
FROM credit_card_transactions
WHERE Class = 1;

-- 3. Genuine transactions
SELECT COUNT(*) AS genuine_transactions
FROM credit_card_transactions
WHERE Class = 0;

-- 4. Fraud percentage
SELECT
    SUM(CASE WHEN Class = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS fraud_percentage
FROM credit_card_transactions;

-- 5. Average transaction amount by class
SELECT
    Class,
    AVG(Amount) AS average_amount
FROM credit_card_transactions
GROUP BY Class;

-- 6. Total transaction amount by class
SELECT
    Class,
    SUM(Amount) AS total_amount
FROM credit_card_transactions
GROUP BY Class;

-- 7. Maximum transaction amount by class
SELECT
    Class,
    MAX(Amount) AS maximum_amount
FROM credit_card_transactions
GROUP BY Class;

-- 8. Number of transactions by class
SELECT
    Class,
    COUNT(*) AS transaction_count
FROM credit_card_transactions
GROUP BY Class;
