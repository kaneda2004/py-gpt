#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Created Date: 2023.04.09 20:00:00                  #
# ================================================== #

from core.ui.dialog.settings import Settings
from core.ui.dialog.preset import Preset
from core.ui.dialog.debug import Debug
from core.ui.dialog.about import About
from core.ui.dialog.changelog import Changelog
from core.ui.dialog.editor import Editor
from core.ui.dialog.ctx_rename import CtxRename
from core.ui.dialog.start import Start
from core.ui.dialog.update import Update
from core.ui.dialog.image import Image
from core.ui.widgets import AlertDialog, ConfirmDialog


class Dialogs:
    def __init__(self, window=None):
        """
        Dialogs setup

        :param window: main UI window object
        """
        self.window = window

    def setup(self):
        """Setups dialogs"""
        self.window.dialog = {}
        self.window.debug = {}
        self.window.editor = {}

        # setup debug dialogs
        debug = Debug(self.window)
        for id in self.window.debugger.ids:
            debug.setup(id)

        # setup info dialogs
        about = About(self.window)
        changelog = Changelog(self.window)
        about.setup()
        changelog.setup()

        # setup settings dialog
        settings = Settings(self.window)
        settings.setup()

        # setup preset editor dialog
        preset = Preset(self.window)
        preset.setup()

        # setup editor dialog
        editor = Editor(self.window)
        editor.setup()

        # setup ctx rename dialog
        ctx_rename = CtxRename(self.window)
        ctx_rename.setup()

        # setup start dialog
        start = Start(self.window)
        start.setup()

        # setup update dialog
        update = Update(self.window)
        update.setup()

        # setup image dialog
        image = Image(self.window)
        image.setup()

        # alert / confirm
        self.window.dialog['alert'] = AlertDialog(self.window)
        self.window.dialog['confirm'] = ConfirmDialog(self.window)

    def confirm(self, type, id, msg):
        """
        Shows confirm dialog

        :param type: confirm type
        :param id: confirm object id
        :param msg: message to show
        """
        self.window.dialog['confirm'].type = type
        self.window.dialog['confirm'].id = id
        self.window.dialog['confirm'].message.setText(msg)
        self.window.dialog['confirm'].show()

    def alert(self, msg):
        """
        Shows alert dialog

        :param msg: message to show
        """
        self.window.dialog['alert'].message.setPlainText(msg)
        self.window.dialog['alert'].show()

    def open_editor(self, id, data_id, width=400, height=400):
        """
        Opens editor dialog

        :param id: debug dialog id
        :param data_id: data id
        :param width: dialog width
        :param height: dialog height
        """
        if id not in self.window.dialog:
            return
        self.window.dialog[id].resize(width, height)
        self.window.dialog[id].data_id = data_id
        self.window.dialog[id].show()

    def open(self, id, width=400, height=400):
        """
        Opens debug/config dialog

        :param id: debug dialog id
        :param width: dialog width
        :param height: dialog height
        """
        if id not in self.window.dialog:
            return
        self.window.dialog[id].resize(width, height)
        qr = self.window.dialog[id].frameGeometry()
        cp = self.window.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.window.dialog[id].move(qr.topLeft())
        self.window.dialog[id].show()

    def close(self, id):
        """
        Closes debug/config dialog

        :param id: debug dialog id
        """
        if id not in self.window.dialog:
            return
        self.window.dialog[id].close()
