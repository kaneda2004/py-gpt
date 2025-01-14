# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Created Date: 2023.04.09 20:00:00                  #
# ================================================== #

from core.controller.model import Model
from core.controller.presets import Presets
from core.controller.plugins import Plugins
from core.controller.debug import Debug
from core.controller.settings import Settings
from core.controller.info import Info
from core.controller.input import Input
from core.controller.output import Output
from core.controller.context import Context
from core.controller.confirm import Confirm
from core.controller.ui import UI
from core.controller.launcher import Launcher
from core.controller.lang import Lang
from core.controller.image import Image


class Controller:
    def __init__(self, window=None):
        """
        Main controller

        :param window: main window object
        """
        self.window = window
        self.model = Model(window)
        self.presets = Presets(window)
        self.plugins = Plugins(window)
        self.debug = Debug(window)
        self.settings = Settings(window)
        self.info = Info(window)
        self.input = Input(window)
        self.output = Output(window)
        self.context = Context(window)
        self.confirm = Confirm(window)
        self.ui = UI(window)
        self.launcher = Launcher(window)
        self.lang = Lang(window)
        self.image = Image(window)

    def setup(self):
        """Setups controller"""
        self.lang.setup()
        self.model.setup()
        self.input.setup()
        self.output.setup()
        self.context.setup()
        self.ui.setup()
        self.info.setup()
        self.launcher.setup()
