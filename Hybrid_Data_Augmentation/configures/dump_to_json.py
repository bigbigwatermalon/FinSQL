import json

few_shot_examples_spider = [
    """
Here's an example for you:
Question: What are the names of movies and books from companies registered in "China"?
Answer:
Reasoning process:
From the question, it is clear that data related to the concepts of "company," "movies," and "books" is required. The corresponding tables for these concepts are: culture_company, movie, and book_club.
Next, we need to figure out how to retrieve relevant movies and books from companies. From the Schema, it can be observed that the culture_company table contains the fields movie_id and book_club_id, which happen to be the primary keys of the other two tables. This means we can use JOIN operations to associate these three tables.
Furthermore, the question mentions "companies registered in China," so it's necessary to add conditions in the WHERE clause of the query to filter out these companies.

Based on the above thought process, the generated SQL query is as follows:

Generated SQL:
```
SELECT T1.title ,  T3.book_title FROM movie AS T1 JOIN culture_company AS T2 ON T1.movie_id  =  T2.movie_id JOIN book_club AS T3 ON T3.book_club_id  =  T2.book_club_id WHERE T2.incorporated_in  =  "中国";

```

""",
    """
Here's an example for you:
Question: For storms with maximum speeds higher than the average speed, return the total number of deaths and the total damages in millions.
Answer:
Reasoning process:
Firstly, we need to identify the average maximum speed of all storms, which requires a query on the "storm" table. Then, we need to find storms with maximum speeds exceeding this average speed, and accumulate their total number of deaths and total damages.
This question essentially involves two subqueries:

1. Calculate the average maximum speed of all storms: SELECT AVG(Max_speed) FROM storm
2. Calculate the total number of deaths and total damages for storms with maximum speeds exceeding this average: SELECT SUM(Number_Deaths), SUM(Damage_millions_USD) FROM storm WHERE Max_speed > (Subquery 1)

Based on the thought process above, the generated SQL query statement is as follows:

Generated SQL:
```
SELECT SUM(Number_Deaths), SUM(Damage_millions_USD) FROM storm WHERE Max_speed > (SELECT AVG(Max_speed) FROM storm);
```

""",
    """
Here's an example for you:
Question: What are the names, heights, and prominences of the mountain ranges that do not belong to the "Changbai Mountains" range?
Answer:
Reasoning process:
1. From which tables should the information be retrieved? Answer: The question requires querying the names of mountain ranges, so the table "mountain" needs to be used.
2. Which columns of information are needed? Answer: The question asks for the names, heights, and prominences of the mountain ranges, so the columns "name," "Height," and "Prominence" are needed.
3. What conditions should be added to filter the rows that meet the requirements? Answer: The column "Range" should not belong to the "Changbai Mountains" range.
4. Which tables need to be joined to obtain all the necessary information? Answer: No need to join other tables.

Based on the above thought process, the generated SQL query statement is as follows:

Generated SQL:
```
SELECT name, Height, Prominence FROM mountain WHERE Range != 'Changbai Mountains';
```

""",
    """
Here's an example for you:
Question: Provide me with detailed information and opening hours for each museum.
Answer:
Reasoning process:
Firstly, this question involves entities and attributes related to museums and opening hours. We need to retrieve data from the tables Tourist_Attractions and Museums. We also need to join these tables to acquire detailed information and opening hours for each museum.

Based on these ideas, we can use the following SQL query statement to solve the problem:

Generated SQL:
```
SELECT Museums.Museum_Details, Tourist_Attractions.Opening_Hours
FROM Museums
INNER JOIN Tourist_Attractions ON Museums.Museum_ID = Tourist_Attractions.Tourist_Attraction_ID;
```

""",
    """
Here's an example for you:
Question: Find the email addresses and phone numbers of customers who have never filed a complaint before.
Answer:
Reasoning:
1. It's necessary to filter out customers who have never filed a complaint from the Customers table.
2. It's required to select the email addresses and phone numbers of these customers.

Generated SQL:
```
SELECT email_address, phone_number 
FROM Customers 
WHERE customer_id NOT IN (
SELECT customer_id 
FROM Complaints
)
```

""",
    """
Here's an example for you:
Question: What are the first names, middle names, and last names of all individuals sorted by their last names?
Answer: 1. To query personal information, the Individuals table will definitely be used.
2. To sort by last name, the ORDER BY statement is needed, and it should be sorted based on the last name. In English, the last name usually comes at the end of the name, so the individual_last_name field from the Individuals table should be used for sorting.
3. The result should display the first names, middle names, and last names of all individuals. Therefore, the individual_first_name, individual_middle_name, and individual_last_name fields from the Individuals table need to be selected.

Generated SQL:
```
SELECT individual_first_name, individual_middle_name, individual_last_name 
FROM Individuals 
ORDER BY individual_last_name;
```

""",
    """
Here's an example for you:
Question: What is the name of the department of the student with the lowest GPA?
Answer:
Reasoning process:
Firstly, we need to find the student with the lowest GPA, so we need to filter out the student with the minimum GPA value from the student table. Then, it's necessary to identify the name of the department to which this student belongs. Hence, we need to get the department name through a join between the student table and the department table.
In conclusion, we require a joined query between the student table and the department table, and we need to use the GPA field as a filter condition, sorting the results in ascending order based on the GPA field. Ultimately, the first retrieved record will provide the name of the department where the student with the lowest GPA is enrolled.

Generated SQL:
```sql
SELECT DEPARTMENT.DEPT_NAME
FROM DEPARTMENT, STUDENT
WHERE STUDENT.DEPT_CODE = DEPARTMENT.DEPT_CODE
ORDER BY STUDENT.STU_GPA ASC
LIMIT 1;
```

""",
    """
Here's an example for you:
Question: How many publications does "Christopher Manning" have?
Answer:
Reasoning process:
First, we need to find the author ID of "Christopher Manning," which can be obtained by querying the "author" table with the author's name. Then, we need to find all the paper IDs he has written in the "writes" table. Next, in the "paper" table, we locate these papers and count their quantity.

Generated SQL:
```
SELECT COUNT(DISTINCT paper.paperId) AS paper_count
FROM author
JOIN writes ON author.authorId = writes.authorId
JOIN paper ON writes.paperId = paper.paperId
WHERE author.authorName = 'Christopher Manning';
```

""",
    """
Here's an example for you:
Question: Display different publishers along with the number of publications they have published.
Answer:
Reasoning process:
Step 1: We need to retrieve different publishers and the count of publications they have published from the publication table, so we need to use the Publisher column and COUNT().
Step 2: We need to use GROUP BY to group by publishers.

Generated SQL:
```
SELECT Publisher, COUNT(*) AS Num_Of_Publications 
FROM publication 
GROUP BY Publisher;
```    

""",
    """
Here's an example for you:
Question: Which papers were written by "Sharon Goldwater"?
Answer:
Reasoning process:
According to the table information, the relationship between authors and papers is established through the writes table, and author information is contained in the author table. Therefore, the question can be answered by connecting the writes and author tables. The query needs to focus on the author information corresponding to the authorId in the writes table for Sharon Goldwater and determine which papers this author has written.

Generated SQL:
```
SELECT writes.paperId
FROM writes
JOIN author ON writes.authorId = author.authorId
WHERE author.authorName = 'Sharon Goldwater'
```    

"""

]

synonymous_prompt = f"""Give you a sentence, please write a sentence with the same meaning as this sentence.
Requirements:
1 - Try to use a different sentence structure and expression method.
2 - Maintain consistent semantics.
3 - Do not provide any explanations.

Some examples about this question:

Q: How many singers do we have?
A: What is the total count of singers?

Q: Display the names, countries, and ages of each singer, sorted from oldest to youngest.
A: Show the names, countries, and ages of each singer, sorted in descending order of age.

Q: Show the names and release years of songs by the youngest singer.
A: What are the names and release years of all songs by the youngest singer?

Q: From which different countries do singers above 20 years old come?
A: Which countries have singers above 20 years old?

Q: Return the names of countries with at least 3 different languages and the number of languages for each.
A: What are the names of countries that speak more than 2 languages, and how many languages do they speak?

Q: Find the number of cities in each region where the population is above the average population of all cities.
A: How many cities in each region have a population higher than the average population of all cities?

Q: What are the orchestra record companies sorted in descending order of establishment year?
A: Provide the names of music companies with orchestras, sorted in descending order of establishment year.

Q: List the airport code and name for the city of "Lhasa."
A: Give the airport code and airport name corresponding to the city "Lhasa."

Q:
"""


print(few_shot_examples_spider[0])

with open("few_shot_examples.json", "w") as f:
    save_results = {
        "spider_cot_generation": few_shot_examples_spider,
        "spider_synonymous": synonymous_prompt
    }
    json.dump(save_results, f, indent=2, ensure_ascii=False)
