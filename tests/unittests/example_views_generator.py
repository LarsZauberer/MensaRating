from django.test import TestCase, Client
from django.urls import reverse
from Generator.models import Exercise, ExerciseData
from django.contrib.auth.models import User, Group

class TestViewsUsers(TestCase):
    def setUp(self):
        with open("tests/Addition.encrypt", "r") as f:
            self.code = f.read()
        self.admin = User.objects.create_superuser(username='admin', password='admin')
        self.user = User.objects.create_user(username='user', password='user')
        self.group = Group.objects.create(name='Test')
        self.group.user_set.add(self.user)
        self.group.save()
    
    def test_view_overview(self):
        response = self.client.get(reverse('overview'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Overview.html')
    
    def test_view_exercise_404(self):
        response = self.client.get(reverse('exercise', args=['0']))
        self.assertEqual(response.status_code, 404)

    def test_view_exercise_200(self):
        task = Exercise.objects.create(name='Test', description='Test', gradingAmount=1, public=True, code=self.code)
        task.save()
        response = self.client.get(reverse('exercise', args=[str(task.pk)]))
        self.assertEqual(response.status_code, 200)

    def test_view_exercise_no_permission(self):
        task = Exercise.objects.create(name='Test', description='Test', gradingAmount=1, public=False, code=self.code)
        task.save()
        # Test redirect to overview page
        response = self.client.get(reverse('exercise', args=[str(task.pk)]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('overview'))
    
    def test_view_exercise_permission(self):
        self.client.login(username='admin', password='admin')
        task = Exercise.objects.create(name='Test', description='Test', gradingAmount=1, public=False, code=self.code)
        task.save()
        response = self.client.get(reverse('exercise', args=[str(task.pk)]))
        self.assertEqual(response.status_code, 200)

    def test_view_exercise_permission_group(self):
        self.client.login(username='user', password='user')
        task = Exercise.objects.create(name='Test', description='Test', gradingAmount=1, public=False, code=self.code, permissionGroup=self.group)
        task.save()
        response = self.client.get(reverse('exercise', args=[str(task.pk)]))
        self.assertEqual(response.status_code, 200)
    
    def test_view_diffChanger_302(self):
        response = self.client.get(reverse('diffChanger'))
        self.assertEqual(response.status_code, 302)

    def test_view_diffChanger_up(self):
        self.client.login(username='admin', password='admin')
        task = Exercise.objects.create(name='Test', description='Test', gradingAmount=1, public=True, code=self.code)
        exerciseData = ExerciseData.objects.create(ex=task, user=self.admin)
        response = self.client.post(reverse('diffChanger'), {'amount': 1, "ex": 1})
        self.assertEqual(response.status_code, 200)
        exerciseData.refresh_from_db()
        self.assertEqual(exerciseData.difficultyLevel, 2)
    
    def test_view_diffChanger_down(self):
        self.client.login(username='admin', password='admin')
        task = Exercise.objects.create(name='Test', description='Test', gradingAmount=1, public=True, code=self.code)
        exerciseData = ExerciseData.objects.create(ex=task, user=self.admin, difficultyLevel=2)
        response = self.client.post(reverse('diffChanger'), {'amount': -1, "ex": 1})
        self.assertEqual(response.status_code, 200)
        exerciseData.refresh_from_db()
        self.assertEqual(exerciseData.difficultyLevel, 1)
    
    def test_view_diffChanger_down_over(self):
        self.client.login(username='admin', password='admin')
        task = Exercise.objects.create(name='Test', description='Test', gradingAmount=1, public=True, code=self.code)
        exerciseData = ExerciseData.objects.create(ex=task, user=self.admin, difficultyLevel=0.5)
        response = self.client.post(reverse('diffChanger'), {'amount': -1, "ex": 1})
        self.assertEqual(response.status_code, 200)
        exerciseData.refresh_from_db()
        self.assertEqual(exerciseData.difficultyLevel, 0.1)
