import zlib
from ativos.models import Computer
from django.test import TestCase, Client
from django.conf import settings


# Create your tests here.
class AtivosTestCase(TestCase):
    def test_deve_cadastrar_um_ativo(self):
        with open("./ativos/fixtures/inventory.xml", "r") as inventory_xml:
            c = Client()
            c.post(
                "/ativos/inventory/",
                zlib.compress(
                    bytes(inventory_xml.read(), encoding=settings.DEFAULT_CHARSET)
                ),
                content_type="application/x-compress-zlib",
            )

        computador = Computer.objects.get(hostname="PNG-DEV005")
        self.assertTrue(computador)
