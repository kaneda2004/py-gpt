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

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel
from core.debug.config import ConfigDebug
from core.debug.context import ContextDebug
from core.debug.presets import PresetsDebug
from core.debug.models import ModelsDebug


class Debug:
    DBG_KEY, DBG_VALUE = range(2)

    def __init__(self, window=None):
        """
        Debug handler

        :param window: main UI window object
        """
        self.window = window

        # setup workers
        self.workers = {}
        self.workers['config'] = ConfigDebug(self.window)
        self.workers['context'] = ContextDebug(self.window)
        self.workers['presets'] = PresetsDebug(self.window)
        self.workers['models'] = ModelsDebug(self.window)

        # prepare debug ids
        self.ids = self.workers.keys()
        self.models = {}
        self.initialized = {}
        self.active = {}
        self.idx = {}
        self.counters = {}

        # prepare debug workers data
        for id in self.ids:
            self.models[id] = self.create_model(self.window)
            self.initialized[id] = False
            self.active[id] = False
            self.idx[id] = 0

    def update(self, all=False):
        """
        Updates debug windows

        :param all: update all debug windows
        """
        not_realtime = ['context']
        for id in self.workers:
            if id in self.active and self.active[id]:
                if all or id not in not_realtime:
                    self.workers[id].update()

    def begin(self, id):
        """
        Begins debug data

        :param id: debug id
        """
        self.window.debug[id].setModel(self.models[id])
        if id not in self.counters or self.counters[id] != self.models[id].rowCount():
            self.models[id].removeRows(0, self.models[id].rowCount())
            self.initialized[id] = False
        self.idx[id] = 0

    def end(self, id):
        """
        Ends debug data

        :param id: debug id
        """
        self.counters[id] = self.idx[id]
        self.initialized[id] = True

    def add(self, id, k, v):
        """
        Appends debug entry

        :param id: debug id
        :param k: key
        :param v: value
        """
        if self.initialized[id] is False:
            idx = self.models[id].rowCount()
            self.models[id].insertRow(idx)
            self.models[id].setData(self.models[id].index(idx, self.DBG_KEY), k)
            self.models[id].setData(self.models[id].index(idx, self.DBG_VALUE), v)
        else:
            for idx in range(0, self.models[id].rowCount()):
                if self.models[id].index(idx, self.DBG_KEY).data() == k:
                    self.models[id].setData(self.models[id].index(idx, self.DBG_VALUE), v)
                    self.idx[id] += 1
                    return
        self.idx[id] += 1

    def create_model(self, parent):
        """
        Creates list model

        :param parent: parent widget
        :return: model instance
        """
        model = QStandardItemModel(0, 2, parent)
        model.setHeaderData(self.DBG_KEY, Qt.Horizontal, "Key")
        model.setHeaderData(self.DBG_VALUE, Qt.Horizontal, "Value")
        return model
