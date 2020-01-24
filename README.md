# Benford’s Law Stat Tool (Version a.2)

Benford’s Law is a mathematical law that describes patterns with the first digit of naturally occurring numbers. For distributions that follow Benford’s Law, we observed that the first digit of the number is 1 most frequently and 9 least frequently. All the other numbers fall somewhere in between. The probabilities for each digit are shown in the chart Benford’s Law Distribution. While other tools compare your numbers to the Benford’s distribution, they don’t provide information as to whether the mis-match is a problem or not. This tool uses the Max(M) statistics (also referred to as Leemis’ M) to examine a dataset and describe how well it adheres to Benford’s law. This can be used to assess risk of a dataset for purposes of auditing or fraud detection.

## Fraud detection
Benford’s Law is useful for detecting fabricated numbers in fraud schemes. Whether the scheme involves fabricating numbers or making changes to existing numbers, the resulting data fails to follow Benford’s Law in many instances. As documented in the Nigrini text, this occurs for two reasons: first, subconscious biases prevent people from creating truly random numbers, and second, fraudsters commonly follow a pattern of behavior.

To address the first point, creating random numbers is difficult. While truly random numbers follow certain patterns, humans thinking of random numbers focus on making the number look random. In one case study, Nigrini found numbers chosen to look random. No two numbers repeated, and no ended in round numbers. When applying analysis for compliance with Benford’s Law, numbers 7 thru 9 occurred most frequently as the first significant digit.

Regarding the second point, successful fraudsters tend to exhibit a pattern of behavior. When an inflated reimbursement or bogus expense works, the fraudster will tend to keep using that expense. For one example, an employee requested reimbursement for her breakfast every day. Because the habit remained the same, the reimbursement remained the same. Even when schemes follow the traditional pattern of test cases followed by larger transactions, unintended patterns can form. In a different case study, Nigrini found a scheme with bogus reimbursements. Even as the amount of fake requests increased, they still used the same numbers repeatedly.
## Data requirements
For this tool to be useful, it should be used on data that we would expect to follow Benford's Law. This section describes what data do and do not conform with Benford’s Law in many practical cases.
### Variability of values
The largest value must be at least 100 times larger than the smallest value. Generally, the bigger the difference, the more accurate the analysis will be. For example, if the values from your data ranged from $10 to $100, that is not variability and we wouldn’t expect the data to follow Benford’s Law (it has only one order of magnitude). Alternatively, if your data ranged from $1 to $100 we would expect closer adherence to Benford’s Law (two orders of magnitude). 
### Specific data
The amounts should be as close to raw data as possible. Once transactions are added together, Benford’s Law analysis becomes less powerful.
### Representative data
The data used should be measuring something that exists in the real world. Most commonly this will be financial data, but it is also appropriate to measure counts of inventory, production outputs, and events like the number of people entering a building per day.
Datasets that work well
There are some datasets that we use practically, but violate the mathematical principles of Benford’s Law. Because I understand we don’t operate in a perfect world, I’ll give details about perfect datasets. Remember that if you data don’t follow all of these rules, the program may assess them at a higher risk than a perfect dataset. In practice, I have found that even if your data does not follow these rules, the tools still gives consistent results. As a result, it can still identify data that is the riskiest from your dataset.
### Ratio numeric values
When comparing values, they should be a ratio based around zero. In other words, 2 should be twice the size of 1; 4 should be twice the size of 2.

For an example of numerical data that is not a ratio dataset, consider temperature measured in degrees fahrenheit. It violates the ratio values in two ways, first, 10° is NOT twice as hot as 5°; second,  0° is not the minimum temperature.
### Bias to smaller number
Small numbers should happen more frequently than big numbers. One way to test is if the median is higher than the mean. This rule can generally be ignored if the data span multiple orders of magnitude (i.e. the biggest number is 1,000 larger than the smallest number).
### Maximums do not impact behavior
In many instances, policies or rules can influence employee behavior which can skew results. For example, a maximum meal cost may incentivize employees to order meals just below the maximum costs. (I.e. An employee has a $25 maximum, but their entree is only $15 so they order an appetizer to get a more expensive meal.)

While many datasets like P-cards generally have a transaction limit, in practice, they tend to work with this analysis because there is not an incentive to spend more. One way to assess if it is appropriate is to look if transactions are clustered around the maximum; if they are, Benford’s Law analysis may not be accurate.
## What to avoid
There are certain datasets that we would not expect to conform with Benford’s Law. Using the analysis on a dataset such as this will produce unreliable and potentially misleading results. Below I have included a list of some examples. This is not intended to be a complete list.
- Random numbers--Serial Numbers, Social Security numbers
- Sequential numbers--Employee numbers/IDs
- Data with low variability--Production outputs from a reliable and consistent machine. If the machine consistently outputs between 90 and 110 units, the data will not follow Benford’s law.
- Aggregated data--Totals of multiple transactions from multiple accounts such as gross profit as shown on an income statement. Fabricated numbers that do not conform can be lost when combined with other numbers.
- Data with apparent trends/obvious explanations--Age of employees. We would expect most employees’ ages to be over 20 and under 80, as a result 1s and 9s would be underrepresented.
# How to interpret results
This section will describe what a P-value is, how to interpret it, and how it is calculated in this analysis. If you don’t care about the math and probability, know that at is core, in the context of this tool, a lower P-value means more risk in the set of transactions. 
## Interpreting results
A P-value describes the probability of pulling a sample by random chance given certain assumptions. For this analysis, the assumption is that all numbers follow Benford’s law. The P-value is the probability of pulling that exact set of numbers in a sample when Benford’s law is true. Very low P-values can indicate one of two things: first, that sample was just unlucky or second, the sample does not follow Benford’s law.

When interpreting outputs form this tool, a lower P-value indicates a higher risk. When using the data explorer included in this tool, outputs are automatically sorted from highest risk to lowest risk (limited to the riskiest 300 users). It displays the P-values to make it easier to understand the distribution of the risks. From experience, I found it a good practice to start with the highest risk transaction (those with the lowest P-values) and open the Quick View. Using professional judgement, determine if the distribution shown requires additional investigation. I have some useful tips for how to interpret Quick Views.
## Interpreting Quick Views
Quick Views are a program output. You can double click on any user/cardholder etc and see how well they conform to Benford’s Law. The red pluses show the first significant distribution observed in the data. The blue lines represent the information we expect to see if the data perfectly followed Benford’s Law.

Notice that there is still a range of values for data that perfectly follow Benford’s Law. Any red crosses between the lines are deemed to adhere to Benford’s Law. The lines will automatically adjust based on the number of transactions associated with an individual user. The more transactions or observations we see, the closer we expect the data to adhere to Benford’s Law.

See full documentation with images in this [Google Document](https://docs.google.com/document/d/1oXSgEeoYuDqYdcmBhc7jH0_IR71UtW4IhtQUo4YF8Eo/edit?usp=sharing)
