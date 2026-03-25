#!/bin/bash
# Compile Qt translation files
# Run this script when updating translations
# Requires: lrelease (from Qt5 tools)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
lrelease "$SCRIPT_DIR/vial_ru.ts" -qm "$SCRIPT_DIR/vial_ru.qm"
echo "Compiled vial_ru.qm"
