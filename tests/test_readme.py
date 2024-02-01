import os

from .conftest import BASE_DIR


class TestReadme:
    def test_readme(self):
        try:
            with open(
                f'{os.path.join(BASE_DIR, "README.md")}', "r", encoding="utf-8"
            ) as f:
                readme = f.read()
        except FileNotFoundError:
            assert False, "Проверьте, что добавили файл README.md"
