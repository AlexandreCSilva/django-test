from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal
from .models import Account, Tree, PlantedTree

User = get_user_model()

class TreePlantingTestCase(TestCase):

  @classmethod
  def setUpTestData(selg):
    selg.account_city_volunteers = Account.objects.create(name='Voluntários da Cidade')
    selg.account_forest_guardians = Account.objects.create(name='Guardiões da Floresta')

    selg.user_alice = User.objects.create_user(username='alice', password='password123')
    selg.user_bob = User.objects.create_user(username='bob', password='password123')
    selg.user_charlie = User.objects.create_user(username='charlie', password='password123')

    selg.user_alice.accounts.add(selg.account_city_volunteers)
    selg.user_bob.accounts.add(selg.account_city_volunteers, selg.account_forest_guardians)
    selg.user_charlie.accounts.add(selg.account_forest_guardians)

    selg.tree_oak = Tree.objects.create(name='Carvalho', scientific_name='Quercus robur')
    selg.tree_pine = Tree.objects.create(name='Pinheiro', scientific_name='Pinus sylvestris')

    selg.alice_tree = PlantedTree.objects.create(
      user=selg.user_alice,
      tree=selg.tree_oak,
      account=selg.account_city_volunteers,
      latitude=Decimal('40.7128'),
      longitude=Decimal('-74.0060')
    )
    selg.bob_tree = PlantedTree.objects.create(
      user=selg.user_bob,
      tree=selg.tree_pine,
      account=selg.account_city_volunteers,
      latitude=Decimal('34.0522'),
      longitude=Decimal('-118.2437')
    )
    selg.charlie_tree = PlantedTree.objects.create(
      user=selg.user_charlie,
      tree=selg.tree_oak,
      account=selg.account_forest_guardians,
      latitude=Decimal('48.8566'),
      longitude=Decimal('2.3522')
    )

  def test_user_specific_tree_list_is_rendered_correctly(self):
    self.client.login(username='alice', password='password123')
    
    response = self.client.get(reverse('user-trees'))

    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'trees/user_planted_trees.html')
    self.assertContains(response, self.tree_oak.name)
    self.assertNotContains(response, self.tree_pine.name)

  def test_access_to_other_user_tree_is_forbidden(self):
    self.client.login(username='alice', password='password123')

    response = self.client.get(reverse('planted-tree-detail', kwargs={'pk': self.charlie_tree.pk}))

    self.assertEqual(response.status_code, 403)

  def test_account_shared_tree_list_is_rendered_correctly(self):
    self.client.login(username='bob', password='password123')

    response = self.client.get(reverse('account-trees'))

    print(response)
    
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'trees/account_planted_trees.html')
    
    self.assertContains(response, self.tree_oak.name, 2)
    self.assertContains(response, self.tree_pine.name, 1)

  def test_account_not_shared_tree_list_is_rendered_correctly(self):
    self.client.login(username='alice', password='password123')

    response = self.client.get(reverse('account-trees'))

    print(response)
    
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'trees/account_planted_trees.html')
    
    self.assertContains(response, self.tree_oak.name, 1)
    self.assertContains(response, self.tree_pine.name, 1)

  def test_plant_tree_unit_method(self):
    user = self.user_alice
    initial_tree_count = PlantedTree.objects.filter(user=user).count()

    user.plant_tree(
      tree=self.tree_pine,
      location=(Decimal('51.5074'), Decimal('-0.1278')),
      account=self.account_city_volunteers
    )

    self.assertEqual(PlantedTree.objects.filter(user=user).count(), initial_tree_count + 1)
    last_planted_tree = PlantedTree.objects.filter(user=user).latest('planted_at')
    self.assertEqual(last_planted_tree.tree, self.tree_pine)

  def test_plant_trees_unit_method(self):
    user = self.user_bob
    initial_tree_count = PlantedTree.objects.filter(user=user).count()
    
    trees_to_plant = [
      (self.tree_oak, (Decimal('35.6895'), Decimal('139.6917')), self.account_forest_guardians),
      (self.tree_pine, (Decimal('35.6895'), Decimal('139.6917')), self.account_forest_guardians),
    ]

    user.plant_trees(trees_to_plant)

    self.assertEqual(PlantedTree.objects.filter(user=user).count(), initial_tree_count + len(trees_to_plant))