# SPDX-License-Identifier: GPL-2.0-or-later
from editor.qmk_settings import QmkSettings
from protocol.constants import VIAL_PROTOCOL_QMK_SETTINGS
from vial_device import VialKeyboard


class KbdSettings(QmkSettings):

    def rebuild(self, device):
        super(QmkSettings, self).rebuild(device)
        if self.valid():
            self.keyboard = device.keyboard
            self.settings_set = self.keyboard.qmk_settings.kbd_settings_set
            self.qmk_settings = self.keyboard.qmk_settings
            self.reload_settings()

    def valid(self):
        return (isinstance(self.device, VialKeyboard) and
                (self.device.keyboard and self.device.keyboard.vial_protocol
                 >= VIAL_PROTOCOL_QMK_SETTINGS and len(self.settings_set)))
