import re
import json
# TODO 以JSON的形式去读取few-shot-examples


with open("configures/few_shot_examples.json") as f:
    few_shot_map = json.load(f)

few_shot_examples_cspider = [
    """
这里给你一个样例：
问题：不属于“长白山脉”的山脉的名称、高度和突出度是什么？
回答：
推理过程：
1. 需要从哪些表中获取信息？答案：问题要查询山脉的名称，因此需要使用表 mountain。
2. 需要获取哪些列的信息？答案：问题问了山脉的名称、高度和突出度，因此需要使用列 name、Height、Prominence。
3. 需要加入哪些条件来筛选符合要求的行？答案：列 Range 不属于“长白山脉”的山脉。
4. 需要连接哪些表来获取所有必要的信息？答案：不需要连接其他表。

根据以上思考过程，生成的SQL查询语句如下：

生成的SQL：
```
SELECT name, Height, Prominence FROM mountain WHERE Range != '长白山脉';
```

""",
    """
这里给你一个样例：
问题：给我每个博物馆的详细时间和开放时间。
回答：
推理过程：
首先，这个问题涉及到博物馆和开放时间这两个实体和属性。我们需要从Tourist_Attractions和Museums这两个表中检索数据。我们还需要连接这两个表，以便获取每个博物馆的详细时间和开放时间。

基于这些想法，我们可以使用以下SQL查询语句来解决问题：

生成的SQL：
```
SELECT Museums.Museum_Details, Tourist_Attractions.Opening_Hours
FROM Museums
INNER JOIN Tourist_Attractions ON Museums.Museum_ID = Tourist_Attractions.Tourist_Attraction_ID;
```

""",
    """
这里给你一个样例：
问题：找出以前从未提出过投诉的客户的电子邮件和电话号码。
回答：
推理过程：
1. 需要从 Customers 表中筛选出从未提出过投诉的客户。
2. 需要选取这些客户的电子邮件和电话号码。

生成的SQL：
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
这里给你一个样例：
问题：按姓氏排序的所有人的名字、中间名和姓氏是什么？
回答：1. 查询个人信息肯定要用到Individuals表
2. 要按照姓氏排序，那么需要用ORDER BY语句，并且需要根据姓氏排序，对于英语来说，姓氏通常在名字的最后面，因此需要用Individuals表中的individual_last_name字段排序。
3. 结果中需要显示所有人的名字、中间名和姓氏，因此需要选择Individuals表中的individual_first_name、individual_middle_name、individual_last_name三个字段。

生成的SQL：
```
SELECT individual_first_name, individual_middle_name, individual_last_name 
FROM Individuals 
ORDER BY individual_last_name;
```

""",
    """
这里给你一个样例：
问题：GPA最低的学生的院系名称是什么？
回答：
推理过程：
首先，我们需要找到GPA最低的学生，因此需要从学生表中筛选出GPA字段最小的那个学生。然后，需要找到该学生所属的院系名称，因此需要通过学生表和系部表的关联来得到院系名称。
综上，我们需要使用学生表和系部表的联表查询，且需要将GPA字段作为查询条件，以及按GPA字段从小到大排序。最终筛选出第一条数据即为GPA最低的学生所在院系的名称。

生成的SQL：
```
SELECT DEPARTMENT.DEPT_NAME
FROM DEPARTMENT, STUDENT
WHERE STUDENT.DEPT_CODE = DEPARTMENT.DEPT_CODE
ORDER BY STUDENT.STU_GPA ASC
LIMIT 1;
```

""",
    """
这里给你一个样例：
问题：“克里斯托弗·曼宁”有多少论文出版物？
回答：
推理过程：
首先，我们需要找到“克里斯托弗·曼宁”的作者ID，可以通过在“author”表中查询作者名字得到，然后我们需要在“writes”表中找到他写过的所有论文ID。接着，在“paper”表中找到这些论文，并统计它们的数量即可。

生成的SQL：
```
SELECT COUNT(DISTINCT paper.paperId) AS paper_count
FROM author
JOIN writes ON author.authorId = writes.authorId
JOIN paper ON writes.paperId = paper.paperId
WHERE author.authorName = '克里斯托弗·曼宁';
```

""",
    """
这里给你一个样例：
问题：展示不同的出版商以及他们出版的出版物数量。
回答：
推理过程：
第一步：我们需要从 publication 表中得到不同的出版商以及他们出版的出版物数量，所以我们需要用到 Publisher 列和 COUNT()。
第二部：我们需要用到 GROUP BY 来按照出版商分组。

生成的SQL：
```
SELECT Publisher, COUNT(*) AS Num_Of_Publications 
FROM publication 
GROUP BY Publisher;
```

""",
    """
这里给你一个样例：
问题：“莎朗·戈德华特”写了哪些论文？
回答：
推理过程：
根据表信息，写作者和论文之间的关系通过writes表建立，而作者的信息包含在author表中，因此问题可以通过连接writes和author表来回答。查询需要关注莎朗·戈德华特在writes表中的authorId对应的作者信息，并且该作者写了哪些论文。

生成的SQL：
```
SELECT writes.paperId
FROM writes
JOIN author ON writes.authorId = author.authorId
WHERE author.authorName = '莎朗·戈德华特'
```

""",

]

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

few_shot_examples = [
    """
这里给你一个样例：
问题：在“中国”注册的公司的电影和书籍的名称是什么？
回答：
推理过程：
从问题中明确知道需要涉及"公司"、"电影"和"书籍"三个概念的数据，这些概念对应的表格，分别是：culture_company、movie和book_club。
然后，是如何从公司找到相关的电影和书籍。从Schema中可以看出，culture_company表中有movie_id和book_club_id两个字段，它们正好是另外两个表的主键。这意味着我们可以使用JOIN操作来关联这三个表。
此外，问题中提到了"在中国注册的公司"，那么需要在查询的WHERE子句中添加条件以筛选出这些公司。

根据以上思考过程，生成的SQL查询语句如下：

生成的SQL：
```
SELECT T1.title ,  T3.book_title FROM movie AS T1 JOIN culture_company AS T2 ON T1.movie_id  =  T2.movie_id JOIN book_club AS T3 ON T3.book_club_id  =  T2.book_club_id WHERE T2.incorporated_in  =  "中国";

```

""",
    """
这里给你一个样例：
问题：对于最大速度高于平均速度的风暴，返回总死亡人数和以百万计的总损失。
回答：
推理过程：
首先，我们要找出所有风暴的平均最大速度，这需要我们在"storm"表上进行查询。然后，我们需要找到那些最大速度高于这个平均速度的风暴，并且对它们的总死亡人数和总损失进行累加。
这个问题实际上涉及到两个子查询：

1. 计算所有风暴的平均最大速度：SELECT AVG(Max_speed) FROM storm
2. 计算最大速度高于这个平均值的风暴的总死亡人数和总损失：SELECT SUM(Number_Deaths), SUM(Damage_millions_USD) FROM storm WHERE Max_speed > (子查询一)

根据以上思考过程，生成的SQL查询语句如下：

生成的SQL：
```
SELECT SUM(Number_Deaths), SUM(Damage_millions_USD) FROM storm WHERE Max_speed > (SELECT AVG(Max_speed) FROM storm);

```

""",
    """
这里给你一个样例：
问题：不属于“长白山脉”的山脉的名称、高度和突出度是什么？
回答：
推理过程：
1. 需要从哪些表中获取信息？答案：问题要查询山脉的名称，因此需要使用表 mountain。
2. 需要获取哪些列的信息？答案：问题问了山脉的名称、高度和突出度，因此需要使用列 name、Height、Prominence。
3. 需要加入哪些条件来筛选符合要求的行？答案：列 Range 不属于“长白山脉”的山脉。
4. 需要连接哪些表来获取所有必要的信息？答案：不需要连接其他表。

根据以上思考过程，生成的SQL查询语句如下：

生成的SQL：
```
SELECT name, Height, Prominence FROM mountain WHERE Range != '长白山脉';
```

""",
    """
这里给你一个样例：
问题：给我每个博物馆的详细时间和开放时间。
回答：
推理过程：
首先，这个问题涉及到博物馆和开放时间这两个实体和属性。我们需要从Tourist_Attractions和Museums这两个表中检索数据。我们还需要连接这两个表，以便获取每个博物馆的详细时间和开放时间。

基于这些想法，我们可以使用以下SQL查询语句来解决问题：

生成的SQL：
```
SELECT Museums.Museum_Details, Tourist_Attractions.Opening_Hours
FROM Museums
INNER JOIN Tourist_Attractions ON Museums.Museum_ID = Tourist_Attractions.Tourist_Attraction_ID;
```

""",
    """
这里给你一个样例：
问题：找出以前从未提出过投诉的客户的电子邮件和电话号码。
回答：
推理过程：
1. 需要从 Customers 表中筛选出从未提出过投诉的客户。
2. 需要选取这些客户的电子邮件和电话号码。

生成的SQL：
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
这里给你一个样例：
问题：按姓氏排序的所有人的名字、中间名和姓氏是什么？
回答：1. 查询个人信息肯定要用到Individuals表
2. 要按照姓氏排序，那么需要用ORDER BY语句，并且需要根据姓氏排序，对于英语来说，姓氏通常在名字的最后面，因此需要用Individuals表中的individual_last_name字段排序。
3. 结果中需要显示所有人的名字、中间名和姓氏，因此需要选择Individuals表中的individual_first_name、individual_middle_name、individual_last_name三个字段。

生成的SQL：
```
SELECT individual_first_name, individual_middle_name, individual_last_name 
FROM Individuals 
ORDER BY individual_last_name;
```

""",
    """
这里给你一个样例：
问题：GPA最低的学生的院系名称是什么？
回答：
推理过程：
首先，我们需要找到GPA最低的学生，因此需要从学生表中筛选出GPA字段最小的那个学生。然后，需要找到该学生所属的院系名称，因此需要通过学生表和系部表的关联来得到院系名称。
综上，我们需要使用学生表和系部表的联表查询，且需要将GPA字段作为查询条件，以及按GPA字段从小到大排序。最终筛选出第一条数据即为GPA最低的学生所在院系的名称。

生成的SQL：
```
SELECT DEPARTMENT.DEPT_NAME
FROM DEPARTMENT, STUDENT
WHERE STUDENT.DEPT_CODE = DEPARTMENT.DEPT_CODE
ORDER BY STUDENT.STU_GPA ASC
LIMIT 1;
```

""",
    """
这里给你一个样例：
问题：“克里斯托弗·曼宁”有多少论文出版物？
回答：
推理过程：
首先，我们需要找到“克里斯托弗·曼宁”的作者ID，可以通过在“author”表中查询作者名字得到，然后我们需要在“writes”表中找到他写过的所有论文ID。接着，在“paper”表中找到这些论文，并统计它们的数量即可。

生成的SQL：
```
SELECT COUNT(DISTINCT paper.paperId) AS paper_count
FROM author
JOIN writes ON author.authorId = writes.authorId
JOIN paper ON writes.paperId = paper.paperId
WHERE author.authorName = '克里斯托弗·曼宁';
```

""",
    """
这里给你一个样例：
问题：展示不同的出版商以及他们出版的出版物数量。
回答：
推理过程：
第一步：我们需要从 publication 表中得到不同的出版商以及他们出版的出版物数量，所以我们需要用到 Publisher 列和 COUNT()。
第二部：我们需要用到 GROUP BY 来按照出版商分组。

生成的SQL：
```
SELECT Publisher, COUNT(*) AS Num_Of_Publications 
FROM publication 
GROUP BY Publisher;
```

""",
    """
这里给你一个样例：
问题：“莎朗·戈德华特”写了哪些论文？
回答：
推理过程：
根据表信息，写作者和论文之间的关系通过writes表建立，而作者的信息包含在author表中，因此问题可以通过连接writes和author表来回答。查询需要关注莎朗·戈德华特在writes表中的authorId对应的作者信息，并且该作者写了哪些论文。

生成的SQL：
```
SELECT writes.paperId
FROM writes
JOIN author ON writes.authorId = author.authorId
WHERE author.authorName = '莎朗·戈德华特'
```

""",

]

def find_outermost_parentheses(text):
    left_index = -1
    right_index = -1
    inner_text = ""

    for i, char in enumerate(text):
        if char == '(':
            left_index = i
            break
    for i, char in enumerate(text[::-1]):
        if char == ')':
            right_index = len(text) - i - 1
            break

    if left_index != -1 and right_index != -1:
        inner_text = text[left_index + 1:right_index]

    return left_index, right_index, inner_text
def hs_schema_template_1(tables, fks):
    schema_sequence = "数据库信息：\n"
    pattern = r'(\w+)\(([^()]+)\)'
    for table_name, columns in tables.items():
        schema_sequence += "表名：\n"
        schema_sequence += f"{table_name}\n"
        schema_sequence += "字段信息（字段名 - 字段中文名）：\n"
        for column in columns:
            print(column)
            l, r, zh_name = find_outermost_parentheses(column)
            en_name = column[:l]
            print(en_name, zh_name)
            schema_sequence += f"{en_name} - {zh_name}\n"
        schema_sequence += "\n"
    fk_sequence = "外键：\n"
    for fk in fks:
        fk_sequence += f"{fk}\n"
    return schema_sequence, fk_sequence


def schema_template_1(tables, fks):
    schema_sequence = ""
    for table_name, columns in tables.items():
        # print(columns)
        column_sequence = " , ".join(columns)
        # print(column_sequence)
        schema_sequence += f"# {table_name} ( {column_sequence} )\n"
    # print(schema_sequence)
    fk_sequence = ""
    for fk in fks:
        fk_sequence += f"# {fk}\n"
    # print(fk_sequence)
    return schema_sequence[:-1], fk_sequence[:-1]


def schema_template_2_en(tables, fks):
    schema_sequence = ""
    for table_name, columns in tables.items():
        # print(columns)
        column_sequence = " , ".join(columns)
        # print(column_sequence)
        schema_sequence += f"table {table_name} contains columns： {column_sequence} \n"
    # print(schema_sequence)
    fk_sequence = ""
    for fk in fks:
        fk_sequence += f"{fk} , "
    # print(fk_sequence)
    fk_sequence = fk_sequence[:-2]
    return schema_sequence[:-1], fk_sequence


def schema_template_2(tables, fks):
    schema_sequence = ""
    for table_name, columns in tables.items():
        # print(columns)
        column_sequence = " , ".join(columns)
        # print(column_sequence)
        schema_sequence += f"表 {table_name} 包含字段： {column_sequence} \n"
    # print(schema_sequence)
    fk_sequence = ""
    for fk in fks:
        fk_sequence += f"{fk} , "
    # print(fk_sequence)
    fk_sequence = fk_sequence[:-2]
    return schema_sequence[:-1], fk_sequence


def schema_template_3(tables, fks):
    schema_sequence = "[ "
    for table_name, columns in tables.items():
        # print(columns)
        columns_for_each_table = []
        for column in columns:
            columns_for_each_table.append(f"{table_name}.{column}")
        column_sequence = " , ".join(columns_for_each_table)
        # print(column_sequence)
        schema_sequence += f"{column_sequence} , "
    schema_sequence = schema_sequence[:-2]
    schema_sequence += "]"
    # print(schema_sequence)
    #
    # exit()
    fk_sequence = "[ "
    for fk in fks:
        fk_sequence += f"{fk} , "
    # print(fk_sequence)
    fk_sequence = fk_sequence[:-2]
    fk_sequence += "]\n"
    return schema_sequence, fk_sequence


schema_template_func_map = {
    "1": schema_template_1,
    "2": schema_template_2,
    "3": schema_template_3,
}


def instruction_cot_spider_1(schema, fks, question):
    prompt = f"""Providing you with the database schema information and a question, performing the following tasks:
1 - Output the SQL query statement corresponding to this question.

Notes:
1 - When generating the SQL, only the relevant parts corresponding to the question need to be included, without additional output of tables and columns.
2 - You should first present your intermediate thought process, and then provide the final SQL in the following format:
Generated SQL:
```
{{sql}}
```

###
Schema:
{schema}
Foreign keys: 
{fks}

Question:
{question}
### 

"""
    return prompt


def instruction_en_1(schema, fks, question):
    prompt = f"""Providing you with the database schema information and a question, performing the following tasks:
1 - Output the SQL query statement corresponding to this question.

Notes:
1 - When generating the SQL, only the relevant parts corresponding to the question need to be included, without additional output of tables and columns.
2 - Directly output the final SQL in the following format:
Generated SQL:
```
{{sql}}
```

###
Schema:
{schema}
Foreign keys: 
{fks}

Question:
{question}
### 

"""
    return prompt


def instruction_1(schema, fks, question):
    schema_sequence = schema + fks
    prompt = f"""给你数据库Schema信息以及一个问题，执行以下任务：
1 - 输出这条问题对应的SQL查询语句。

注意：
1 - 在生成SQL的时候只需要输出问题中对应的部分，不要额外输出表和列。
2 - 你需要先输出你的中间思考过程，再以如下形式输出最终SQL: 
生成的SQL：
```
{{sql}}
```

###
Schema:
{schema}
Foreign keys: 
{fks}

Question:
{question}
### 

"""
    # print(prompt)

    return prompt


def instruction_cot_spider_2(schema, fks, question):
    prompt = f"""I have a question for you. I need you to write the corresponding SQL query for this question. To make it easier for you to compose the SQL, I will provide you with the database schema information. Please start by outlining your thought process, and finally, provide the SQL in the following format:
Generated SQL:
```
{{sql}}
```

###
Schema: 
{schema} 
Foreign keys: 
{fks}

Question: 
{question}
### 

"""
    return prompt


def instruction_en_2(schema, fks, question):
    prompt = f"""I have a question for you. I need you to write the corresponding SQL query for this question. To make it easier for you to compose the SQL, I will provide you with the database schema information. Please provide the SQL in the following format:
Generated SQL:
```
{{sql}}
```

###
Schema: 
{schema} 
Foreign keys: 
{fks}

Question: 
{question}
### 

"""
    return prompt


def instruction_2(schema, fks, question):
    schema_sequence = schema + fks
    prompt = f"""给你一个问题，你需要写出该问题对应的SQL，为了方便你撰写SQL，我将会提供数据库Schema信息。
请先写出你的思考过程，最后直接如下格式输出最终的SQL： 
生成的SQL：
```
{{sql}}
```


###
Schema: 
{schema} 
Foreign keys: 
{fks}

Question: 
{question}
### 

"""
    # print(prompt)
    return prompt


def instruction_cot_spider_3(schema, fks, question):
    prompt = f"""Given the provided database schema information and a question, please write the corresponding SQL query statement for the question.

"Question":
{question}
"Table Information":
{schema}
"Foreign Keys":
{fks}

Please start by outlining your thought process, and then output the final SQL in the following format:
Generated SQL:
```
{{sql}}
```
"""
    return prompt


def instruction_en_3(schema, fks, question):
    prompt = f"""Given the provided database schema information and a question, please write the corresponding SQL query statement for the question.

"Question":
{question}
"Table Information":
{schema}
"Foreign Keys":
{fks}

Please output the final SQL in the following format without any explanations:
Generated SQL:
```
{{sql}}
```
"""
    return prompt


def instruction_3(schema, fks, question):
    prompt = f"""给定以下数据库Schema信息和一个问题，请为该问题编写相应的SQL查询语句。

"问题": 
{question}
"表信息": 
{schema}
"外键": 
{fks}

请先写出你的思考过程，然后用下面的格式输出最终SQL: 
生成的SQL：
```
{{sql}}
```
"""
    # print(prompt)
    return prompt


def instruction_no_cot_1(schema, fks, question):
    prompt = f"""给你数据库Schema信息以及一个问题，执行以下任务：
1 - 输出这条问题对应的SQL查询语句。

注意：
1 - 在生成SQL的时候只需要输出问题中对应的部分，不要额外输出表和列。
2 - 请以如下形式直接输出最终SQL: 
生成的SQL：
```
{{sql}}
```

###
Schema:
{schema}
Foreign keys: 
{fks}

Question:
{question}
### 

    """
    # print(prompt)

    return prompt


def instruction_no_cot_2(schema, fks, question):
    prompt = f"""给你一个问题，你需要写出该问题对应的SQL，为了方便你撰写SQL，我将会提供数据库Schema信息。
请在最后直接如下格式输出最终的SQL： 
生成的SQL：
```
{{sql}}
```


###
Schema: 
{schema} 
Foreign keys: 
{fks}

Question: 
{question}
### 

    """
    # print(prompt)
    return prompt


def instruction_no_cot_3(schema, fks, question):
    prompt = f"""给定以下数据库Schema信息和一个问题，请为该问题编写相应的SQL查询语句。

"问题": 
{question}
"表信息": 
{schema}
"外键": 
{fks}

请用下面的格式输出最终SQL: 
生成的SQL：
```
{{sql}}
```
"""
    # print(prompt)
    return prompt


def instruction_skeleton_spider_1(schema, fks, question):
    prompt = f"""Here is the database schema information and a question for you to perform the following tasks:
1. Output the skeleton of the SQL statement corresponding to this question.
2. Output the SQL query statement corresponding to this question.

Note:
1. When generating the SQL, only the relevant parts from the question need to be included. Do not provide additional information about tables and columns.
2. Please provide the final SQL output in the following format: .

Generated SQL skeleton：
```
{{sql skeleton}}
```
Generated SQL：
```
{{sql}}
```

###
Schema:
{schema}
Foreign keys: 
{fks}

Question:
{question}
### 

"""

    return prompt


def instruction_no_cot_skeleton_1(schema, fks, question):
    prompt = f"""给你数据库Schema信息以及一个问题，执行以下任务:
1 - 输出这条问题对应的SQL语句的结构;
2 - 输出这条问题对应的SQL查询语句。

注意：
1 - 在生成SQL的时候只需要输出问题中对应的部分，不要额外输出表和列。
2 - 请以如下形式直接输出最终SQL:
生成的SQL结构:
```
{{sql结构}}
```
生成的SQL:
```
{{sql}}
```

###
Schema:
{schema}
Foreign keys: 
{fks}

Question:
{question}
### 

    """
    # print(prompt)

    return prompt


def instruction_skeleton_spider_2(schema, fks, question):
    prompt = f"""Given you a question, you need to write the corresponding SQL. To facilitate you in composing the SQL, I will provide the database schema information. Please provide the SQL skeleton and the final SQL in the following format at the end:
Generated SQL skeleton:
```
{{sql skeleton}}
```
Generated SQL:
```
{{sql}}
```


###
Schema: 
{schema} 
Foreign keys: 
{fks}

Question: 
{question}
### 

"""
    # print(prompt)
    return prompt


def instruction_no_cot_skeleton_2(schema, fks, question):
    prompt = f"""给你一个问题，你需要写出该问题对应的SQL，为了方便你撰写SQL，我将会提供数据库Schema信息。
请在最后直接如下格式输出SQL结构和最终的SQL： 
生成的SQL结构：
```
{{sql结构}}
```
生成的SQL：
```
{{sql}}
```


###
Schema: 
{schema} 
Foreign keys: 
{fks}

Question: 
{question}
### 

    """
    # print(prompt)
    return prompt


def instruction_skeleton_spider_3(schema, fks, question):
    prompt = f"""Given the following database schema information and a question, please write the corresponding SQL query statement for the question.

"Question":
{question}
"Table information":
{schema}
"Foreign keys":
{fks}

Please output the SQL skeleton and the final SQL in the following format: 
Generated SQL skeleton:
```
{{sql skeleton}}
```
Generated SQL:
```
{{sql}}
```
"""
    # print(prompt)
    return prompt


def instruction_no_cot_skeleton_3(schema, fks, question):
    prompt = f"""给定以下数据库Schema信息和一个问题，请为该问题编写相应的SQL查询语句。

"问题": 
{question}
"表信息": 
{schema}
"外键": 
{fks}

请用下面的格式输出SQL结构和最终SQL: 
生成的SQL结构：
```
{{sql结构}}
```
生成的SQL：
```
{{sql}}
```
"""
    # print(prompt)
    return prompt


def instruction_generate_skeleton_1(schema, fks, question):
    prompt = f"""给你数据库Schema信息以及一个问题，执行以下任务：
1 - 输出这条问题对应的SQL语句的结构；

注意：
1 - SQL结构是指把完整SQL的表和列用下划线_代替。
2 - 请以如下形式直接输出最终SQL: 
生成的SQL结构：
```
{{sql结构}}
```

###
Schema:
{schema}
Foreign keys: 
{fks}

Question:
{question}
### 

"""
    # print(prompt)

    return prompt


def instruction_generate_skeleton_2(schema, fks, question):
    prompt = f"""给你一个问题，你需要写出该问题对应SQL的结构，为了方便你撰写SQL，我将会提供数据库Schema信息。
请在最后直接如下格式输出SQL结构： 
生成的SQL结构：
```
{{sql结构}}
```

###
Schema: 
{schema} 
Foreign keys: 
{fks}

Question: 
{question}
### 

"""
    # print(prompt)
    return prompt


def instruction_generate_skeleton_3(schema, fks, question):
    prompt = f"""给定以下数据库Schema信息和一个问题，请为该问题编写相应的SQL查询语句的结构。

"问题": 
{question}
"表信息": 
{schema}
"外键": 
{fks}

请用下面的格式输出SQL结构: 
生成的SQL结构：
```
{{sql结构}}
```
"""
    # print(prompt)
    return prompt


def generate_skeleton_output_template_zh(gold_sql=None, skeleton=None):
    output = f"""生成的SQL结构：
```
{skeleton}
```
"""
    return output


def no_cot_skeleton_output_template_zh(gold_sql=None, skeleton=None):
    output = f"""生成的SQL结构：
```
{skeleton}
```
生成的SQL：
```
{gold_sql}
```
"""
    return output


def normal_sql_output_template_zh(gold_sql=None, skeleton=None):
    output = f"""生成的SQL：
```
{gold_sql}
```"""
    return output


def normal_sql_output_template(gold_sql):
    output = f"""Generated SQL:
```
{gold_sql}
```"""
    return output


def skeleton_output_template(gold_sql, skeleton):
    output = f"""Generated SQL skeleton：
```
{skeleton}
```
Generated SQL:
```
{gold_sql}
```
"""
    return output


schema_template_list = [
    schema_template_1,
    schema_template_2,
    schema_template_3,
]

schema_template_en_list = [
    schema_template_1,
    schema_template_2_en,
    schema_template_3,
]

instruction_cot_spider_template_list = [
    instruction_cot_spider_1,
    instruction_cot_spider_2,
    instruction_cot_spider_3,
]

instruction_template_list = [
    instruction_1,
    instruction_2,
    instruction_3,
]

instruction_spider_template_list = [
    instruction_en_1,
    instruction_en_2,
    instruction_en_3,
]

instruction_no_cot_template_list = [
    instruction_no_cot_1,
    instruction_no_cot_2,
    instruction_no_cot_3,
]

instruction_no_cot_skeleton_template_list = [
    instruction_no_cot_skeleton_1,
    instruction_no_cot_skeleton_2,
    instruction_no_cot_skeleton_3,
]

instruction_skeleton_spider_template_list = [
    instruction_skeleton_spider_1,
    instruction_skeleton_spider_2,
    instruction_skeleton_spider_3,
]

instruction_generate_skeleton_template_list = [
    instruction_generate_skeleton_1,
    instruction_generate_skeleton_2,
    instruction_generate_skeleton_3,
]
