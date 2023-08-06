"""
Views either need an associated template or a ``render`` method:

  # PY2 - remove '+IGNORE_EXCEPTION_DETAIL'  when dropping Python 2 support:
  >>> grok.testing.grok(__name__)  # doctest: +IGNORE_EXCEPTION_DETAIL
  Traceback (most recent call last):
    ...
  zope.configuration.config.ConfigurationExecutionError:\
  martian.error.GrokError: View\
  <class 'grokcore.view.tests.base.view.notemplateorrender.CavePainting'>\
  has no associated template or 'render' method.

"""

import grokcore.view as grok


class Mammoth(grok.Context):
    pass


class CavePainting(grok.View):
    pass
