#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
lrelease "$SCRIPT_DIR/vial_ru.ts" -qm "$SCRIPT_DIR/vial_ru.qm"
echo "Compiled vial_ru.qm"
