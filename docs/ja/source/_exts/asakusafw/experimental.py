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

    asakusafw.experimental
    ~~~~~~~~~~~~~~~~~~~~~~

    Allow the directives indicating that it is an experimental feature to be inserted into your documentation.

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


class experimental_node(nodes.Admonition, nodes.Element):
    pass


class experimentallist(nodes.General, nodes.Element):
    pass


class Experimental(BaseAdmonition):
    """
    A experimental entry, displayed (if configured) in the form of an admonition.
    """

    node_class = experimental_node
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
            self.options['class'] = ['experimental']

        (experimental,) = super(Experimental, self).run()
        if isinstance(experimental, nodes.system_message):
            return [experimental]

        experimental.insert(0, nodes.title(text=_('Experimental')))
        set_source_info(self, experimental)

        env = self.state.document.settings.env
        targetid = 'index-%s' % env.new_serialno('index')
        # Stash the target to be retrieved later in latex_visit_experimental_node.
        experimental['targetref'] = '%s:%s' % (env.docname, targetid)
        targetnode = nodes.target('', '', ids=[targetid])
        return [targetnode, experimental]


def process_experimentals(app, doctree):
    # type: (Sphinx, nodes.Node) -> None
    # collect all experimentals in the environment
    # this is not done in the directive itself because it some transformations
    # must have already been run, e.g. substitutions
    env = app.builder.env
    if not hasattr(env, 'experimental_all_experimentals'):
        env.experimental_all_experimentals = []  # type: ignore
    for node in doctree.traverse(experimental_node):
        app.emit('experimental-defined', node)

        try:
            targetnode = node.parent[node.parent.index(node) - 1]
            if not isinstance(targetnode, nodes.target):
                raise IndexError
        except IndexError:
            targetnode = None
        newnode = node.deepcopy()
        del newnode['ids']
        env.experimental_all_experimentals.append({  # type: ignore
            'docname': env.docname,
            'source': node.source or env.doc2path(env.docname),
            'lineno': node.line,
            'experimental': newnode,
            'target': targetnode,
        })


class ExperimentalList(Directive):
    """
    A list of all experimental entries.
    """

    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}  # type: Dict

    def run(self):
        # type: () -> List[experimentallist]
        # Simply insert an empty experimentallist node which will be replaced later
        # when process_experimental_nodes is called
        return [experimentallist('')]


def process_experimental_nodes(app, doctree, fromdocname):
    # type: (Sphinx, nodes.Node, unicode) -> None
    if not app.config['experimental_include_experimentals']:
        for node in doctree.traverse(experimental_node):
            node.parent.remove(node)

    # Replace all experimentallist nodes with a list of the collected experimentals.
    # Augment each experimental with a backlink to the original location.
    env = app.builder.env

    if not hasattr(env, 'experimental_all_experimentals'):
        env.experimental_all_experimentals = []  # type: ignore

    for node in doctree.traverse(experimentallist):
        if node.get('ids'):
            content = [nodes.target()]
        else:
            content = []

        if not app.config['experimental_include_experimentals']:
            node.replace_self(content)
            continue

        for experimental_info in env.experimental_all_experimentals:  # type: ignore
            para = nodes.paragraph(classes=['experimental-source'])
            if app.config['experimental_link_only']:
                description = _('<<original entry>>')
            else:
                description = (
                    _('(The <<original entry>> is located in %s, line %d.)') %
                    (experimental_info['source'], experimental_info['lineno'])
                )
            desc1 = description[:description.find('<<')]
            desc2 = description[description.find('>>') + 2:]
            para += nodes.Text(desc1, desc1)

            # Create a reference
            newnode = nodes.reference('', '', internal=True)
            innernode = nodes.emphasis(_(u'記述箇所'), _(u'記述箇所'))
            try:
                newnode['refuri'] = app.builder.get_relative_uri(
                    fromdocname, experimental_info['docname'])
                newnode['refuri'] += '#' + experimental_info['target']['refid']
            except NoUri:
                # ignore if no URI can be determined, e.g. for LaTeX output
                pass
            newnode.append(innernode)
            para += newnode
            para += nodes.Text(desc2, desc2)

            experimental_entry = experimental_info['experimental']
            # Remove targetref from the (copied) node to avoid emitting a
            # duplicate label of the original entry when we walk this node.
            del experimental_entry['targetref']

            # (Recursively) resolve references in the experimental content
            env.resolve_references(experimental_entry, experimental_info['docname'],
                                   app.builder)

            # Insert into the experimentallist
            content.append(experimental_entry)
            content.append(para)

        node.replace_self(content)


def purge_experimentals(app, env, docname):
    # type: (Sphinx, BuildEnvironment, unicode) -> None
    if not hasattr(env, 'experimental_all_experimentals'):
        return
    env.experimental_all_experimentals = [experimental for experimental in env.experimental_all_experimentals
                                          if experimental['docname'] != docname]


def merge_info(app, env, docnames, other):
    # type: (Sphinx, BuildEnvironment, Iterable[unicode], BuildEnvironment) -> None
    if not hasattr(other, 'experimental_all_experimentals'):
        return
    if not hasattr(env, 'experimental_all_experimentals'):
        env.experimental_all_experimentals = []  # type: ignore
    env.experimental_all_experimentals.extend(other.experimental_all_experimentals)  # type: ignore


def visit_experimental_node(self, node):
    # type: (nodes.NodeVisitor, experimental_node) -> None
    self.visit_admonition(node)
    # self.visit_admonition(node, 'experimental')


def depart_experimental_node(self, node):
    # type: (nodes.NodeVisitor, experimental_node) -> None
    self.depart_admonition(node)


def latex_visit_experimental_node(self, node):
    # type: (nodes.NodeVisitor, experimental_node) -> None
    title = node.pop(0).astext().translate(tex_escape_map)
    self.body.append(u'\n\\begin{sphinxadmonition}{note}{')
    # If this is the original experimental node, emit a label that will be referenced by
    # a hyperref in the experimentallist.
    target = node.get('targetref')
    if target is not None:
        self.body.append(u'\\label{%s}' % target)
    self.body.append('%s:}' % title)


def latex_depart_experimental_node(self, node):
    # type: (nodes.NodeVisitor, experimental_node) -> None
    self.body.append('\\end{sphinxadmonition}\n')


def setup(app):
    # type: (Sphinx) -> Dict[unicode, Any]
    app.add_event('experimental-defined')
    app.add_config_value('experimental_include_experimentals', False, 'html')
    app.add_config_value('experimental_link_only', False, 'html')

    app.add_node(experimentallist)
    app.add_node(experimental_node,
                 html=(visit_experimental_node, depart_experimental_node),
                 latex=(latex_visit_experimental_node, latex_depart_experimental_node),
                 text=(visit_experimental_node, depart_experimental_node),
                 man=(visit_experimental_node, depart_experimental_node),
                 texinfo=(visit_experimental_node, depart_experimental_node))

    app.add_directive('experimental', Experimental)
    app.add_directive('experimentallist', ExperimentalList)
    app.connect('doctree-read', process_experimentals)
    app.connect('doctree-resolved', process_experimental_nodes)
    app.connect('env-purge-doc', purge_experimentals)
    app.connect('env-merge-info', merge_info)
    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}
