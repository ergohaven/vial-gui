# SPDX-License-Identifier: GPL-2.0-or-later
import os
import sys
from PyQt5.QtCore import QTranslator, QLocale, QCoreApplication


_translator = None


def install_translator(app, locale=None):
    """Install Russian translator if locale is Russian or locale is explicitly set."""
    global _translator

    if locale is None:
        locale = QLocale.system().name()  # e.g. "ru_RU"

    if not locale.startswith("ru"):
        return

    _translator = QTranslator()

    # Try to find the .qm file
    search_paths = []

    # When running from fbs build
    if getattr(sys, "_MEIPASS", None):
        search_paths.append(os.path.join(sys._MEIPASS, "i18n"))

    # Running from source
    base_dir = os.path.dirname(os.path.abspath(__file__))
    search_paths.append(os.path.join(base_dir, "..", "resources", "base", "i18n"))
    search_paths.append(os.path.join(base_dir, "i18n"))

    for path in search_paths:
        qm_path = os.path.join(path, "vial_ru.qm")
        if os.path.exists(qm_path):
            if _translator.load(qm_path):
                app.installTranslator(_translator)
                return

    # Fallback: try loading by name from Qt resource system
    if _translator.load("vial_ru", ":/i18n"):
        app.installTranslator(_translator)
