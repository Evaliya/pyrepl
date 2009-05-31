
# Copyright 2009 Mark Seaborn <mrs@mythic-beasts.com>
#
# Permission to use, copy, modify, and distribute this software and
# its documentation for any purpose is hereby granted without fee,
# provided that the above copyright notice appear in all copies and
# that both that copyright notice and this permission notice appear in
# supporting documentation.
#
# THE AUTHOR MICHAEL HUDSON DISCLAIMS ALL WARRANTIES WITH REGARD TO
# THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
# INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER
# RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF
# CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import unittest

import pyrepl.reader
import pyrepl.unix_console


class TestWrappingLongLines(unittest.TestCase):

    def test_wrapping(self):
        console = pyrepl.unix_console.UnixConsole()
        reader = pyrepl.reader.Reader(console)
        reader.ps1 = "foo$"
        reader.prepare()
        reader.restore() # Don't screw up terminal
        console.width = 10
        reader.buffer = list("01234567890123456789")
        lines = reader.calc_screen()
        self.assertEquals(lines,
                          ["foo$01234\\", "567890123\\", "456789"])
        for line in lines[:-1]:
            self.assertEquals(len(line), console.width)
        # Check cursor position consistency.
        for index, char in enumerate("".join(reader.buffer)):
            x, y = reader.pos2xy(index)
            self.assertEquals(lines[y][x], char)


if __name__ == "__main__":
    unittest.main()