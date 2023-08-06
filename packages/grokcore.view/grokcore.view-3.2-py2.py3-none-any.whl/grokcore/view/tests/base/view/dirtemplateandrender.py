"""
A View may either have an associated template or a render-method. Here
we check that this also works for templates in a template-directory:

  # PY2 - remove '+IGNORE_EXCEPTION_DETAIL'  when dropping Python 2 support:
  >>> grok.testing.grok(__name__)  # doctest: +IGNORE_EXCEPTION_DETAIL
  Traceback (most recent call last):
    ...
  zope.configuration.config.ConfigurationExecutionError:\
  martian.error.GrokError: Multiple possible ways to render view\
  <class 'grokcore.view.tests.base.view.dirtemplateandrender.CavePainting'>.\
  It has both a 'render' method as well as an associated template.

"""
import grokcore.view as grok


class Mammoth(grok.Context):
    pass


class CavePainting(grok.View):
    def render(self):
        pass
