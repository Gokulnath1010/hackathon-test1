import csv

from django.conf import settings
from django.shortcuts import redirect, render

RESULTS_FILE = settings.BASE_DIR / 'student_results.csv'

QUESTIONS = [
	{
		'id': 1,
		'topic': 'Quantitative aptitude',
		'text': 'A train travels 360 km in 4 hours. What is its average speed?',
		'options': ['72 km/h', '80 km/h', '90 km/h', '96 km/h'],
		'answer': '90 km/h',
	},
	{
		'id': 2,
		'topic': 'Logical reasoning',
		'text': 'Find the next number in the series: 3, 7, 15, 31, __',
		'options': ['47', '55', '63', '65'],
		'answer': '63',
	},
	{
		'id': 3,
		'topic': 'English language',
		'text': 'Choose the word closest in meaning to “concise”.',
		'options': ['Careful', 'Brief', 'Confusing', 'Persuasive'],
		'answer': 'Brief',
	},
	{
		'id': 4,
		'topic': 'General awareness',
		'text': 'Which planet is known for its prominent ring system?',
		'options': ['Mars', 'Jupiter', 'Saturn', 'Neptune'],
		'answer': 'Saturn',
	},
]

PYTHON_QUESTIONS = [
	{'id': 1, 'topic': 'Python output', 'text': 'What is the output?', 'code': 'x = [1, 2, 3]\ny = x\ny.append(4)\nprint(x)', 'options': ['[1, 2, 3]', '[1, 2, 3, 4]', '[4]', 'Error'], 'answer': '[1, 2, 3, 4]'},
	{'id': 2, 'topic': 'Python booleans', 'text': 'What is the output?', 'code': 'print(bool([]), bool([0]))', 'options': ['True True', 'False False', 'False True', 'True False'], 'answer': 'False True'},
	{'id': 3, 'topic': 'Python slicing', 'text': 'What does this produce?', 'code': 'x = [1, 2, 3, 4, 5]\nprint(x[::-2])', 'options': ['[5, 3, 1]', '[1, 3, 5]', '[5, 4, 3]', '[2, 4]'], 'answer': '[5, 3, 1]'},
	{'id': 4, 'topic': 'Python scope', 'text': 'What is the output?', 'code': 'a = 10\n\ndef test():\n    a = 20\n\ntest()\nprint(a)', 'options': ['10', '20', 'None', 'Error'], 'answer': '10'},
	{'id': 5, 'topic': 'Python identity', 'text': 'What is the output?', 'code': 'x = [1, 2, 3]\n\nprint(x == x[:])\nprint(x is x[:])', 'options': ['True True', 'False False', 'True False', 'False True'], 'answer': 'True False'},
	{'id': 6, 'topic': 'Python sets', 'text': 'What is the output?', 'code': 'a = {1, 2, 3}\nb = {3, 4, 5}\n\nprint(a & b)', 'options': ['{1, 2, 3, 4, 5}', '{3}', '{1, 2}', 'Error'], 'answer': '{3}'},
	{'id': 7, 'topic': 'List comprehension', 'text': 'What is the output?', 'code': 'x = [i*i for i in range(5) if i % 2 == 0]\nprint(x)', 'options': ['[1, 9]', '[0, 4, 16]', '[0, 2, 4]', '[1, 4, 9]'], 'answer': '[0, 4, 16]'},
	{'id': 8, 'topic': 'Python functions', 'text': 'What does *args allow in a function?', 'code': '', 'options': ['Multiple keyword arguments', 'Multiple positional arguments', 'Only one argument', 'No arguments'], 'answer': 'Multiple positional arguments'},
	{'id': 9, 'topic': 'Default arguments', 'text': 'What is the output?', 'code': 'def func(x=[]):\n    x.append(1)\n    return x\n\nprint(func())\nprint(func())', 'options': ['[1]\n[1]', '[1]\n[1, 1]', '[1, 1]\n[1, 1]', 'Error'], 'answer': '[1]\n[1, 1]'},
	{'id': 10, 'topic': 'Python lists', 'text': 'What is the output?', 'code': 'x = [10, 20, 30, 40]\nx.pop(1)\nprint(x)', 'options': ['[10, 30, 40]', '[20, 30, 40]', '[10, 20, 40]', '[10, 20, 30]'], 'answer': '[10, 30, 40]'},
	{'id': 11, 'topic': 'Closures', 'text': 'What is the output?', 'code': 'def outer():\n    x = 10\n\n    def inner():\n        nonlocal x\n        x += 5\n\n    inner()\n    return x\n\nprint(outer())', 'options': ['10', '15', '5', 'Error'], 'answer': '15'},
	{'id': 12, 'topic': 'Copying lists', 'text': 'What is the output?', 'code': 'a = [1, 2, 3]\nb = a.copy()\n\nb[0] = 100\n\nprint(a)', 'options': ['[100, 2, 3]', '[1, 2, 3]', '[100]', 'Error'], 'answer': '[1, 2, 3]'},
	{'id': 13, 'topic': 'Immutable types', 'text': 'Which one is immutable?', 'code': '', 'options': ['List', 'Dictionary', 'Set', 'Tuple'], 'answer': 'Tuple'},
	{'id': 14, 'topic': 'Generators', 'text': 'What does yield create/use?', 'code': '', 'options': ['Class', 'Generator', 'Exception', 'Thread'], 'answer': 'Generator'},
	{'id': 15, 'topic': 'Generator functions', 'text': 'What is the output?', 'code': 'def gen():\n    yield 1\n    yield 2\n    yield 3\n\ng = gen()\n\nprint(next(g))\nprint(next(g))', 'options': ['1\n1', '1\n2', '2\n3', 'Error'], 'answer': '1\n2'},
	{'id': 16, 'topic': 'Exception handling', 'text': 'Which keyword is used to handle exceptions?', 'code': '', 'options': ['catch', 'error', 'except', 'handle'], 'answer': 'except'},
	{'id': 17, 'topic': 'Lambda functions', 'text': 'What is the output?', 'code': 'x = lambda a, b: a if a > b else b\nprint(x(10, 20))', 'options': ['10', '20', '30', 'Error'], 'answer': '20'},
	{'id': 18, 'topic': 'Tuple unpacking', 'text': 'What is the output?', 'code': 'a = 10\nb = 20\n\na, b = b, a\n\nprint(a, b)', 'options': ['10 20', '20 10', '10 10', '20 20'], 'answer': '20 10'},
	{'id': 19, 'topic': 'Generators', 'text': 'What is the main advantage of a generator?', 'code': '', 'options': ['Faster CPU', 'Lower memory usage', 'Automatic database connection', 'Better graphics'], 'answer': 'Lower memory usage'},
	{'id': 20, 'topic': 'List iteration', 'text': 'What will happen here?', 'code': 'x = [1, 2, 3]\n\nfor i in x:\n    x.append(i)\n\nprint(x)', 'options': ['Prints [1,2,3]', 'Prints [1,2,3,1,2,3] and stops', 'Can continue indefinitely', 'Syntax error'], 'answer': 'Can continue indefinitely'},
	{'id': 21, 'topic': 'Python lists', 'text': 'What is the output?', 'code': 'x = [10, 20, 30]\nprint(len(x))', 'options': ['2', '3', '4', 'Error'], 'answer': '3'},
	{'id': 22, 'topic': 'Python lists', 'text': 'Which method is used to add an element at the end of a list?', 'code': '', 'options': ['add()', 'insert()', 'append()', 'push()'], 'answer': 'append()'},
	{'id': 23, 'topic': 'Python strings', 'text': 'What is the output?', 'code': 'x = "Python"\nprint(x[1:4])', 'options': ['Pyt', 'yth', 'tho', 'Python'], 'answer': 'yth'},
	{'id': 24, 'topic': 'Python operators', 'text': 'What is the output?', 'code': 'a = 10\nb = 3\nprint(a // b)', 'options': ['3.33', '3', '4', '1'], 'answer': '3'},
	{'id': 25, 'topic': 'Python functions', 'text': 'Which keyword is used to define a function in Python?', 'code': '', 'options': ['function', 'define', 'def', 'fun'], 'answer': 'def'},
	{'id': 26, 'topic': 'Python lists', 'text': 'What is the output?', 'code': 'x = [1, 2, 3, 4]\nprint(x[-1])', 'options': ['1', '2', '3', '4'], 'answer': '4'},
	{'id': 27, 'topic': 'Python sets', 'text': 'What is the output?', 'code': 'x = {1, 2, 2, 3, 3}\nprint(len(x))', 'options': ['5', '4', '3', '2'], 'answer': '3'},
	{'id': 28, 'topic': 'Python loops', 'text': 'Which statement is used to skip the current iteration of a loop?', 'code': '', 'options': ['break', 'continue', 'pass', 'skip'], 'answer': 'continue'},
	{'id': 29, 'topic': 'Python range', 'text': 'What is the output?', 'code': 'for i in range(2, 6):\n    print(i, end=" ")', 'options': ['2 3 4 5', '2 3 4 5 6', '1 2 3 4 5', '3 4 5 6'], 'answer': '2 3 4 5'},
	{'id': 30, 'topic': 'Python dictionaries', 'text': 'What is the output?', 'code': 'x = {"name": "Gogul", "age": 25}\nprint(x["name"])', 'options': ['name', 'Gogul', 'age', 'Error'], 'answer': 'Gogul'},
]

JAVA_QUESTIONS = [
	{'id': 1, 'topic': 'Java objects', 'text': 'Which keyword is used to create an object in Java?', 'code': '', 'options': ['class', 'new', 'object', 'create'], 'answer': 'new'},
	{'id': 2, 'topic': 'Java data types', 'text': 'What is the default value of an int instance variable?', 'code': '', 'options': ['null', '0', '1', 'undefined'], 'answer': '0'},
	{'id': 3, 'topic': 'Java entry point', 'text': 'Which method is the entry point of a Java program?', 'code': '', 'options': ['start()', 'run()', 'main()', 'execute()'], 'answer': 'main()'},
	{'id': 4, 'topic': 'Java primitives', 'text': 'Which of these is NOT a primitive data type?', 'code': '', 'options': ['int', 'double', 'String', 'boolean'], 'answer': 'String'},
	{'id': 5, 'topic': 'Java inheritance', 'text': 'Which keyword is used for inheritance?', 'code': '', 'options': ['inherits', 'extends', 'implements', 'super'], 'answer': 'extends'},
	{'id': 6, 'topic': 'Java collections', 'text': 'Which collection does NOT allow duplicate elements?', 'code': '', 'options': ['ArrayList', 'LinkedList', 'HashSet', 'Vector'], 'answer': 'HashSet'},
	{'id': 7, 'topic': 'Java methods', 'text': 'What is method overloading?', 'code': '', 'options': ['Same method with different parameters', 'Same method in different classes only', 'Changing return type only', 'Removing a method'], 'answer': 'Same method with different parameters'},
	{'id': 8, 'topic': 'Java inheritance', 'text': 'Which keyword is used to prevent inheritance?', 'code': '', 'options': ['static', 'private', 'final', 'protected'], 'answer': 'final'},
	{'id': 9, 'topic': 'Java exceptions', 'text': 'Which exception occurs when dividing an integer by zero?', 'code': '', 'options': ['NullPointerException', 'ArithmeticException', 'IOException', 'NumberFormatException'], 'answer': 'ArithmeticException'},
	{'id': 10, 'topic': 'Java threads', 'text': "Which interface is commonly used to define a thread's task?", 'code': '', 'options': ['Runnable', 'Serializable', 'Comparable', 'Cloneable'], 'answer': 'Runnable'},
	{'id': 11, 'topic': 'Java operators', 'text': 'What is the output?', 'code': 'int x = 5;\nSystem.out.println(x++ + ++x);', 'options': ['10', '11', '12', '13'], 'answer': '12'},
	{'id': 12, 'topic': 'Java strings', 'text': 'What is the output?', 'code': 'String s1 = "Java";\nString s2 = new String("Java");\n\nSystem.out.println(s1 == s2);', 'options': ['true', 'false', 'Java', 'Error'], 'answer': 'false'},
	{'id': 13, 'topic': 'Java methods', 'text': 'Which method cannot be overridden?', 'code': '', 'options': ['public', 'protected', 'static', 'abstract'], 'answer': 'static'},
	{'id': 14, 'topic': 'Java fields', 'text': 'What is the output?', 'code': 'class A {\n    int x = 10;\n}\n\nclass B extends A {\n    int x = 20;\n}\n\nA obj = new B();\nSystem.out.println(obj.x);', 'options': ['10', '20', '30', 'Error'], 'answer': '10'},
	{'id': 15, 'topic': 'Java ternary operator', 'text': 'What is the output?', 'code': 'int a = 10;\nint b = 20;\n\nSystem.out.println(a > b ? a : b);', 'options': ['10', '20', 'true', 'false'], 'answer': '20'},
	{'id': 16, 'topic': 'Java collections', 'text': 'Which collection provides average O(1) lookup by key?', 'code': '', 'options': ['ArrayList', 'LinkedList', 'HashMap', 'TreeSet'], 'answer': 'HashMap'},
	{'id': 17, 'topic': 'Java final variables', 'text': 'What happens?', 'code': 'final int x = 10;\nx++;', 'options': ['x becomes 11', 'Runtime error', 'Compilation error', 'x remains 10'], 'answer': 'Compilation error'},
	{'id': 18, 'topic': 'Java exceptions', 'text': 'What is the output?', 'code': 'try {\n    System.out.println(10 / 0);\n}\ncatch (Exception e) {\n    System.out.println("Exception");\n}\nfinally {\n    System.out.println("Done");\n}', 'options': ['Exception', 'Done', 'Exception Done', 'Compilation error'], 'answer': 'Exception Done'},
	{'id': 19, 'topic': 'Java exceptions', 'text': 'Which statement about finally is correct?', 'code': '', 'options': ['It executes only when exception occurs', 'It normally executes whether exception occurs or not', 'It never executes after return', 'It can replace catch in every situation'], 'answer': 'It normally executes whether exception occurs or not'},
	{'id': 20, 'topic': 'Java static fields', 'text': 'What is the output?', 'code': 'class Test {\n    static int x = 10;\n\n    public static void main(String[] args) {\n        Test t1 = new Test();\n        Test t2 = new Test();\n\n        t1.x = 50;\n\n        System.out.println(t2.x);\n    }\n}', 'options': ['10', '50', '0', 'Error'], 'answer': '50'},
	{'id': 21, 'topic': 'Java strings', 'text': 'What is the output?', 'code': 'String s = "Hello";\ns = s.concat(" World");\n\nSystem.out.println(s);', 'options': ['Hello', 'World', 'Hello World', 'Error'], 'answer': 'Hello World'},
	{'id': 22, 'topic': 'Java exceptions', 'text': 'Which exception occurs when accessing an invalid array index?', 'code': '', 'options': ['NullPointerException', 'ArrayIndexOutOfBoundsException', 'ArithmeticException', 'IndexException'], 'answer': 'ArrayIndexOutOfBoundsException'},
	{'id': 23, 'topic': 'Java arrays', 'text': 'What is the output?', 'code': 'int[] a = {1, 2, 3};\n\nfor (int i : a) {\n    System.out.print(i * 2 + " ");\n}', 'options': ['1 2 3', '2 4 6', '0 2 4', '1 4 9'], 'answer': '2 4 6'},
	{'id': 24, 'topic': 'Java abstract classes', 'text': 'Which statement is TRUE about an abstract class?', 'code': '', 'options': ['It can always be instantiated', 'It cannot contain constructors', 'It can contain both abstract and concrete methods', 'It cannot contain variables'], 'answer': 'It can contain both abstract and concrete methods'},
	{'id': 25, 'topic': 'Java polymorphism', 'text': 'What is the output?', 'code': 'class A {\n    void show() {\n        System.out.println("A");\n    }\n}\n\nclass B extends A {\n    @Override\n    void show() {\n        System.out.println("B");\n    }\n}\n\nA obj = new B();\nobj.show();', 'options': ['A', 'B', 'A B', 'Error'], 'answer': 'B'},
	{'id': 26, 'topic': 'Java wrapper classes', 'text': 'What is the output?', 'code': 'Integer a = 100;\nInteger b = 100;\n\nSystem.out.println(a == b);', 'options': ['true', 'false', 'Error', 'null'], 'answer': 'true'},
	{'id': 27, 'topic': 'Java wrapper classes', 'text': 'What is the output?', 'code': 'Integer a = 200;\nInteger b = 200;\n\nSystem.out.println(a == b);', 'options': ['true', 'false', '200', 'Error'], 'answer': 'false'},
	{'id': 28, 'topic': 'Java generics', 'text': 'Which statement about Java Generics is correct?', 'code': '', 'options': ['Generics work directly with primitive types like int', 'Generics provide compile-time type safety', 'Generics exist only for arrays', 'Generics cannot be used with collections'], 'answer': 'Generics provide compile-time type safety'},
	{'id': 29, 'topic': 'Java collections', 'text': 'What can happen when modifying an ArrayList while using its enhanced for loop?', 'code': 'for (String s : list) {\n    list.remove(s);\n}', 'options': ['Always works correctly', 'ConcurrentModificationException may occur', 'Compilation error', 'List automatically becomes empty'], 'answer': 'ConcurrentModificationException may occur'},
	{'id': 30, 'topic': 'Java threads', 'text': 'Which statement is TRUE about Java threads?', 'code': '', 'options': ['start() directly executes the method on the current thread', 'run() creates a new thread automatically', 'start() begins a new thread and eventually invokes run()', 'A thread can be started multiple times'], 'answer': 'start() begins a new thread and eventually invokes run()'},
]

MYSQL_QUESTIONS = [
	{'id': 1, 'topic': 'SQL basics', 'text': 'Which command is used to retrieve data from a table?', 'code': '', 'options': ['GET', 'SELECT', 'FETCH', 'OPEN'], 'answer': 'SELECT'},
	{'id': 2, 'topic': 'Filtering rows', 'text': 'Which clause is used to filter rows?', 'code': '', 'options': ['SORT BY', 'ORDER BY', 'WHERE', 'GROUP BY'], 'answer': 'WHERE'},
	{'id': 3, 'topic': 'Insert data', 'text': 'Which command is used to add a new row?', 'code': '', 'options': ['INSERT INTO', 'ADD ROW', 'CREATE ROW', 'APPEND'], 'answer': 'INSERT INTO'},
	{'id': 4, 'topic': 'Unique results', 'text': 'Which keyword removes duplicate results?', 'code': '', 'options': ['UNIQUE', 'DISTINCT', 'REMOVE', 'FILTER'], 'answer': 'DISTINCT'},
	{'id': 5, 'topic': 'Sorting results', 'text': 'Which clause sorts query results?', 'code': '', 'options': ['SORT BY', 'ORDER BY', 'GROUP BY', 'ARRANGE BY'], 'answer': 'ORDER BY'},
	{'id': 6, 'topic': 'Aggregate functions', 'text': 'Which function returns the number of rows?', 'code': '', 'options': ['SUM()', 'COUNT()', 'TOTAL()', 'NUMBER()'], 'answer': 'COUNT()'},
	{'id': 7, 'topic': 'Update data', 'text': 'Which command modifies existing data?', 'code': '', 'options': ['UPDATE', 'MODIFY', 'CHANGE', 'ALTER'], 'answer': 'UPDATE'},
	{'id': 8, 'topic': 'Database keys', 'text': 'Which key uniquely identifies each row?', 'code': '', 'options': ['Foreign Key', 'Candidate Key', 'Primary Key', 'Alternate Key'], 'answer': 'Primary Key'},
	{'id': 9, 'topic': 'Pattern matching', 'text': 'Which operator is used for pattern matching?', 'code': '', 'options': ['MATCH', 'LIKE', 'PATTERN', 'SEARCH'], 'answer': 'LIKE'},
	{'id': 10, 'topic': 'Table management', 'text': 'Which command removes a table completely?', 'code': '', 'options': ['DELETE TABLE', 'REMOVE TABLE', 'DROP TABLE', 'CLEAR TABLE'], 'answer': 'DROP TABLE'},
	{'id': 11, 'topic': 'NULL values', 'text': 'What will be the output?', 'code': 'SELECT 10 + NULL;', 'options': ['10', '0', 'NULL', 'Error'], 'answer': 'NULL'},
	{'id': 12, 'topic': 'Subqueries', 'text': 'What does this query return?', 'code': 'SELECT name, salary\nFROM employees\nWHERE salary > (\n    SELECT AVG(salary)\n    FROM employees\n);', 'options': ['Employees earning below average', 'Employees earning exactly average', 'Employees earning above average', 'Highest-paid employee only'], 'answer': 'Employees earning above average'},
	{'id': 13, 'topic': 'GROUP BY and HAVING', 'text': 'What is the result?', 'code': 'SELECT department_id, COUNT(*)\nFROM employees\nGROUP BY department_id\nHAVING COUNT(*) > 5;', 'options': ['Departments having more than 5 employees', 'Employees having salary > 5', 'First 5 departments', 'All departments'], 'answer': 'Departments having more than 5 employees'},
	{'id': 14, 'topic': 'INNER JOIN', 'text': 'What does this query return?', 'code': 'SELECT e.name, d.department_name\nFROM employees e\nINNER JOIN departments d\nON e.department_id = d.id;', 'options': ['All employees, even without departments', 'Only employees with matching departments', 'All departments', 'Duplicate employees'], 'answer': 'Only employees with matching departments'},
	{'id': 15, 'topic': 'LEFT JOIN', 'text': 'What will this query return?', 'code': 'SELECT e.name\nFROM employees e\nLEFT JOIN departments d\nON e.department_id = d.id\nWHERE d.id IS NULL;', 'options': ['Employees with a department', 'Employees without a matching department', 'All departments', 'Employees with duplicate departments'], 'answer': 'Employees without a matching department'},
	{'id': 16, 'topic': 'Aggregate functions', 'text': 'What is the output?', 'code': 'SELECT MAX(salary)\nFROM employees\nWHERE salary < (\n    SELECT MAX(salary)\n    FROM employees\n);', 'options': ['30000', '40000', '50000', '120000'], 'answer': '40000'},
	{'id': 17, 'topic': 'Subqueries', 'text': 'Which employees are returned?', 'code': 'SELECT name\nFROM employees\nWHERE salary IN (\n    SELECT salary\n    FROM employees\n    WHERE department_id = 10\n);', 'options': ['Employees whose salary matches a salary in department 10', 'Only department 10 employees', 'Employees with highest salary', 'All employees'], 'answer': 'Employees whose salary matches a salary in department 10'},
	{'id': 18, 'topic': 'EXISTS', 'text': 'What does EXISTS check?', 'code': 'SELECT name\nFROM employees e\nWHERE EXISTS (\n    SELECT 1\n    FROM departments d\n    WHERE d.id = e.department_id\n);', 'options': ['Whether the employee has a matching department', 'Whether salary is NULL', 'Whether employee name exists', 'Whether duplicate rows exist'], 'answer': 'Whether the employee has a matching department'},
	{'id': 19, 'topic': 'GROUP BY', 'text': 'What is the result?', 'code': 'SELECT department_id, AVG(salary)\nFROM employees\nGROUP BY department_id;', 'options': ['Average salary of all employees', 'Average salary for each department', 'Maximum salary per department', 'Number of employees per department'], 'answer': 'Average salary for each department'},
	{'id': 20, 'topic': 'ORDER BY and LIMIT', 'text': 'What does this query find?', 'code': 'SELECT name, salary\nFROM employees\nORDER BY salary DESC\nLIMIT 3;', 'options': ['Lowest 3 salaries', 'Highest 3 salaries', 'All salaries', 'Third salary only'], 'answer': 'Highest 3 salaries'},
	{'id': 21, 'topic': 'Ranking subqueries', 'text': 'What does this query find?', 'code': 'SELECT name, salary\nFROM employees e1\nWHERE 2 = (\n    SELECT COUNT(DISTINCT salary)\n    FROM employees e2\n    WHERE e2.salary > e1.salary\n);', 'options': ['Highest salary', 'Second-highest salary', 'Third-highest salary', 'Lowest salary'], 'answer': 'Third-highest salary'},
	{'id': 22, 'topic': 'GROUP BY', 'text': 'What does this query do?', 'code': 'SELECT department_id, MAX(salary)\nFROM employees\nGROUP BY department_id;', 'options': ['Finds the highest salary in each department', 'Finds the highest department ID', 'Finds the average salary', 'Finds the total salary'], 'answer': 'Finds the highest salary in each department'},
	{'id': 23, 'topic': 'Highest salary per group', 'text': 'What does this query return?', 'code': 'SELECT e.name, e.salary, d.department_name\nFROM employees e\nJOIN departments d\nON e.department_id = d.id\nWHERE e.salary = (\n    SELECT MAX(e2.salary)\n    FROM employees e2\n    WHERE e2.department_id = e.department_id\n);', 'options': ['Lowest-paid employee in each department', 'Highest-paid employee(s) in each department', 'Highest-paid employee overall only', 'All employees'], 'answer': 'Highest-paid employee(s) in each department'},
	{'id': 24, 'topic': 'COUNT', 'text': 'What will COUNT(*) return?', 'code': 'SELECT COUNT(*)\nFROM employees;', 'options': ['Number of non-NULL names', 'Number of rows', 'Number of unique employees', 'Number of columns'], 'answer': 'Number of rows'},
	{'id': 25, 'topic': 'COUNT and NULL', 'text': 'What will this return?', 'code': 'SELECT COUNT(salary)\nFROM employees;', 'options': ['Number of all rows', 'Number of rows where salary is NOT NULL', 'Number of NULL salaries', 'Number of unique salaries'], 'answer': 'Number of rows where salary is NOT NULL'},
	{'id': 26, 'topic': 'Window functions', 'text': 'What does ROW_NUMBER() do?', 'code': 'SELECT\n    name,\n    salary,\n    ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn\nFROM employees;', 'options': ['Gives each employee a sequential ranking', 'Removes duplicate salaries', 'Calculates average salary', 'Groups employees'], 'answer': 'Gives each employee a sequential ranking'},
	{'id': 27, 'topic': 'Window functions', 'text': 'What does this query find?', 'code': 'SELECT *\nFROM (\n    SELECT\n        name,\n        salary,\n        DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk\n    FROM employees\n) x\nWHERE rnk = 2;', 'options': ['Highest-paid employees', 'Second-highest salary group', 'Third-highest salary group', 'Lowest-paid employees'], 'answer': 'Second-highest salary group'},
	{'id': 28, 'topic': 'CTE', 'text': 'What does this CTE query do?', 'code': 'WITH high_salary AS (\n    SELECT *\n    FROM employees\n    WHERE salary > 50000\n)\nSELECT name, salary\nFROM high_salary;', 'options': ['Creates a permanent table', 'Creates a temporary named result for the query', 'Deletes employees', 'Creates an index'], 'answer': 'Creates a temporary named result for the query'},
	{'id': 29, 'topic': 'GROUP BY and SUM', 'text': 'What is the result of this query?', 'code': 'SELECT department_id, SUM(salary) AS total_salary\nFROM employees\nGROUP BY department_id\nORDER BY total_salary DESC;', 'options': ['Departments sorted by total salary from highest to lowest', 'Employees sorted by salary', 'Departments sorted alphabetically', 'Only the highest-paid employee'], 'answer': 'Departments sorted by total salary from highest to lowest'},
	{'id': 30, 'topic': 'Correlated subqueries', 'text': 'What does this query find?', 'code': 'SELECT e.name, e.salary\nFROM employees e\nWHERE e.salary > (\n    SELECT AVG(e2.salary)\n    FROM employees e2\n    WHERE e2.department_id = e.department_id\n);', 'options': ['Employees earning above the company average', "Employees earning above their department's average", 'Highest-paid employee in each department', 'Employees earning below department average'], 'answer': "Employees earning above their department's average"},
]

WEB_DESIGN_QUESTIONS = [
	{'id': 1, 'topic': 'HTML document structure', 'text': 'What is the purpose of <!DOCTYPE html>?', 'code': '', 'options': ['Creates HTML document', 'Specifies HTML version/rendering mode', 'Adds CSS', 'Adds JavaScript'], 'answer': 'Specifies HTML version/rendering mode'},
	{'id': 2, 'topic': 'Semantic HTML', 'text': 'Which HTML element is semantically best for main navigation?', 'code': '', 'options': ['<div>', '<section>', '<nav>', '<menu>'], 'answer': '<nav>'},
	{'id': 3, 'topic': 'Script loading', 'text': 'What happens when defer is used?', 'code': '<script src="app.js" defer></script>', 'options': ['Script executes immediately and blocks HTML parsing', 'Script downloads during parsing and executes after parsing', 'Script never executes', 'Script executes before HTML parsing'], 'answer': 'Script downloads during parsing and executes after parsing'},
	{'id': 4, 'topic': 'Web accessibility', 'text': 'Which attribute improves accessibility by describing an image?', 'code': '<img src="logo.png" alt="Company Logo">', 'options': ['title', 'description', 'alt', 'label'], 'answer': 'alt'},
	{'id': 5, 'topic': 'HTML forms', 'text': 'Which HTML element is normally used to associate a text label with a form input?', 'code': '', 'options': ['<caption>', '<label>', '<legend>', '<span>'], 'answer': '<label>'},
	{'id': 6, 'topic': 'CSS specificity', 'text': 'Which selector has the highest specificity?', 'code': 'p { color: red; }\n.text { color: blue; }\n#demo { color: green; }\n\n<p id="demo" class="text">Hello</p>', 'options': ['p', '.text', '#demo', 'All equal'], 'answer': '#demo'},
	{'id': 7, 'topic': 'CSS box model', 'text': 'What is the total width?', 'code': '.box {\n    width: 200px;\n    padding: 20px;\n    box-sizing: content-box;\n}', 'options': ['200px', '220px', '240px', '160px'], 'answer': '240px'},
	{'id': 8, 'topic': 'CSS Grid', 'text': 'What does this create?', 'code': '.container {\n    display: grid;\n    grid-template-columns: repeat(3, 1fr);\n}', 'options': ['3 equal columns', '3 equal rows', '1 column', '2 columns'], 'answer': '3 equal columns'},
	{'id': 9, 'topic': 'CSS Flexbox', 'text': 'What happens? Inside a horizontal flex container, this generally:', 'code': '.child {\n    margin-left: auto;\n}', 'options': ['Pushes the child toward the left', 'Pushes the child toward the right', 'Hides the child', 'Centers the child'], 'answer': 'Pushes the child toward the right'},
	{'id': 10, 'topic': 'CSS stacking', 'text': 'Which property controls the order of overlapping positioned elements?', 'code': '', 'options': ['position', 'layer', 'z-index', 'stack'], 'answer': 'z-index'},
	{'id': 11, 'topic': 'CSS Grid units', 'text': 'What does 1fr mean in CSS Grid?', 'code': '', 'options': ['1 fixed pixel', 'One fraction of the available grid space', 'One font size', 'One row'], 'answer': 'One fraction of the available grid space'},
	{'id': 12, 'topic': 'CSS positioning', 'text': 'What does position: fixed generally position an element relative to?', 'code': '', 'options': ['Normal document flow', 'Nearest flex container', 'Viewport', 'Previous sibling'], 'answer': 'Viewport'},
	{'id': 13, 'topic': 'JavaScript coercion', 'text': 'What is the output?', 'code': 'console.log(1 + "2" + 3);\nconsole.log(1 + 2 + "3");', 'options': ['6\n6', '123\n33', '33\n123', '123\n123'], 'answer': '123\n33'},
	{'id': 14, 'topic': 'JavaScript operators', 'text': 'What is the output?', 'code': 'console.log("5" - 2);\nconsole.log("5" + 2);', 'options': ['3\n7', '3\n52', '52\n7', '52\n52'], 'answer': '3\n52'},
	{'id': 15, 'topic': 'JavaScript equality', 'text': 'What is the output?', 'code': 'console.log([] == false);\nconsole.log([] === false);', 'options': ['true true', 'false false', 'true false', 'false true'], 'answer': 'true false'},
	{'id': 16, 'topic': 'JavaScript types', 'text': 'What is the output?', 'code': 'console.log(typeof null);\nconsole.log(typeof NaN);', 'options': ['null\nNaN', 'object\nnumber', 'undefined\nnumber', 'object\nNaN'], 'answer': 'object\nnumber'},
	{'id': 17, 'topic': 'JavaScript scope', 'text': 'What is the output?', 'code': 'let x = 10;\n\n{\n    let x = 20;\n}\n\nconsole.log(x);', 'options': ['10', '20', 'undefined', 'Error'], 'answer': '10'},
	{'id': 18, 'topic': 'JavaScript scope', 'text': 'What is the output?', 'code': 'var x = 10;\n\n{\n    var x = 20;\n}\n\nconsole.log(x);', 'options': ['10', '20', 'undefined', 'Error'], 'answer': '20'},
	{'id': 19, 'topic': 'JavaScript arrays', 'text': 'What is the output?', 'code': 'const arr = [1, 2, 3];\n\narr.push(4);\n\nconsole.log(arr);', 'options': ['Error', '[1, 2, 3]', '[1, 2, 3, 4]', '4'], 'answer': '[1, 2, 3, 4]'},
	{'id': 20, 'topic': 'JavaScript arrays', 'text': 'What is the output?', 'code': 'const nums = [1, 2, 3, 4];\n\nconst result = nums.filter(x => x % 2 === 0);\n\nconsole.log(result);', 'options': ['[1, 3]', '[2, 4]', '[0, 2, 4]', 'true'], 'answer': '[2, 4]'},
	{'id': 21, 'topic': 'JavaScript NaN', 'text': 'What is the output?', 'code': 'console.log(NaN === NaN);\nconsole.log(Number.isNaN(NaN));', 'options': ['true true', 'false false', 'false true', 'true false'], 'answer': 'false true'},
	{'id': 22, 'topic': 'JavaScript event loop', 'text': 'What is the output?', 'code': 'setTimeout(() => {\n    console.log("A");\n}, 0);\n\nPromise.resolve().then(() => {\n    console.log("B");\n});\n\nconsole.log("C");', 'options': ['A\nB\nC', 'C\nA\nB', 'C\nB\nA', 'B\nC\nA'], 'answer': 'C\nB\nA'},
	{'id': 23, 'topic': 'JavaScript event loop', 'text': 'What is the output?', 'code': 'console.log(1);\n\nsetTimeout(() => {\n    console.log(2);\n}, 0);\n\nPromise.resolve().then(() => {\n    console.log(3);\n});\n\nconsole.log(4);', 'options': ['1\n2\n3\n4', '1\n4\n2\n3', '1\n4\n3\n2', '3\n1\n4\n2'], 'answer': '1\n4\n3\n2'},
	{'id': 24, 'topic': 'JavaScript arrays', 'text': 'What does map() return?', 'code': 'const a = [1, 2, 3];\n\nconst b = a.map(x => x * 2);', 'options': ['Original array modified automatically', 'A new array', 'A string', 'A boolean'], 'answer': 'A new array'},
	{'id': 25, 'topic': 'JavaScript hoisting', 'text': 'What is the output?', 'code': 'function test() {\n    console.log(x);\n    var x = 10;\n}\n\ntest();', 'options': ['10', 'undefined', 'null', 'ReferenceError'], 'answer': 'undefined'},
	{'id': 26, 'topic': 'jQuery events', 'text': 'What does this do?', 'code': '$("#btn").click(function() {\n    $("#demo").hide();\n});', 'options': ['Hides the button', 'Hides #demo when the button is clicked', 'Deletes #demo', 'Reloads the page'], 'answer': 'Hides #demo when the button is clicked'},
	{'id': 27, 'topic': 'jQuery content', 'text': 'What is the difference?', 'code': '$("#demo").html("<b>Hello</b>");\n$("#demo").text("<b>Hello</b>");', 'options': ['Both display bold text', 'html() interprets HTML; text() treats it as text', 'Both display plain text', 'Both produce errors'], 'answer': 'html() interprets HTML; text() treats it as text'},
	{'id': 28, 'topic': 'jQuery iteration', 'text': 'What does this code do?', 'code': '$("p").each(function(index) {\n    console.log(index);\n});', 'options': ['Processes only the first <p>', 'Iterates over each <p> element', 'Deletes all <p> elements', 'Creates new <p> elements'], 'answer': 'Iterates over each <p> element'},
	{'id': 29, 'topic': 'jQuery events', 'text': 'What does this demonstrate?', 'code': '$("#list").on("click", "li", function() {\n    console.log($(this).text());\n});', 'options': ['Event delegation', 'AJAX', 'Animation', 'Form validation'], 'answer': 'Event delegation'},
	{'id': 30, 'topic': 'jQuery content', 'text': 'What happens?', 'code': '$("#btn").click(function() {\n    $("#result").html("<b>Success</b>");\n});', 'options': ['#result displays literal <b>Success</b>', '#result displays Success in bold', '#btn becomes bold', 'Page reloads'], 'answer': '#result displays Success in bold'},
]

EXAMS = [
	{'slug': 'python', 'name': 'Python', 'count': 24, 'description': 'Core Python · problem solving', 'series': 'Python Fundamentals · 12 tests', 'tone': 'blue'},
	{'slug': 'java', 'name': 'Java', 'count': 18, 'description': 'Java 21 · OOP · collections', 'series': 'Java Developer Track · 8 tests', 'tone': 'green'},
	{'slug': 'mysql', 'name': 'MySQL', 'count': 16, 'description': 'SQL queries · database design', 'series': 'SQL Interview Series · 6 tests', 'tone': 'red'},
	{'slug': 'web-design', 'name': 'Web Design', 'count': 21, 'description': 'HTML · CSS · responsive UI', 'series': 'Frontend Starter Series · 10 tests', 'tone': 'teal'},
]


def home(request):
	return redirect('login')


def login(request):
	if request.session.get('member_logged_in'):
		return redirect('exam_list')
	message = None
	if request.method == 'POST':
		if request.POST.get('username') == 'pumo' and request.POST.get('password') == '1234':
			request.session['member_logged_in'] = True
			request.session['student_name'] = request.POST.get('student_name', '').strip()
			request.session['course'] = request.POST.get('course', '').strip()
			request.session['staff_name'] = request.POST.get('staff_name', '').strip()
			return redirect('exam_list')
		message = 'Username or password is incorrect.'
	return render(request, 'member/login.html', {'message': message})


def exam_list(request):
	if not request.session.get('member_logged_in'):
		return redirect('login')
	student = {
		'name': request.session.get('student_name', 'Student'),
		'course': request.session.get('course', 'Course not set'),
		'staff': request.session.get('staff_name', 'Staff not set'),
	}
	return render(request, 'member/exams.html', {'exams': EXAMS, 'student': student})


def logout(request):
	request.session.flush()
	return redirect('login')


def save_result(request, result):
	file_exists = RESULTS_FILE.exists()
	with RESULTS_FILE.open('a', newline='', encoding='utf-8') as results_file:
		writer = csv.DictWriter(results_file, fieldnames=['Student Name', 'Course', 'Staff Name', 'Mark', 'Time Taken'])
		if not file_exists:
			writer.writeheader()
		writer.writerow({
			'Student Name': request.session.get('student_name', 'Student'),
			'Course': request.session.get('course', 'Course not set'),
			'Staff Name': request.session.get('staff_name', 'Staff not set'),
			'Mark': f'{result["correct"]}/{result["total"]}',
			'Time Taken': result.get('time_taken', '0:00'),
		})


def mock_test(request, exam_slug='practice'):
	if not request.session.get('member_logged_in'):
		return redirect('login')
	questions = PYTHON_QUESTIONS if exam_slug == 'python' else JAVA_QUESTIONS if exam_slug == 'java' else MYSQL_QUESTIONS if exam_slug == 'mysql' else WEB_DESIGN_QUESTIONS if exam_slug == 'web-design' else QUESTIONS
	display_questions = [dict(question) for question in questions]
	result = None
	if request.method == 'POST':
		for question in display_questions:
			question['user_answer'] = request.POST.get(f'question-{question["id"]}', 'Not answered')
		correct = sum(
			request.POST.get(f'question-{question["id"]}') == question['answer']
			for question in questions
		)
		result = {
			'correct': correct,
			'total': len(questions),
			'percentage': round(correct / len(questions) * 100),
			'time_taken': request.POST.get('time_taken', '0:00'),
			'time_remaining': request.POST.get('time_remaining', '45:00'),
		}
		save_result(request, result)
	return render(request, 'member/mock_test.html', {'questions': display_questions, 'result': result, 'exam_name': 'Web Design' if exam_slug == 'web-design' else exam_slug.title() if exam_slug in ('python', 'java', 'mysql') else 'Practice'})
