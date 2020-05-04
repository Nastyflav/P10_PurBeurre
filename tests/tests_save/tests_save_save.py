#! /usr/bin/env python3
# coding: utf-8

"""
Author: [Nastyflav](https://github.com/Nastyflav) 2020-04-30
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

"""

from django.test import TestCase, Client
from django.db import IntegrityError
from django.urls import reverse

from save.models import Favorites
from search.models import Category, Product
from authentication.models import User


def db_init():
    """Create a temp user and temp products to perform tests"""
    user = User.objects.create(email='remy@purbeurre.fr')
    user.set_password('pixar2020')
    user.save()

    data = Category(name="Pate à tartiner")
    data.save()

    data = Product(
        name="Beurre de cacahuètes",
        category_id=Category.objects.get(name="Pate à tartiner"),
        store="Carrefour",
        nutriscore="c",
        barcode="012456870000",
        url="https://peanutbutter.fr",
        image="https://peanutbutter.fr/photo.jpg",
        lipids_for_100g="2.60",
        saturated_fats_for_100g="0.59",
        sugars_for_100g="0.11",
        salt_for_100g="3.51",
    )
    data.save()

    data = Product(
        name="Ovomaltine",
        category_id=Category.objects.get(name="Pate à tartiner"),
        store="Leclerc, BioCoop",
        nutriscore="a",
        barcode="0189654870000",
        url="https://ovomaltine.fr",
        image="https://ovomaltine.fr/photo.jpg",
        lipids_for_100g="4.59",
        saturated_fats_for_100g="0.02",
        sugars_for_100g="1.54",
        salt_for_100g="3.25",
    )
    data.save()

    data = Product(
        name="Nutella",
        category_id=Category.objects.get(name="Pate à tartiner"),
        store="Auchan",
        nutriscore="c",
        barcode="012232370000",
        url="https://nutella.fr",
        image="https://nutella.fr/photo.jpg",
        lipids_for_100g="1.64",
        saturated_fats_for_100g="0.33",
        sugars_for_100g="2.20",
        salt_for_100g="1.06",
    )
    data.save()


class TestSaveSave(TestCase):
    """To test the subs and saving functionalities"""
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.favorites_url = reverse('save:favorites')
        cls.save_url = reverse('save:save')
        db_init()
    
    def test_save_if_user_not_logged_in(self):   # checking saving_product()
        """To check the redirection when an unlogged user tries to save a prod"""
        user_id = User.objects.get(email='remy@purbeurre.fr').id
        response = self.client.post(
            self.save_url, {
                'original_product_id': Product.objects.get(id=1).id,
                'substitute_id': Product.objects.get(id=2).id,
                'user_id': user_id,
                'next': '/',
            }
        )
        self.assertRedirects(
            response, '/authentication?next=/save/save/',
            status_code=302, target_status_code=301)

    def test_save_if_original_product_no_longer_exists(self):
        """To check the error raising when a substituted product is erased"""
        user_id = User.objects.get(email='remy@purbeurre.fr').id
        with self.assertRaises(Product.DoesNotExist):
            response = self.client.post(
                self.save_url, {
                    'original_product_id': Product.objects.get(id=10).id,
                    'substitute_id': Product.objects.get(id=2).id,
                    'user_id': user_id,
                }
            )

    def test_save_without_any_savings_yet(self):
        """To check a fresh account with no saved products"""
        self.client.login(
            username='remy@purbeurre.fr',
            password='pixar2020')

        user_id = User.objects.get(email='remy@purbeurre.fr').id
        self.assertEqual(Favorites.objects.all().count(), 0)
