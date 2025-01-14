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

from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtWidgets import QLineEdit, QTreeView, QAbstractItemView, QMenu, QDialog, QLabel, QCheckBox, QHBoxLayout, \
    QWidget, QSlider, QTextEdit, QDialogButtonBox, QVBoxLayout, QPushButton, QPlainTextEdit, QApplication

from core.utils import trans


class NameInput(QLineEdit):
    def __init__(self, window=None, id=None):
        """
        AI or user name input

        :param window: main window
        :param id: input id
        """
        super(NameInput, self).__init__(window)
        self.window = window
        self.id = id

    def keyPressEvent(self, event):
        """
        Key press event

        :param event: key event
        """
        super(NameInput, self).keyPressEvent(event)
        self.window.controller.ui.update()
        self.window.controller.presets.update_field(self.id, self.text(), self.window.config.data['preset'], True)


class ChatInput(QTextEdit):
    def __init__(self, window=None):
        """
        Chat input

        :param window: main window
        """
        super(ChatInput, self).__init__(window)
        self.window = window
        self.setFocus()

    def keyPressEvent(self, event):
        """
        Key press event

        :param event: key event
        """
        super(ChatInput, self).keyPressEvent(event)
        self.window.controller.ui.update()
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            if self.window.config.data['send_shift_enter']:
                modifiers = QApplication.keyboardModifiers()
                if modifiers == QtCore.Qt.ShiftModifier:
                    self.window.controller.input.send()
            else:
                self.window.controller.input.send()
            self.setFocus()


class ChatOutput(QTextEdit):
    def __init__(self, window=None):
        """
        Chat input

        :param window: main window
        """
        super(ChatOutput, self).__init__(window)
        self.window = window
        self.setReadOnly(True)
        self.setStyleSheet("color: {};".format(self.window.config.data['ui.chatbox.font.color']))


class SelectMenu(QTreeView):
    NAME = range(1)  # list of columns

    def __init__(self, window=None, id=None):
        """
        Select menu

        :param window: main window
        :param id: input id
        """
        super(SelectMenu, self).__init__(window)
        self.window = window
        self.id = id
        self.setStyleSheet("QTreeView {"
                           "padding: 0px;"
                           "margin: 0px;"
                           "};"
                           "QTreeView::item {"
                           "padding: 0px;"
                           "margin: 0px;"
                           "}")
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setIndentation(0)
        self.setHeaderHidden(True)

        self.clicked.connect(self.click)

    def click(self, val):
        self.window.controller.model.select(self.id, val.row())


class PresetSelectMenu(SelectMenu):
    def __init__(self, window=None, id=None):
        """
        Presets select menu

        :param window: main window
        :param id: input id
        """
        super(PresetSelectMenu, self).__init__(window)
        self.window = window
        self.id = id

        self.doubleClicked.connect(self.dblclick)

    def dblclick(self, val):
        """
        Double click event

        :param val: double click event
        """
        self.window.controller.presets.edit(val.row())

    def contextMenuEvent(self, event):
        """
        Context menu event

        :param event: context menu event
        """
        actions = {}
        actions['edit'] = QAction(QIcon.fromTheme("edit-edit"), trans('preset.action.edit'), self)
        actions['edit'].triggered.connect(
            lambda: self.action_edit(event))

        actions['duplicate'] = QAction(QIcon.fromTheme("edit-copy"), trans('preset.action.duplicate'), self)
        actions['duplicate'].triggered.connect(
            lambda: self.action_duplicate(event))

        actions['delete'] = QAction(QIcon.fromTheme("edit-delete"), trans('preset.action.delete'), self)
        actions['delete'].triggered.connect(
            lambda: self.action_delete(event))

        menu = QMenu(self)
        menu.addAction(actions['edit'])
        menu.addAction(actions['duplicate'])
        menu.addAction(actions['delete'])

        item = self.indexAt(event.pos())
        idx = item.row()
        if idx >= 1:
            self.window.controller.model.select(self.id, item.row())
            menu.exec_(event.globalPos())

    def action_edit(self, event):
        """
        Edit action handler

        :param event: mouse event
        """
        item = self.indexAt(event.pos())
        idx = item.row()
        if idx >= 0:
            self.window.controller.presets.edit(idx)

    def action_duplicate(self, event):
        """
        Duplicate action handler

        :param event: mouse event
        """
        item = self.indexAt(event.pos())
        idx = item.row()
        if idx >= 0:
            self.window.controller.presets.duplicate(idx)

    def action_delete(self, event):
        """
        Delete action handler

        :param event: mouse event
        """
        item = self.indexAt(event.pos())
        idx = item.row()
        if idx >= 0:
            self.window.controller.presets.delete(idx)


class ContextSelectMenu(SelectMenu):
    def __init__(self, window=None, id=None):
        """
        Presets select menu

        :param window: main window
        :param id: input id
        """
        super(ContextSelectMenu, self).__init__(window)
        self.window = window
        self.id = id

        self.doubleClicked.connect(self.dblclick)

    def click(self, val):
        """
        Click event

        :param val: click event
        """
        self.window.controller.context.select(val.row())

    def dblclick(self, val):
        """
        Double click event

        :param val: double click event
        """
        self.window.controller.context.select(val.row())

    def contextMenuEvent(self, event):
        """
        Context menu event

        :param event: context menu event
        """
        actions = {}
        actions['rename'] = QAction(QIcon.fromTheme("edit-edit"), trans('ctx.action.rename'), self)
        actions['rename'].triggered.connect(
            lambda: self.action_rename(event))

        actions['delete'] = QAction(QIcon.fromTheme("edit-delete"), trans('ctx.action.delete'), self)
        actions['delete'].triggered.connect(
            lambda: self.action_delete(event))

        menu = QMenu(self)
        menu.addAction(actions['rename'])
        menu.addAction(actions['delete'])

        item = self.indexAt(event.pos())
        idx = item.row()
        if idx >= 0:
            self.window.controller.context.select(item.row())
            menu.exec_(event.globalPos())

    def action_rename(self, event):
        """
        Rename action handler

        :param event: mouse event
        """
        item = self.indexAt(event.pos())
        idx = item.row()
        if idx >= 0:
            self.window.controller.context.rename(idx)

    def action_delete(self, event):
        """
        Delete action handler

        :param event: mouse event
        """
        item = self.indexAt(event.pos())
        idx = item.row()
        if idx >= 0:
            self.window.controller.context.delete(idx)


class DebugDialog(QDialog):
    def __init__(self, window=None, id=None):
        """
        Debug window dialog

        :param window: main window
        :param id: debug window id
        """
        super(DebugDialog, self).__init__(window)
        self.window = window
        self.id = id

    def closeEvent(self, event):
        """
        Close event

        :param event: close event
        """
        self.window.debugger.active[self.id] = False
        self.window.controller.debug.update_menu()


class InfoDialog(QDialog):
    def __init__(self, window=None, id=None):
        """
        Info window dialog

        :param window: main window
        :param id: info window id
        """
        super(InfoDialog, self).__init__(window)
        self.window = window
        self.id = id

    def closeEvent(self, event):
        """
        Close event

        :param event: close event
        """
        self.window.info.active[self.id] = False
        self.window.controller.info.update_menu()


class RenameInput(QLineEdit):
    def __init__(self, window=None, id=None):
        """
        Rename dialog

        :param window: main window
        :param id: info window id
        """
        super(RenameInput, self).__init__(window)

        self.window = window
        self.id = id

    def keyPressEvent(self, event):
        """
        Key press event

        :param event: key event
        """
        super(RenameInput, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            self.window.controller.context.update_name(self.window.dialog['ctx.rename'].current,
                                                       self.text())


class RenameDialog(QDialog):
    def __init__(self, window=None, id=None):
        """
        Rename dialog

        :param window: main window
        :param id: info window id
        """
        super(RenameDialog, self).__init__(window)
        self.window = window
        self.id = id
        self.current = None
        self.input = RenameInput(window, id)
        self.input.setMinimumWidth(400)

        self.window.data['dialog.ctx_rename.btn.update'] = QPushButton(trans('dialog.ctx.rename.update'))
        self.window.data['dialog.ctx_rename.btn.update'].clicked.connect(
            lambda: self.window.controller.context.update_name(self.window.dialog['ctx.rename'].current,
                                                               self.input.text()))

        self.window.data['dialog.ctx_rename.btn.dismiss'] = QPushButton(trans('dialog.ctx.rename.dismiss'))
        self.window.data['dialog.ctx_rename.btn.dismiss'].clicked.connect(
            lambda: self.window.controller.context.dismiss_rename())

        bottom = QHBoxLayout()
        bottom.addWidget(self.window.data['dialog.ctx_rename.btn.dismiss'])
        bottom.addWidget(self.window.data['dialog.ctx_rename.btn.update'])

        self.window.data['dialog.ctx_rename.label'] = QLabel(trans("dialog.ctx.rename.title"))

        layout = QVBoxLayout()
        layout.addWidget(self.window.data['dialog.ctx_rename.label'])
        layout.addWidget(self.input)
        layout.addLayout(bottom)

        self.setLayout(layout)


class SettingsSlider(QWidget):
    def __init__(self, window=None, id=None, title=None, min=None, max=None, step=None, value=None, max_width=True,
                 section=None):
        """
        Settings slider

        :param window: main window
        :param id: option id
        :param title: option title
        :param min: min value
        :param max: max value
        :param step: value step
        :param value: current value
        :param max_width: max width
        :param section: settings section
        """
        super(SettingsSlider, self).__init__(window)
        self.window = window
        self.id = id
        self.title = title
        self.min = min
        self.max = max
        self.step = step
        self.value = value
        self.section = section

        self.label = QLabel(title)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(min)
        self.slider.setMaximum(max)
        self.slider.setSingleStep(step)
        self.slider.setValue(value)
        self.slider.valueChanged.connect(
            lambda: self.window.controller.settings.apply(self.id, self.slider.value(), 'slider', self.section))

        if max_width:
            self.slider.setMaximumWidth(240)

        self.input = SettingsInputInline(self.window, self.id, self.section)
        self.input.setText(str(value))

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.input)

        self.setLayout(self.layout)


class SettingsCheckbox(QWidget):
    def __init__(self, window=None, id=None, title=None, value=False, section=None):
        """
        Settings checkbox

        :param window: main window
        :param id: option id
        :param title: option title
        :param value: current value
        :param section: settings section
        """
        super(SettingsCheckbox, self).__init__(window)
        self.window = window
        self.id = id
        self.title = title
        self.value = value
        self.section = section

        self.box = QCheckBox(title, self.window)
        self.box.setChecked(value)
        self.box.stateChanged.connect(
            lambda: self.window.controller.settings.toggle(self.id, self.box.isChecked(), self.section))

        # windows style fix (without this checkboxes are invisible!)
        self.box.setStyleSheet(
            "QCheckBox::indicator:checked { background-color: #1de9b6; } QCheckBox::indicator:unchecked { background-color: #3a3f45; }")

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.box)
        # self.layout.addWidget(self.label)

        self.setLayout(self.layout)


class SettingsInputInline(QLineEdit):
    def __init__(self, window=None, id=None, section=None):
        """
        Settings input inline

        :param window: main window
        :param id: option id
        :param section: settings section
        """
        super(SettingsInputInline, self).__init__(window)
        self.window = window
        self.id = id
        self.section = section
        self.setMaximumWidth(60)

    def keyPressEvent(self, event):
        """
        Key press event

        :param event: key event
        """
        super(SettingsInputInline, self).keyPressEvent(event)
        self.window.controller.settings.apply(self.id, self.text(), 'input', self.section)


class SettingsInput(QLineEdit):
    def __init__(self, window=None, id=None, autoupdate=False, section=None):
        """
        Settings input

        :param window: main window
        :param id: option id
        :param autoupdate: auto update
        :param section: settings section
        """
        super(SettingsInput, self).__init__(window)
        self.window = window
        self.id = id
        self.section = section
        self.autoupdate = autoupdate

    def keyPressEvent(self, event):
        """
        Key press event

        :param event: key event
        """
        super(SettingsInput, self).keyPressEvent(event)
        if not self.autoupdate:
            return
        self.window.controller.ui.update()
        self.window.controller.settings.change(self.id, self.text(), self.section)


class SettingsTextarea(QTextEdit):
    def __init__(self, window=None, id=None, autoupdate=False, section=None):
        """
        Settings input

        :param window: main window
        :param id: option id
        :param autoupdate: auto update
        :param section: settings section
        """
        super(SettingsTextarea, self).__init__(window)
        self.window = window
        self.id = id
        self.section = section
        self.autoupdate = autoupdate

    def keyPressEvent(self, event):
        """
        Key press event

        :param event: key event
        """
        super(SettingsTextarea, self).keyPressEvent(event)
        if not self.autoupdate:
            return
        self.window.controller.ui.update()
        self.window.controller.settings.change(self.id, self.toPlainText(), self.section)


class SettingsDialog(QDialog):
    def __init__(self, window=None, id=None):
        """
        Settings dialog

        :param window: main window
        :param id: settings id
        """
        super(SettingsDialog, self).__init__(window)
        self.window = window
        self.id = id

    def closeEvent(self, event):
        """
        Close event

        :param event: close event
        """
        self.window.settings.active[self.id] = False
        self.window.controller.settings.close(self.id)
        self.window.controller.settings.update()


class EditorDialog(QDialog):
    def __init__(self, window=None, id=None, data_id=None):
        """
        EditorDialog

        :param window: main window
        :param id: configurator id
        :param data_id: data id
        """
        super(EditorDialog, self).__init__(window)
        self.window = window
        self.id = id
        self.data_id = data_id

    def closeEvent(self, event):
        """
        Closes event

        :param event: close event
        """
        pass
        # self.window.settings.active[self.id] = False
        # self.window.controller.settings.close(self.id)
        # self.window.controller.settings.update()


class AlertDialog(QDialog):
    def __init__(self, window=None):
        """
        Alert dialog

        :param window: main window
        """
        super(AlertDialog, self).__init__(window)
        self.window = window
        self.setWindowTitle(trans('alert.title'))

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.message = QPlainTextEdit()
        self.message.setReadOnly(True)
        self.message.setMaximumWidth(400)
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class UpdateDialog(QDialog):
    def __init__(self, window=None):
        """
        Update dialog

        :param window: main window
        """
        super(UpdateDialog, self).__init__(window)
        self.window = window
        self.setParent(window)
        self.setWindowTitle(trans('update.title'))

        download = QPushButton(trans('update.download'))
        download.clicked.connect(
            lambda: self.window.controller.info.goto_update())

        self.changelog = QPlainTextEdit()
        self.changelog.setReadOnly(True)
        self.changelog.setMaximumWidth(400)
        self.changelog.setMaximumHeight(200)

        logo_label = QLabel()
        pixmap = QPixmap('./data/logo.png')
        logo_label.setPixmap(pixmap)

        self.layout = QVBoxLayout()
        self.message = QLabel("")
        info = QLabel(trans("update.info"))
        info.setWordWrap(True)
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("font-weight: bold")
        self.layout.addWidget(logo_label)
        self.layout.addWidget(info)
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.changelog)
        self.layout.addWidget(download)
        self.setLayout(self.layout)


class ConfirmDialog(QDialog):
    def __init__(self, window=None, type=None, id=None):
        """
        Confirm dialog

        :param window: main window
        :param type: confirm type
        :param id: confirm id
        """
        super(ConfirmDialog, self).__init__(window)
        self.window = window
        self.type = type
        self.id = id
        self.setWindowTitle(trans('dialog.confirm.title'))

        btn_yes = QPushButton(trans('dialog.confirm.yes'))
        btn_yes.clicked.connect(
            lambda: self.window.controller.confirm.accept(self.type, self.id))

        btn_no = QPushButton(trans('dialog.confirm.no'))
        btn_no.clicked.connect(
            lambda: self.window.controller.confirm.dismiss(self.type, self.id))

        bottom = QHBoxLayout()
        bottom.addWidget(btn_no)
        bottom.addWidget(btn_yes)

        self.layout = QVBoxLayout()
        self.message = QLabel("")
        self.message.setContentsMargins(10, 10, 10, 10)
        self.message.setAlignment(Qt.AlignCenter)
        self.message.setMinimumWidth(400)
        self.layout.addWidget(self.message)
        self.layout.addLayout(bottom)
        self.setLayout(self.layout)


class FileEditorDialog(QDialog):
    def __init__(self, window=None):
        """
        File editor dialog

        :param window: main window
        """
        super(FileEditorDialog, self).__init__(window)
        self.window = window
        self.file = None

    def closeEvent(self, event):
        """
        Close event

        :param event: close event
        """
        self.window.settings.active['editor'] = False
        self.window.controller.settings.close('editor')
        self.window.controller.settings.update()


class GeneratedImageDialog(QDialog):
    def __init__(self, window=None, id=None):
        """
        Image dialog

        :param window: main window
        :param id: info window id
        """
        super(GeneratedImageDialog, self).__init__(window)
        self.window = window
        self.id = id


class GeneratedImageLabel(QLabel):
    def __init__(self, window=None, path=None):
        """
        Presets select menu

        :param window: main window
        :param path: image path
        """
        super(GeneratedImageLabel, self).__init__(window)
        self.window = window
        self.path = path

    def contextMenuEvent(self, event):
        """
        Context menu event

        :param event: context menu event
        """
        actions = {}
        actions['open'] = QAction(QIcon.fromTheme("view-fullscreen"), trans('img.action.open'), self)
        actions['open'].triggered.connect(
            lambda: self.action_open(event))

        actions['open_dir'] = QAction(QIcon.fromTheme("system-file-manager"), trans('img.action.open_dir'), self)
        actions['open_dir'].triggered.connect(
            lambda: self.action_open_dir(event))

        actions['save'] = QAction(QIcon.fromTheme("document-save"), trans('img.action.save'), self)
        actions['save'].triggered.connect(
            lambda: self.action_save(event))

        actions['delete'] = QAction(QIcon.fromTheme("edit-delete"), trans('img.action.delete'), self)
        actions['delete'].triggered.connect(
            lambda: self.action_delete(event))

        menu = QMenu(self)
        menu.addAction(actions['open'])
        menu.addAction(actions['open_dir'])
        menu.addAction(actions['save'])
        menu.addAction(actions['delete'])

        menu.exec_(event.globalPos())

    def action_open(self, event):
        """
        Open action handler

        :param event: mouse event
        """
        self.window.controller.image.img_action_open(self.path)

    def action_open_dir(self, event):
        """
        Open dir action handler

        :param event: mouse event
        """
        self.window.controller.image.img_action_open_dir(self.path)

    def action_save(self, event):
        """
        Save action handler

        :param event: mouse event
        """
        self.window.controller.image.img_action_save(self.path)

    def action_delete(self, event):
        """
        Delete action handler

        :param event: mouse event
        """
        self.window.controller.image.img_action_delete(self.path)
