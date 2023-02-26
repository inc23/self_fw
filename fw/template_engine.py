import os
import re

FOR_BLOCK_PATTERN = re.compile(
    r'{% for (?P<variable>[a-zA-Z]+) in (?P<seq>[a-zA-Z]+) %}(?P<content>[\S\s]+)(?={% endblock %}){% endblock %}')
VARIABLE_PATTERN = re.compile(r'{{ (?P<variable>[a-zA-Z_]+) }}')


class Engine:

    def __init__(self, base_dir, template_dir_name):
        self.template_dir_path = os.path.join(base_dir, template_dir_name)

    def _get_template_as_string(self, template_name):
        template_path = os.path.join(self.template_dir_path, template_name)
        if not os.path.isfile(template_path):
            raise Exception('template is not file')
        with open(template_path) as file:
            return file.read()

    def _build_block(self, context, raw_template):
        used_var = VARIABLE_PATTERN.findall(raw_template)
        if used_var is None:
            return raw_template
        for var in used_var:
            var_in_template = '{{ %s }}' % var
            raw_template = re.sub(var_in_template, str(context.get(var, '')), raw_template)
        return raw_template

    def _build_block_for(self, context, raw_template):
        for_block = FOR_BLOCK_PATTERN.search(raw_template)
        if for_block is None:
            return raw_template
        build_block = ''
        for i in context.get(for_block.group('seq'), ''):
            build_block += self._build_block(
                {for_block.group('variable'): i},
                for_block.group('content')
            )
        raw_template = FOR_BLOCK_PATTERN.sub(build_block, raw_template)
        return raw_template

    def build(self, context, template_name):
        template = self._get_template_as_string(template_name)
        template = self._build_block_for(context, template)
        return self._build_block(context, template)


def build_template(request, context, template_name):

    engine = Engine(
        request.settings.get('BASE_DIR'),
        request.settings.get('TEMPLATE_DIR_NAME')
    )

    return engine.build(context, template_name)