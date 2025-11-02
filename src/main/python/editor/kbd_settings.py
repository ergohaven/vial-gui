# SPDX-License-Identifier: GPL-2.0-or-later
from editor.qmk_settings import QmkSettings


class KbdSettings(QmkSettings):

    def rebuild(self, device):
        super(QmkSettings, self).rebuild(device)
        if self.valid():
            self.keyboard = device.keyboard
            self.settings_set = self.keyboard.qmk_settings.kbd_settings_set
            self.qmk_settings = self.keyboard.qmk_settings
            self.reload_settings()
