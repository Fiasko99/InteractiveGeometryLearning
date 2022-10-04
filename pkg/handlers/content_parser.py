import json
from typing import Any, Dict

from pkg.handlers.paths import resource_path


def parse_content_data() -> Dict[str, Dict[str, Any]]:
    """Функция служит для преобразования `content.json` в словарь.

    :return: Словарь с темами.
    """
    with open(
        resource_path("content.json"),
        mode="r",
        encoding="utf-8",
    ) as file:
        return json.load(file)
