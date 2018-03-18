import unittest
import toyblock3
import polytanks
import polytanks.entity
import server
import server.entity

"""
Estos son test generales, tanto del servidor como del cliente, para el juego.
"""

ManagedBlastzone = toyblock3.Manager(polytanks.entity.Blastzone, 1)
ManagedBlastzone()

class TestBullets(unittest.TestCase):
    def test_bullets_freed_in_blastzone(self):
        self.collided = False
        self.ManagedBullet = toyblock3.Manager(server.entity.Bullet, 3)
        bullet = self.ManagedBullet()
        polytanks.system.collision.register_callbacks(
            (polytanks.collision.BULLET, polytanks.collision.BLAST_ZONE),
            end=self._bullet_blastzone
        )
        self._run_once()
        self.assertFalse(self.ManagedBullet.pool.used, "Bullet is freed!")
        bullet = self.ManagedBullet()
        bullet.body.y = -82
        self._run_once()
        self.assertTrue(self.ManagedBullet.pool.used, "Bullet is not freed!")

    def _run_once(self):
        polytanks.system.collision()

    def _bullet_blastzone(self, bullet, blastzone, bullet_rect, blastzone_rect):
        print("Bom!")
        bullet.free()
