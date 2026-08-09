"""Correct what python-docx leaves behind in a delivered .docx.

python-docx stamps docProps/app.xml with <Pages>1</Pages> — and zero words, zero lines —
regardless of the document it just wrote. Word repaginates on open and shows the truth,
but every tool that reads the property instead of opening the file in Word is told the
study is one page long. A delivered file must not declare something false about itself.

The stub is REMOVED rather than replaced with a guess: pagination is a property of the
renderer and the fonts it has, not of the file. Two engines will legitimately disagree.
"""
import os
import re
import shutil
import zipfile

STUB_TAGS = ('Pages', 'Words', 'Characters', 'Lines', 'Paragraphs', 'CharactersWithSpaces')


def strip_stub_counts(path):
    tmp = path + '.tmp'
    with zipfile.ZipFile(path) as zin, \
            zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'docProps/app.xml':
                txt = data.decode('utf8')
                for tag in STUB_TAGS:
                    txt = re.sub(rf'<{tag}>[^<]*</{tag}>', '', txt)
                data = txt.encode('utf8')
            zout.writestr(item, data)
    shutil.move(tmp, path)
    return path
