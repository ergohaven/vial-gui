# SPDX-License-Identifier: GPL-2.0-or-later
import os
import sys
from PyQt5.QtCore import QTranslator, QLocale, QSettings

_translator = None
SETTINGS_KEY = "language"

def get_available_languages():
    """Returns list of (locale_code, display_name) tuples"""
    return [
        ("", "English"),
        ("ru", "Русский"),
    ]

def get_saved_language():
    """Get previously saved language preference"""
    settings = QSettings("Vial", "Vial")
    return settings.value(SETTINGS_KEY, "")

def save_language(locale_code):
    """Save language preference"""
    settings = QSettings("Vial", "Vial")
    settings.setValue(SETTINGS_KEY, locale_code)

def install_translator(app, locale=None):
    """Install translator based on locale or saved preference."""
    global _translator

    if locale is None:
        saved = get_saved_language()
        if saved:
            locale = saved
        else:
            locale = QLocale.system().name()

    if not locale.startswith("ru"):
        return

    _translator = QTranslator()

    search_paths = []
    if getattr(sys, "_MEIPASS", None):
        search_paths.append(os.path.join(sys._MEIPASS, "i18n"))
    base_dir = os.path.dirname(os.path.abspath(__file__))
    search_paths.append(os.path.join(base_dir, "..", "resources", "base", "i18n"))
    search_paths.append(os.path.join(base_dir, "i18n"))

    for path in search_paths:
        qm_path = os.path.join(path, "vial_ru.qm")
        if os.path.exists(qm_path):
            if _translator.load(qm_path):
                app.installTranslator(_translator)
                return

    if _translator.load("vial_ru", ":/i18n"):
        app.installTranslator(_translator)
