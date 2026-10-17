import csv

from django.test import TestCase

from .views import JAVA_QUESTIONS, MYSQL_QUESTIONS, PYTHON_QUESTIONS, QUESTIONS, RESULTS_FILE, WEB_DESIGN_QUESTIONS


class MockTestViewTests(TestCase):
	@classmethod
	def tearDownClass(cls):
		if RESULTS_FILE.exists():
			RESULTS_FILE.unlink()
		super().tearDownClass()

	def test_root_opens_login_url(self):
		response = self.client.get('/')
		self.assertRedirects(response, '/login/')

	def test_login_page_loads(self):
		response = self.client.get('/login/')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Welcome back.')

	def test_login_opens_exam_list(self):
		response = self.client.post('/login/', {
			'username': 'pumo', 'password': '1234', 'student_name': 'Arun',
			'course': 'Python', 'staff_name': 'Kumar',
		})
		self.assertRedirects(response, '/exams/')
		exams_response = self.client.get('/exams/')
		self.assertContains(exams_response, 'Arun')
		self.assertContains(exams_response, 'Python')
		self.assertContains(exams_response, 'Kumar')

	def test_quiz_scores_submitted_answers(self):
		self.client.post('/login/', {
			'username': 'pumo', 'password': '1234', 'student_name': 'Arun',
			'course': 'Python', 'staff_name': 'Kumar',
		})
		answers = {f'question-{question["id"]}': question['answer'] for question in QUESTIONS}
		answers['time_taken'] = '02:15'
		answers['time_remaining'] = '43:06'
		response = self.client.post('/test/', answers)
		self.assertContains(response, '100')
		self.assertContains(response, '4 of 4 answers correct')
		self.assertContains(response, 'View answer')
		self.assertContains(response, 'Your answer')
		self.assertContains(response, 'Correct answer')
		self.assertContains(response, '02:15')
		self.assertContains(response, 'quiz-submitted')
		self.assertContains(response, '>43:06</div>')
		with RESULTS_FILE.open(newline='', encoding='utf-8') as results_file:
			row = next(row for row in csv.DictReader(results_file) if row['Student Name'] == 'Arun')
		self.assertEqual(row['Student Name'], 'Arun')
		self.assertEqual(row['Course'], 'Python')
		self.assertEqual(row['Staff Name'], 'Kumar')
		self.assertEqual(row['Mark'], '4/4')

	def test_python_explore_shows_python_questions(self):
		self.client.post('/login/', {'username': 'pumo', 'password': '1234'})
		response = self.client.get('/test/python/')
		self.assertContains(response, 'x = [1, 2, 3]')
		self.assertContains(response, 'print(bool([]), bool([0]))')
		self.assertContains(response, 'x.pop(1)')
		self.assertContains(response, '30</strong><span>questions')
		answers = {f'question-{question["id"]}': question['answer'] for question in PYTHON_QUESTIONS}
		result = self.client.post('/test/python/', answers)
		self.assertContains(result, '100')
		self.assertContains(result, '30 of 30 answers correct')

	def test_java_explore_shows_java_questions(self):
		self.client.post('/login/', {'username': 'pumo', 'password': '1234'})
		response = self.client.get('/test/java/')
		self.assertContains(response, 'Which keyword is used to create an object in Java?')
		self.assertContains(response, "Which interface is commonly used to define a thread&#x27;s task?")
		answers = {f'question-{question["id"]}': question['answer'] for question in JAVA_QUESTIONS}
		result = self.client.post('/test/java/', answers)
		self.assertContains(result, '30 of 30 answers correct')

	def test_mysql_explore_shows_mysql_questions(self):
		self.client.post('/login/', {'username': 'pumo', 'password': '1234'})
		response = self.client.get('/test/mysql/')
		self.assertContains(response, 'Which command is used to retrieve data from a table?')
		self.assertContains(response, 'Which command removes a table completely?')
		self.assertContains(response, 'What does this CTE query do?')
		answers = {f'question-{question["id"]}': question['answer'] for question in MYSQL_QUESTIONS}
		result = self.client.post('/test/mysql/', answers)
		self.assertContains(result, '30 of 30 answers correct')

	def test_web_design_explore_shows_questions(self):
		self.client.post('/login/', {'username': 'pumo', 'password': '1234'})
		response = self.client.get('/test/web-design/')
		self.assertContains(response, 'What is the purpose of &lt;!DOCTYPE html&gt;?')
		self.assertContains(response, 'Which HTML element is semantically best for main navigation?')
		self.assertContains(response, 'Which selector has the highest specificity?')
		self.assertContains(response, 'What does position: fixed generally position an element relative to?')
		self.assertContains(response, 'console.log(1 + &quot;2&quot; + 3);')
		self.assertContains(response, 'What does map() return?')
		self.assertContains(response, 'What does this demonstrate?')
		answers = {f'question-{question["id"]}': question['answer'] for question in WEB_DESIGN_QUESTIONS}
		result = self.client.post('/test/web-design/', answers)
		self.assertContains(result, '30 of 30 answers correct')
