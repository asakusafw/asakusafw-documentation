# -*- coding: utf-8 -*-
"""
    Copyright 2011-2019 Asakusa Framework Team.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    asakusafw.deprecated
    ~~~~~~~~~~~~~~~~~~~~

    Allow the directives indicating that it is an deperated feature to be inserted into your documentation.

    This plugin based on ``sphinx.ext.todo``.

"""

from docutils import nodes
from docutils.parsers.rst import directives

import sphinx
from sphinx.locale import _
from sphinx.environment import NoUri
from sphinx.util import logging
from sphinx.util.nodes import set_source_info
from sphinx.util.texescape import tex_escape_map
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives.admonitions import BaseAdmonition

if False:
    # For type annotation
    from typing import Any, Dict, Iterable, List  # NOQA
    from sphinx.application import Sphinx  # NOQA
    from sphinx.environment import BuildEnvironment  # NOQA

logger = logging.getLogger(__name__)


class deprecated_node(nodes.Admonition, nodes.Element):
    pass


class deprecatedlist(nodes.General, nodes.Element):
    pass


class Deprecated(BaseAdmonition):
    """
    A deprecated entry, displayed (if configured) in the form of an admonition.
    """

    node_class = deprecated_node
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'class': directives.class_option,
    }

    def run(self):
        # type: () -> List[nodes.Node]
        if not self.options.get('class'):
            self.options['class'] = ['deprecated']

        (deprecated,) = super(Deprecated, self).run()
        if isinstance(deprecated, nodes.system_message):
            return [deprecated]

        deprecated.insert(0, nodes.title(text=_('Deprecated')))
        set_source_info(self, deprecated)

        env = self.state.document.settings.env
        targetid = 'index-%s' % env.new_serialno('index')
        # Stash the target to be retrieved later in latex_visit_deprecated_node.
        deprecated['targetref'] = '%s:%s' % (env.docname, targetid)
        targetnode = nodes.target('', '', ids=[targetid])
        return [targetnode, deprecated]


def process_deprecateds(app, doctree):
    # type: (Sphinx, nodes.Node) -> None
    # collect all deprecateds in the environment
    # this is not done in the directive itself because it some transformations
    # must have already been run, e.g. substitutions
    env = app.builder.env
    if not hasattr(env, 'deprecated_all_deprecateds'):
        env.deprecated_all_deprecateds = []  # type: ignore
    for node in doctree.traverse(deprecated_node):
        app.emit('deprecated-defined', node)

        try:
            targetnode = node.parent[node.parent.index(node) - 1]
            if not isinstance(targetnode, nodes.target):
                raise IndexError
        except IndexError:
            targetnode = None
        newnode = node.deepcopy()
        del newnode['ids']
        env.deprecated_all_deprecateds.append({  # type: ignore
            'docname': env.docname,
            'source': node.source or env.doc2path(env.docname),
            'lineno': node.line,
            'deprecated': newnode,
            'target': targetnode,
        })


class DeprecatedList(Directive):
    """
    A list of all deprecated entries.
    """

    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}  # type: Dict

    def run(self):
        # type: () -> List[deprecatedlist]
        # Simply insert an empty deprecatedlist node which will be replaced later
        # when process_deprecated_nodes is called
        return [deprecatedlist('')]


def process_deprecated_nodes(app, doctree, fromdocname):
    # type: (Sphinx, nodes.Node, unicode) -> None
    if not app.config['deprecated_include_deprecateds']:
        for node in doctree.traverse(deprecated_node):
            node.parent.remove(node)

    # Replace all deprecatedlist nodes with a list of the collected deprecateds.
    # Augment each deprecated with a backlink to the original location.
    env = app.builder.env

    if not hasattr(env, 'deprecated_all_deprecateds'):
        env.deprecated_all_deprecateds = []  # type: ignore

    for node in doctree.traverse(deprecatedlist):
        if node.get('ids'):
            content = [nodes.target()]
        else:
            content = []

        if not app.config['deprecated_include_deprecateds']:
            node.replace_self(content)
            continue

        for deprecated_info in env.deprecated_all_deprecateds:  # type: ignore
            para = nodes.paragraph(classes=['deprecated-source'])
            if app.config['deprecated_link_only']:
                description = _('<<original entry>>')
            else:
                description = (
                    _('(The <<original entry>> is located in %s, line %d.)') %
                    (deprecated_info['source'], deprecated_info['lineno'])
                )
            desc1 = description[:description.find('<<')]
            desc2 = description[description.find('>>') + 2:]
            para += nodes.Text(desc1, desc1)

            # Create a reference
            newnode = nodes.reference('', '', internal=True)
            innernode = nodes.emphasis(_(u'記述箇所'), _(u'記述箇所'))
            try:
                newnode['refuri'] = app.builder.get_relative_uri(
                    fromdocname, deprecated_info['docname'])
                newnode['refuri'] += '#' + deprecated_info['target']['refid']
            except NoUri:
                # ignore if no URI can be determined, e.g. for LaTeX output
                pass
            newnode.append(innernode)
            para += newnode
            para += nodes.Text(desc2, desc2)

            deprecated_entry = deprecated_info['deprecated']
            # Remove targetref from the (copied) node to avoid emitting a
            # duplicate label of the original entry when we walk this node.
            del deprecated_entry['targetref']

            # (Recursively) resolve references in the deprecated content
            env.resolve_references(deprecated_entry, deprecated_info['docname'],
                                   app.builder)

            # Insert into the deprecatedlist
            content.append(deprecated_entry)
            content.append(para)

        node.replace_self(content)


def purge_deprecateds(app, env, docname):
    # type: (Sphinx, BuildEnvironment, unicode) -> None
    if not hasattr(env, 'deprecated_all_deprecateds'):
        return
    env.deprecated_all_deprecateds = [deprecated for deprecated in env.deprecated_all_deprecateds
                                      if deprecated['docname'] != docname]


def merge_info(app, env, docnames, other):
    # type: (Sphinx, BuildEnvironment, Iterable[unicode], BuildEnvironment) -> None
    if not hasattr(other, 'deprecated_all_deprecateds'):
        return
    if not hasattr(env, 'deprecated_all_deprecateds'):
        env.deprecated_all_deprecateds = []  # type: ignore
    env.deprecated_all_deprecateds.extend(other.deprecated_all_deprecateds)  # type: ignore


def visit_deprecated_node(self, node):
    # type: (nodes.NodeVisitor, deprecated_node) -> None
    self.visit_admonition(node)
    # self.visit_admonition(node, 'deprecated')


def depart_deprecated_node(self, node):
    # type: (nodes.NodeVisitor, deprecated_node) -> None
    self.depart_admonition(node)


def latex_visit_deprecated_node(self, node):
    # type: (nodes.NodeVisitor, deprecated_node) -> None
    title = node.pop(0).astext().translate(tex_escape_map)
    self.body.append(u'\n\\begin{sphinxadmonition}{note}{')
    # If this is the original deprecated node, emit a label that will be referenced by
    # a hyperref in the deprecatedlist.
    target = node.get('targetref')
    if target is not None:
        self.body.append(u'\\label{%s}' % target)
    self.body.append('%s:}' % title)


def latex_depart_deprecated_node(self, node):
    # type: (nodes.NodeVisitor, deprecated_node) -> None
    self.body.append('\\end{sphinxadmonition}\n')


def setup(app):
    # type: (Sphinx) -> Dict[unicode, Any]
    app.add_event('deprecated-defined')
    app.add_config_value('deprecated_include_deprecateds', False, 'html')
    app.add_config_value('deprecated_link_only', False, 'html')

    app.add_node(deprecatedlist)
    app.add_node(deprecated_node,
                 html=(visit_deprecated_node, depart_deprecated_node),
                 latex=(latex_visit_deprecated_node, latex_depart_deprecated_node),
                 text=(visit_deprecated_node, depart_deprecated_node),
                 man=(visit_deprecated_node, depart_deprecated_node),
                 texinfo=(visit_deprecated_node, depart_deprecated_node))

    app.add_directive('deprecated', Deprecated)
    app.add_directive('deprecatedlist', DeprecatedList)
    app.connect('doctree-read', process_deprecateds)
    app.connect('doctree-resolved', process_deprecated_nodes)
    app.connect('env-purge-doc', purge_deprecateds)
    app.connect('env-merge-info', merge_info)
    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}
