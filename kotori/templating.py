# -*- coding: utf-8 -*-
"""
:Author: Juti Noppornpitak

This package is used for rendering.

.. note::

    Originally implemented for Tori Framework (version 2.0 and higher).

"""

import os
import re

from jinja2 import Environment, FileSystemLoader, PackageLoader

class Renderer(object):
    """ The default renderer with Jinja2

        :param `referers`: the template module path (e.g., com.shiroyuki.view)
                            or multiple folders of Jinja templates based on the
                            current working directory.

        For example::

            # Refer to the module os.path.
            renderer = Renderer('app.views')

            # Refer to multiple folders of Jinja templates.
            renderer = Renderer(['/opt/app/ui/template', '/usr/local/tori/module/template'])

    """
    def __init__(self, referer, *engine_largs, **engine_kwargs):
        if len(referers) == 0:
            raise RendererSetupError('Require either one resource module or multiple file paths to the templates.')

        self.referers = referers

        self._loader = None
        self._engine = None

        self._engine_largs  = engine_largs
        self._engine_kwargs = engine_kwargs

    @property
    def loader(self):
        if not self._loader:
            self._loader = self._get_filesystem_loader() \
                if   isinstance(self.referers, list) \
                else self._get_package_loader()

        return self._loader

    @property
    def engine(self):
        if not self._engine:
            self._engine_kwargs.update({
                'loader':     self.loader,
                'extensions': [
                    'jinja2.ext.do',
                    'jinja2.ext.i18n',
                    'jinja2.ext.loopcontrols',
                    'jinja2.ext.autoescape',
                ],
            })

            self._engine = Environment(
                *self._engine_largs,
                **self._engine_kwargs
            )

        return self._engine

    def render(self, template_path, **contexts):
        """ Render a template with context variables.

            :param str template_path: a path to the template
            :param str contexts: a dictionary of context variables.

            Example::

                renderer = Renderer()
                renderer.render('dummy.html', appname='ikayaki', version=1.0)

        """
        template = self.engine.get_template(template_path)

        return template.render(**contexts)

    def _get_filesystem_loader(self):
        """ Get the file-system loader for the renderer.

            :rtype: FileSystemLoader
        """
        return FileSystemLoader(self.referers)

    def _get_package_loader(self):
        """ Get the package loader for the renderer.

            :rtype: PackageLoader
        """

        module_name_chunks       = self.referers # :type: str
        module_name              = '.'.join(module_name_chunks[:-1])
        template_sub_module_name = module_name_chunks[-1]

        if len(module_name_chunks) <= 1:
            raise RendererSetupError(
                'Could not instantiate the package loader. ({})'.format(
                    '.'.join(module_name_chunks)
                )
            )

        return PackageLoader(module_name, template_sub_module_name)
