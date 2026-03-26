# SPDX-License-Identifier: GPL-2.0-or-later
import os
import sys
from PyQt5.QtCore import QTranslator, QLocale, QSettings

_translator = None
SETTINGS_KEY = "language"
# Sentinel value meaning "user has never chosen a language — use system locale"
LANG_AUTO = "__auto__"

def get_available_languages():
    """Returns list of (locale_code, display_name) tuples"""
    return [
        ("", "English"),
        ("ru", "Русский"),
    ]

def get_saved_language():
    """Get previously saved language preference. Returns '' for English, 'ru' for Russian,
    or LANG_AUTO if the user has never made a choice."""
    settings = QSettings("Vial", "Vial")
    return settings.value(SETTINGS_KEY, LANG_AUTO)

def save_language(locale_code):
    """Save language preference. Pass '' to explicitly select English."""
    import sys
    settings = QSettings("Vial", "Vial")
    settings.setValue(SETTINGS_KEY, locale_code)
    # On WASM, also persist to localStorage via JS bridge
    if sys.platform == "emscripten":
        try:
            import vialglue
            vialglue.save_language(locale_code)
        except Exception:
            pass

def switch_language(app, locale_code):
    """Switch application language at runtime without restart."""
    global _translator
    save_language(locale_code)
    if _translator is not None:
        app.removeTranslator(_translator)
        _translator = None
    if locale_code:
        install_translator(app, locale_code)

def install_translator(app, locale=None):
    """Install translator based on locale or saved preference.
    On first run (no saved preference), auto-detects system locale."""
    global _translator

    if locale is None:
        saved = get_saved_language()
        if saved == LANG_AUTO:
            # First run: use system locale
            locale = QLocale.system().name()
        elif saved:
            locale = saved
        else:
            # User explicitly chose English
            return

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

def install_translator_web(app):
    """For WASM/web: use locale passed from JS bridge via env vars.
    Priority: user's explicit choice > browser language > English."""
    import os
    lang_pref = os.environ.get("VIAL_BROWSER_LANG_PREF", LANG_AUTO)
    browser_locale = os.environ.get("VIAL_BROWSER_LOCALE", "")

    if lang_pref == LANG_AUTO:
        # No explicit user choice — use browser language
        locale = browser_locale
    elif lang_pref:
        locale = lang_pref
    else:
        # User explicitly chose English
        return

    if locale:
        install_translator(app, locale)
