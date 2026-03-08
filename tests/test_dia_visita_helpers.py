import unittest
from datetime import datetime

from helpers import (
    get_dia_visita_hoje,
    normalizar_dia_visita,
    dia_visita_label,
    dia_visita_sort_key,
    listar_dias_visita_validos,
)


class TestDiaVisitaHelpers(unittest.TestCase):
    def test_normalizar_dia_visita(self):
        self.assertEqual(normalizar_dia_visita("Segunda-feira"), "segunda")
        self.assertEqual(normalizar_dia_visita("terça-feira"), "terca")
        self.assertEqual(normalizar_dia_visita("SÁBADO"), "sabado")
        self.assertIsNone(normalizar_dia_visita(None))

    def test_get_dia_visita_hoje(self):
        # 2024-01-01 foi segunda-feira
        self.assertEqual(get_dia_visita_hoje(datetime(2024, 1, 1, 12, 0, 0)), "segunda")
        self.assertEqual(get_dia_visita_hoje(datetime(2024, 1, 2, 12, 0, 0)), "terca")
        self.assertEqual(get_dia_visita_hoje(datetime(2024, 1, 7, 12, 0, 0)), "domingo")

    def test_label_and_order(self):
        self.assertEqual(dia_visita_label("terca"), "Terça-feira")
        self.assertLess(dia_visita_sort_key("segunda"), dia_visita_sort_key("sexta"))
        self.assertIn("domingo", listar_dias_visita_validos())


if __name__ == "__main__":
    unittest.main()
