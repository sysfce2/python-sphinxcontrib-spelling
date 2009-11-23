# -*- coding: utf-8 -*-
"""
    test_build
    ~~~~~~~~~~

    Test the entire build process with the test root.

    :copyright: Copyright 2007-2009 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import os
import re
import sys
import difflib
import htmlentitydefs
from StringIO import StringIO

from tests.util import test_root, raises, raises_msg, Struct,\
  ListOutput, TestApp, with_app, gen_with_app, path, with_tempdir,\
  write_file, sprint

import feedparser

import nose.tools

def teardown_module():
    (test_root / '_build').rmtree(True)

feed_warnfile = StringIO()

ENV_WARNINGS = ""
# """\
# %(root)s/includes.txt:4: WARNING: download file not readable: nonexisting.png
# """

FEED_WARNINGS = ENV_WARNINGS + ""
# """\
# %(root)s/images.txt:20: WARNING: no matching candidate for image URI u'foo.*'
# """

@gen_with_app(buildername='html', warning=feed_warnfile, cleanenv=True,
              tags=['testtag'])
def test_feed(app):
    app.builder.build_all()
    feed_warnings = feed_warnfile.getvalue().replace(os.sep, '/')
    feed_warnings_exp = FEED_WARNINGS % {'root': app.srcdir}
    assert feed_warnings == feed_warnings_exp, 'Warnings don\'t match:\n' + \
           '\n'.join(difflib.ndiff(feed_warnings_exp.splitlines(),
                                   feed_warnings.splitlines()))
    
    # see http://www.feedparser.org/
    f = feedparser.parse(os.path.join(app.outdir, 'rss.xml'))
    entries = f.entries
    assert entries[0].updated_parsed == (2001, 8, 11)
    assert entries[0].title == "The latest blog post"
    assert entries[1].updated_parsed == (2001, 8, 1)
    assert entries[1].title == "An older blog post"
    assert entries[2].updated_parsed == (1979, 1, 1)
    assert entries[2].title == "The oldest blog post"

