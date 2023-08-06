"""
It is too confusing to have a template that would be implicitly
associated with a view while that view already refers to another
template using grok.template.  Therefore there is an error:

  # PY2 - remove '+IGNORE_EXCEPTION_DETAIL'  when dropping Python 2 support:
  >>> grok.testing.grok(__name__)  # doctest: +IGNORE_EXCEPTION_DETAIL
  Traceback (most recent call last):
    ...
  zope.configuration.config.ConfigurationExecutionError:\
  martian.error.GrokError: Multiple possible templates for view\
  <class 'grokcore.view.tests.base.view.explicitimplicittemplate.Painting'>.\
  It uses grok.template('cavepainting'), but there is also a template\
  called 'painting'.

"""
import grokcore.view as grok


class Mammoth(grok.Context):
    pass


class Painting(grok.View):
    grok.template('cavepainting')


cavepainting = grok.PageTemplate("GROK CAVEPAINT MAMMOTH!")
painting = grok.PageTemplate("GROK PAINT MAMMOTH!")
