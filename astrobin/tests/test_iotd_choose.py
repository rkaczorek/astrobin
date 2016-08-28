# Python
import datetime

# Django
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.test import TestCase

# AstroBin
from astrobin.models import (
    Image, ImageOfTheDay, ImageOfTheDayCandidate)


class IOTDChooseTest(TestCase):
    def _assert_message(self, response, tags, content):
        storage = response.context[0]['messages']
        for message in storage:
            self.assertEqual(message.tags, tags)
            self.assertTrue(content in message.message)

    def test_page_exists(self):
        response = self.client.get(reverse('iotd_choose'))
        self.assertEqual(response.status_code, 302)

    def test_page_accessible_by_iotd_staff(self):
        user = User.objects.create_user('test', 'test@test.com', 'password')
        self.client.login(username = 'test', password = 'password')
        response = self.client.get(reverse('iotd_choose'))
        self.assertEqual(response.status_code, 403)


        group = Group.objects.create(name = 'IOTD_Staff')
        user.groups.add(group)
        response = self.client.get(reverse('iotd_choose'))
        self.assertEqual(response.status_code, 200)

        group.delete()
        user.delete()

    def test_iotd_already_exists(self):
        user = User.objects.create_user('test', 'test@test.com', 'password')
        group = Group.objects.create(name = 'IOTD_Staff')
        user.groups.add(group)
        self.client.login(username = 'test', password = 'password')

        self.client.post(reverse('image_upload_process'), {'image_file': open('astrobin/fixtures/test.jpg', 'rb')})
        image = Image.all_objects.all().order_by('-id')[0]
        iotd, created = ImageOfTheDay.objects.get_or_create(
            image = image, date = datetime.date.today)

        response = self.client.get(reverse('iotd_choose'))
        self._assert_message(response, "error unread", "was already chosen")

        iotd.delete()
        image.delete()
        group.delete()
        user.delete()

    def test_iotd_choose_confirm(self):
        user = User.objects.create_user('test', 'test@test.com', 'password')
        group = Group.objects.create(name = 'IOTD_Staff')
        user.groups.add(group)
        self.client.login(username = 'test', password = 'password')

        self.client.post(reverse('image_upload_process'), {'image_file': open('astrobin/fixtures/test.jpg', 'rb')})
        image = Image.all_objects.all().order_by('-id')[0]
        response = self.client.get(reverse('iotd_choose', kwargs = {'image_pk': image.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual('image' in response.context[0], True)

        image.delete()
        group.delete()
        user.delete()

    def test_iotd_choose_post(self):
        user = User.objects.create_user('test', 'test@test.com', 'password')
        group = Group.objects.create(name = 'IOTD_Staff')
        user.groups.add(group)
        self.client.login(username = 'test', password = 'password')

        # No args
        response = self.client.post(reverse('iotd_choose'))
        self.assertEqual(response.status_code, 405)

        # Arg ok but image not in candidates
        self.client.post(reverse('image_upload_process'), {'image_file': open('astrobin/fixtures/test.jpg', 'rb')})
        image = Image.all_objects.all().order_by('-id')[0]
        response = self.client.post(reverse('iotd_choose', kwargs = {'image_pk': image.pk}))
        self.assertEqual(response.status_code, 403)

        # All should be ok
        candidate, created = ImageOfTheDayCandidate.objects.get_or_create(
            image = image,
            position = 1)
        response = self.client.post(reverse('iotd_choose', kwargs = {'image_pk': image.pk}))
        self.assertEqual(response.status_code, 200)
        iotd = ImageOfTheDay.objects.all()[0]
        self.assertEqual(iotd.image, image)
        self.assertEqual(iotd.chosen_by, user)

        iotd.delete()
        candidate.delete()
        image.delete()
        group.delete()
        user.delete()