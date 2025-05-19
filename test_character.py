import unittest
from unittest.mock import patch
from main import Character  # main.py에 Character 클래스가 정의돼 있다고 가정

class TestCharacter(unittest.TestCase):
    def setUp(self):
        self.player = Character("Player", 100, 20, 5, 10, 50)
        self.enemy = Character("Enemy", 80, 15, 3, 8, 10)

    def test_take_damage_without_defense(self):
        damage = self.player.take_damage(30)
        self.assertEqual(self.player.health, 70)
        self.assertEqual(damage, 30)

    def test_take_damage_with_defense(self):
        self.player.is_defending = True
        damage = self.player.take_damage(30)
        self.assertEqual(self.player.health, 75)
        self.assertEqual(damage, 25)

    @patch('random.randint', return_value=30)  # 치명타 아님
    def test_attack_enemy_normal(self, mock_randint):
        damage, crit = self.player.attack_enemy(self.enemy)
        self.assertEqual(damage, 20)
        self.assertFalse(crit)

    @patch('random.randint', return_value=10)  # 치명타 발생
    def test_attack_enemy_critical(self, mock_randint):
        damage, crit = self.player.attack_enemy(self.enemy)
        self.assertEqual(damage, 40)
        self.assertTrue(crit)

    def test_is_alive(self):
        self.assertTrue(self.player.is_alive())
        self.player.health = 0
        self.assertFalse(self.player.is_alive())

if __name__ == '__main__':
    unittest.main()