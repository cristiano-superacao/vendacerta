import importlib
import os
import sys
import unittest


class TestConfigFallback(unittest.TestCase):
    def test_sqlite_fallback_when_enabled(self):
        # Garante que o fallback só é usado quando explicitamente habilitado.
        old_env = os.environ.copy()
        try:
            os.environ.pop('DATABASE_URL', None)
            os.environ.pop('URL_DO_BANCO_DE_DADOS', None)

            for key in ['PGDATABASE', 'PGHOST', 'PGUSER', 'PGPASSWORD', 'PGPORT']:
                os.environ.pop(key, None)

            os.environ['ALLOW_SQLITE_DEV'] = '1'

            if 'config' in sys.modules:
                del sys.modules['config']

            import config  # noqa: F401
            importlib.reload(config)

            uri = config.Config.SQLALCHEMY_DATABASE_URI
            self.assertTrue(uri.startswith('sqlite'), f"Esperado SQLite, obtido: {uri}")
        finally:
            os.environ.clear()
            os.environ.update(old_env)


if __name__ == '__main__':
    unittest.main()
