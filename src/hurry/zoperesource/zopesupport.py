from zope.interface import implements
from zope.component import adapter
from zope.publisher.interfaces import IEndRequestEvent
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.traversing.interfaces import ITraversable

import fanstatic

@adapter(IEndRequestEvent)
def set_base_url_on_needed_inclusions(event):
    needed = fanstatic.get_current_needed_inclusions()
    if not needed.base_url:
        needed.base_url = absoluteURL(None, event.request)

class HurryResource(object):

    # Hack to get ++resource++foo/bar/baz.jpg paths working in Zope
    # Pagetemplates.

    implements(ITraversable, IAbsoluteURL)

    def __init__(self, request, library, name=''):
        self.request = request
        self.library = library
        self.name = name

    def traverse(self, name, furtherPath):
        name = '%s/%s' % (self.name, name)
        # XXX check whether the request resource actually exists and
        # warn if not.
        return HurryResource(self.request, self.library, name=name)

    def __str__(self):
        needed = fanstatic.get_current_needed_inclusions()
        if not needed.base_url:
            needed.base_url = absoluteURL(None, self.request)
        return needed.library_url(self.library) + self.name
