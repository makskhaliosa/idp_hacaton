import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

root_dir_content = os.listdir(BASE_DIR)
PROJECT_DIR_NAME = "idp"

if PROJECT_DIR_NAME not in root_dir_content or not os.path.isdir(
    os.path.join(BASE_DIR, PROJECT_DIR_NAME)
):
    assert False, (
        f"В директории `{BASE_DIR}` не найдена папка c проектом "
        f"`{PROJECT_DIR_NAME}`. Убедитесь, что у вас верная структура проекта."
    )

pytest_plugins = [
    "tests.fixtures.fixture_user",
]
