# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinxcontrib', 'sphinxcontrib.analyzers']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=1.6,<5.0']

setup_kwargs = {
    'name': 'sphinxcontrib-autoanysrc',
    'version': '0.1.1',
    'description': 'Sphinx extension with some autodoc features for any sources',
    'long_description': 'autoanysrc\n==========\n\n.. attention::\n\n    Currently in early development stage\n\nExtension for gathering reST documentation from any files.\nThis is a documenter_ from ext.autodoc.\n\nIn current state this extension will only insert reST docs from files to\ntarget documentation project without auto generation definitions\nand signatures.\n\nBut it simple and clean to make documentation for API and store documentation\nstrings in the source code.\n\nInstall\n-------\n\n::\n\n    pip install sphinxcontrib-autoanysrc\n\n\nUsage\n-----\n\nAdd autoanysrc to extensions list::\n\n    extensions = [\'sphinxcontrib.autoanysrc\', ]\n\nExample of usage::\n\n    .. autoanysrc:: blabla\n        :src: app/**/*.js\n        :analyzer: js\n\n.. note::\n\n    directive argument \'blabla\' not used now, but it required by autodoc\n    behaviour\n\nWhere:\n\n - `src` option is the pattern to list source files where docs are stored\n - `analyzer` option to determine witch analyzer must be used for\n   processing this files\n\nDirective will iterate over `app/**/*.js` files and process\nit line by line.\n\n\nCustom analyzer\n---------------\n\nautoanysrc allow define custom analyzers.\n\nDefine custom analyzer (conf.py)::\n\n    # make conf.py importtable\n    sys.path.insert(0, os.path.abspath(\'.\'))\n\n    from sphinxcontrib.autoanysrc import analyzers\n\n    class CustomAnalyzer(analyzers.BaseAnalyzer):\n\n        def process(self, content):\n            """\n            Must process content line by line\n\n            :param content: processing file content\n            :returns: generator of pairs docs line and line number\n            """\n            for lineno, srcline in enumerate(content.split(\'\\n\')):\n                yield \'some parsed doc line from content\', lineno\n\n\n    # put analyzer to the autonaysrc setting\n    autoanysrc_analyzers = {\n        \'my-custom\': \'conf.CustomAnalyzer\',\n    }\n\n\nAnd use it::\n\n    .. autoanysrc:: blabla\n        :src: ../src/*.js\n        :analyzer: my-custom\n\n\nDefault analyzers\n-----------------\n\nJSAnalyzer\n``````````\n\nSearch comments blocks starts by `/*"""` and ends by `*/`\n(inspired by `Nuulogic/sphinx-jsapidoc`_).\n\n::\n\n    .. autoanysrc:: directives\n        :src: app/services.js\n        :analyzer: js\n\nWhere services.js::\n\n    /*"""\n    Services\n    ````````\n\n    The function :func:`someService` does a some function.\n    */\n\n    function someService(href, callback, errback) {\n    /*"""\n    .. function:: someService(href, callback[, errback])\n\n        :param string href: An URI to the location of the resource.\n        :param callback: Gets called with the object.\n        :throws SomeError: For whatever reason in that case.\n        :returns: Something.\n    */\n        return \'some result\';\n    };\n\n\nTODO\n----\n\n- encoding option\n- allow internal indent in comment block\n- generate signatures like ext.autodoc...\n\n\n.. _documenter: http://sphinx-doc.org/extdev/appapi.html?highlight=documenter#sphinx.application.Sphinx.add_autodocumenter\n.. _`Nuulogic/sphinx-jsapidoc`: https://github.com/Nuulogic/sphinx-jsapidoc\n',
    'author': 'Evgeniy Tatarkin',
    'author_email': 'tatarkin.evg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sphinx-contrib/autoanysrc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
