from docutils import nodes

def html_page_context(app, pagename, templatename, context, doctree):
    env = app.builder.env

    # toc looks like this:

    # <compact_paragraph toctree="True">
    # ..<bullet_list>
    # ....<list_item classes="toctree-l1">
    # ......<compact_paragraph classes="toctree-l1">
    # ........<reference anchorname="" internal="True" refuri="about/index.html">
    # ..........About
    # ........</reference>
    # ......</compact_paragraph>
    # ....</list_item>

    # etc; go through and add text inside the <reference>

    def render_toctree(**kwargs):
        collapse = kwargs.pop('collapse', True)
        toc = env.get_toctree_for(pagename, app.builder, collapse, **kwargs)
        for bullet_list in toc.children:
            for list_item in bullet_list.children:
                for para in list_item.children:
                    for reference in para.children:
                        assert reference.tagname == 'reference'
                        refuri = reference['refuri']
                        for name, metadata in env.metadata.iteritems():
                            #html_name = app.builder.get_target_uri(name)
                            #html_name = context['pathto'](name, )
                            html_name = app.builder.get_relative_uri(
                                from_=pagename,
                                to=name,
                                )
                            if html_name != refuri:
                                continue
                            description = metadata.get('customtoc-description')
                            if description is None:
                                continue
                            reference.append(
                                nodes.paragraph(text=description),
                                )
        r = app.builder.render_partial(toc)['fragment']
        return r

    context['toctree'] = render_toctree

def setup(Sphinx):
    Sphinx.connect('html-page-context', html_page_context)
