import subprocess

from jinja2.ext import Extension

try:
    from jinja2 import pass_eval_context as eval_context
except ImportError:
    from jinja2 import evalcontextfilter as eval_context


@eval_context
def shell(eval_ctx, value, die_on_error=False, hide_stderr=True, encoding="utf8"):
    cmd = value
    stderr = subprocess.DEVNULL

    if not die_on_error:
        cmd = "%s ; exit 0" % value
    if not hide_stderr:
        stderr = subprocess.STDOUT

    output = subprocess.check_output(cmd, stderr=stderr, shell=True)
    return output.decode(encoding)


class ShellExtension(Extension):

    def __init__(self, environment):
        super(ShellExtension, self).__init__(environment)
        environment.filters['shell'] = shell
