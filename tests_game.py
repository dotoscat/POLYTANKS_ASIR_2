import time
import unittest
import unittest.mock
import toyblock3
import polytanks
import polytanks.entity
import server.engine
import server.entity
import server.protocol
import server.server
import server.gamemode
import client.scene
import client.client

"""
Estos son test generales, tanto del servidor como del cliente, para el juego.
"""

ManagedBlastzone = toyblock3.Manager(polytanks.entity.Blastzone, 1)
ManagedBlastzone()

SERVER = ("127.0.0.1", 1337)

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
        self.assertTrue(self.ManagedBullet.pool.used, "Bullet is freed!")
        bullet = self.ManagedBullet()
        bullet.body.y = -82
        self._run_once()
        self.assertTrue(self.ManagedBullet.pool.used, "Bullet is not freed!")

    def _run_once(self):
        polytanks.system.collision()

    def _bullet_blastzone(self, bullet, blastzone, bullet_rect, blastzone_rect):
        print("Bom!")
        bullet.free()

class GameProtocol(server.protocol.GameProtocol):
    unittest = None
    def datagram_received(self, data, addr):
        super().datagram_received(data, addr)
        print("unittest", data, len(data), addr)
        print("from unittest", self.unittest)

@unittest.skip("Lack of time for network times.")
class InputTest(unittest.TestCase):
    def test1_shoot_input(self):
        """
        El servidor tiene que crear una bala si en el cliente se dispara.
        """
        self.player = None
        self.game_client = client.client.Client()
        self.game_screen = client.scene.Screen(self.game_client)
        GameProtocol.unittest = self
        self.game_server = server.server.Server(2, SERVER, game_protocol=GameProtocol)
        self.connect_client_with_server()
        self.press_shoot()
        self.assertTrue(
            self.game_server.engine.players[1].input.shoots, "shoot on server should be true!")

    def load(self):
        self.game_screen.engine.load_level()
        self.game_screen.load()
        self.player = self.game_screen.engine.add_player(self.game_client.id)[1]
        self.assertNotEqual(self.player, None, "Player shall not be None!")

    def connect_client_with_server(self):
        self.game_client.connect_to_server(
            SERVER, self.game_screen.udp_from_server,
            self.game_screen.tcp_from_server, self.load, self.game_screen.rudp_from_server
        )
        while not self.player:
            self.tick()
            
    def tick(self):
        self.game_client.step()
        self.game_server.loop._run_once()

    def press_shoot(self):
        player = self.game_screen.engine.players[1]
        player.input.shoots = True
        player.input.move = -1.
        self.game_screen.send_input_to_server(0.)
        self.assertTrue(self.player.input.shoots)
        self.tick()
        self.assertTrue(self.player.input.shoots)

class GamemodeTest(unittest.TestCase):
    def run_gamemode_for(self, gamemode, secs):
        last = time.monotonic()
        seconds = 0.
        while seconds < secs:
            now = time.monotonic()
            dt = now - last
            seconds += dt
            gamemode.run_steps(dt)
            last = now
            time.sleep(0.1)

    def test1_steps(self):
        class TestMode(server.gamemode.AbstractGameMode):
            pass

        testmode = TestMode(object(), object(), ready_time=1., running_time=2., gameover_time=3.)
        testmode.running_step = unittest.mock.Mock()
        testmode.running = unittest.mock.Mock()
        testmode.ready = unittest.mock.Mock()
        testmode.gameover = unittest.mock.Mock()

        self.run_gamemode_for(testmode, 10)

        self.assertEqual(testmode.ready.call_count, 1, "Does not start with READY!")
        self.assertEqual(testmode.running.call_count, 2, "running doesn't called twice in 10 secs.")
        self.assertEqual(testmode.gameover.call_count, 2, "gameover doesn't called twice in 10 secs.")
        self.assertTrue(testmode.running_step.call_count > 10, "running_step doesn't called in running within 10 secs.")

    def test2_createpowerup(self):
        engine_mock = unittest.mock.Mock(server.engine.Engine)
        standard = server.gamemode.Standard(object(), engine_mock)
        self.run_gamemode_for(standard, 10)
        self.assertTrue(engine_mock.add_powerup.called, "powerup not added")
