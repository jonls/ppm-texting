#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs

import pygtk
pygtk.require("2.0")

import gtk

import ppm


class Interface(object):
    def __init__(self, ppm):
        self.builder = gtk.Builder()
        self.builder.add_from_file('ppm.ui')
        self.builder.connect_signals(self, None)

        self._chars = (u'.,?!;:-+_',
                       u'abcæåáàABCÆÅÁÀ',
                       u'deféèDEFÉÈ',
                       u'ghiíìGHIÍÌ',
                       u'jklJKL',
                       u'mnoøóòMNOØÓÒ',
                       u'pqrsPQRS',
                       u'tuvúùTUVÚÙ',
                       u'wxyzýỳWXYZÝỲ')
        self._char_input = None

        self._sequence = None
        self._seq_pos = None

        self._buffer = ''

        self._ppm = ppm

    def _commit(self, c):
        self._ppm.write(c)
        self._buffer += c

    def _reset_sequence(self):
        self._sequence = self._ppm.predict_order(self._chars[self._char_input])
        self._seq_pos = 0
        print u'sequence ' + u''.join(self._sequence)

    def _forward_sequence(self):
        self._seq_pos = (self._seq_pos + 1) % len(self._chars[self._char_input])

    def _rewind_sequence(self):
        self._seq_pos = (self._seq_pos - 1) % len(self._chars[self._char_input])

    def _input_char(self, group):
        if self._char_input == group:
            self._forward_sequence()
        else:
            if self._seq_pos is not None:
                self._commit(self._sequence[self._seq_pos])
            self._char_input = group
            self._reset_sequence()

        self.builder.get_object('text').set_text(self._buffer + self._sequence[self._seq_pos])

    def char_symbol_clicked_cb(self, button, data=None):
        self._input_char(0)

    def char_abc_clicked_cb(self, button, data=None):
        self._input_char(1)

    def char_def_clicked_cb(self, button, data=None):
        self._input_char(2)

    def char_ghi_clicked_cb(self, button, data=None):
        self._input_char(3)

    def char_jkl_clicked_cb(self, button, data=None):
        self._input_char(4)

    def char_mno_clicked_cb(self, button, data=None):
        self._input_char(5)

    def char_pqrs_clicked_cb(self, button, data=None):
        self._input_char(6)

    def char_tuv_clicked_cb(self, button, data=None):
        self._input_char(7)

    def char_wxyz_clicked_cb(self, button, data=None):
        self._input_char(8)

    def next_clicked_cb(self, button, data=None):
        if self._seq_pos is not None:
            self._commit(self._sequence[self._seq_pos])
            self._seq_pos = None
        self._char_input = None

        self.builder.get_object('text').set_text(self._buffer)

    def space_clicked_cb(self, button, data=None):
        if self._seq_pos is not None:
            self._commit(self._sequence[self._seq_pos])
            self._commit(' ')
            self._seq_pos = None
        self._char_input = None

        self.builder.get_object('text').set_text(self._buffer)

    def backspace_clicked_cb(self, button, data=None):
        pass

    def window_delete_event_cb(self, window, event, data=None):
        return False

    def window_destroy_cb(self, window, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()


if __name__ == '__main__':
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = None

    try:
        pred_length = int(sys.argv[2])
    except IndexError:
        pred_length = 2

    ppm = ppm.PPM(pred_length)

    # Train from input file
    if file_name is not None:
        with codecs.open(file_name, 'r', 'utf-8') as f:
            for line in f:
                for c in line:
                    c = c if not c.isspace() else ' '
                    ppm.write(c)
        ppm.clear_context()

    print '{} entries'.format(len(ppm._pred))

    i = Interface(ppm)
    i.main()
