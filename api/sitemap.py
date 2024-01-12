class View:

    def __init__(self, url, name, parent):
        self.url = url
        self.name = name
        self.parent = parent

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value


home = View('index', 'Home', None)
project = View('project', 'Project', home)
user_stories = View('user_stories', 'User stories', project)
requirements = View('requirements', 'Requirements', project)
design = View('design', 'Design', project)
code = View('code', 'Code', project)
tests = View('tests', 'Tests', project)
traceability = View('traceability', 'Traceability', project)
urls = {
    '/': home,
    'project': project,
    'user_stories': user_stories,
    'requirements': requirements,
    'design': design,
    'code': code,
    'tests': tests,
    'traceability': traceability,
    'tests_applications': tests,
}


def resolve(url):
    view = urls.get(url)
    if not view:
        view = urls.get('/')
    crumbs = [{
        'label': view.name,
        'url': view.url,
    }]
    while view.parent:
        view = view.parent
        crumbs.append({
            'label': view.name,
            'url': view.url,
        })
    crumbs.reverse()
    return crumbs
