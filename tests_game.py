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
        last_bullet = self.ManagedBullet()
        polytanks.system.collision.register_callbacks(
            (polytanks.collision.BULLET, polytanks.collision.BLAST_ZONE),
            start=self._bullet_blastzone
        )
        self._run_once()
        bullet = self.ManagedBullet()
        self._run_once()

    def _run_once(self):
        polytanks.system.collision()
        self.assertTrue(self.collided and len(self.ManagedBullet.pool.used) == 0, "Bullet is not freed!")
        self.collided = False

    def _bullet_blastzone(self, bullet, blastzone, bullet_rect, blastzone_rect):
        print("Bom!")
        bullet.free()
        self.collided = True
