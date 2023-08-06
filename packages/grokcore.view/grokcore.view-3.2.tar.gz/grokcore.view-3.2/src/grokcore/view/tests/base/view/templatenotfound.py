"""
This should fail because ``grok.template`` points to a non-existing
template:

  # PY2 - remove '+IGNORE_EXCEPTION_DETAIL'  when dropping Python 2 support:
  >>> grok.testing.grok(__name__)  # doctest: +IGNORE_EXCEPTION_DETAIL
  Traceback (most recent call last):
    ...
  zope.configuration.config.ConfigurationExecutionError:\
  martian.error.GrokError: Template cavepainting for View\
  <class 'grokcore.view.tests.base.view.templatenotfound.Painting'>\
  cannot be found.
"""
import grokcore.view as grok


class Mammoth(grok.Context):
    pass


class Painting(grok.View):
    grok.template('cavepainting')

# no cavepainting template here
