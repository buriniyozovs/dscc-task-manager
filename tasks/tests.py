from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Task, Category, Comment


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Description',
            user=self.user
        )

    def test_task_creation(self):
        task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            deadline=timezone.now() + timedelta(days=7),
            priority=3,
            user=self.user
        )
        task.categories.add(self.category)
        
        self.assertEqual(task.title, 'Test Task')
        self.assertFalse(task.is_completed)
        self.assertEqual(task.priority, 3)
        self.assertEqual(task.user, self.user)
        self.assertIn(self.category, task.categories.all())

    def test_task_str(self):
        task = Task.objects.create(
            title='My Task',
            description='Description',
            deadline=timezone.now() + timedelta(days=1),
            priority=1,
            user=self.user
        )
        self.assertEqual(str(task), 'My Task')

    def test_task_default_priority(self):
        task = Task.objects.create(
            title='Default Priority Task',
            description='Description',
            deadline=timezone.now() + timedelta(days=1),
            user=self.user
        )
        self.assertEqual(task.priority, 3)

    def test_task_completed_default(self):
        task = Task.objects.create(
            title='Task',
            description='Description',
            deadline=timezone.now() + timedelta(days=1),
            user=self.user
        )
        self.assertFalse(task.is_completed)


class CategoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_category_creation(self):
        category = Category.objects.create(
            name='Work',
            description='Work related tasks',
            user=self.user
        )
        self.assertEqual(category.name, 'Work')
        self.assertEqual(str(category), 'Work')
        self.assertEqual(category.user, self.user)

    def test_category_with_tasks(self):
        category = Category.objects.create(
            name='Personal',
            description='Personal tasks',
            user=self.user
        )
        task = Task.objects.create(
            title='Task 1',
            description='Description',
            deadline=timezone.now() + timedelta(days=1),
            user=self.user
        )
        task.categories.add(category)
        
        self.assertEqual(category.tasks.count(), 1)


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.task = Task.objects.create(
            title='Test Task',
            description='Description',
            deadline=timezone.now() + timedelta(days=1),
            user=self.user
        )

    def test_comment_creation(self):
        comment = Comment.objects.create(
            content='This is a test comment',
            user=self.user,
            task=self.task
        )
        self.assertEqual(comment.content, 'This is a test comment')
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.task, self.task)

    def test_comment_str(self):
        comment = Comment.objects.create(
            content='Test comment',
            user=self.user,
            task=self.task
        )
        self.assertIn(self.user.username, str(comment))
        self.assertIn(self.task.title, str(comment))


class TaskViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            deadline=timezone.now() + timedelta(days=7),
            priority=3,
            user=self.user
        )

    def test_task_list_view_requires_login(self):
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 302)

    def test_task_list_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_detail_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(f'/tasks/{self.task.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_create_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/tasks/create/')
        self.assertEqual(response.status_code, 200)

    def test_task_toggle_complete(self):
        self.client.login(username='testuser', password='testpass123')
        self.assertFalse(self.task.is_completed)
        
        response = self.client.get(f'/tasks/{self.task.pk}/toggle/')
        self.task.refresh_from_db()
        
        self.assertTrue(self.task.is_completed)


class CategoryViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            description='Description',
            user=self.user
        )

    def test_category_list_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')

    def test_category_create_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/categories/create/')
        self.assertEqual(response.status_code, 200)


class AuthenticationViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_login_view(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        response = self.client.post('/accounts/register/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
