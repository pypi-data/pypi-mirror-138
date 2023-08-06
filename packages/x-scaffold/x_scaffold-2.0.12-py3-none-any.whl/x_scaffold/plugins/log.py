from charset_normalizer import logging
from x_scaffold.context import ScaffoldContext
from ..runtime import ScaffoldRuntime
from ..steps import ScaffoldStep
from ..plugin import ScaffoldPluginContext
from ..rendering import render_text


_log = logging.getLogger(__name__)


def init(context: ScaffoldPluginContext):
    context.add_step('log', LogStep())
    context.add_step('debug', DebugStep())


class LogStep(ScaffoldStep):
    # def resolve_fn(self, obj_name, fn_name, context):
    #     return getattr(_log, fn_name), False

    def run(self, context: ScaffoldContext, step: dict, runtime: ScaffoldRuntime):
        message = render_text(step, context)
        _log.info(message)


class DebugStep(ScaffoldStep):
    def run(self, context: ScaffoldContext, step: dict, runtime: ScaffoldRuntime):
        message = render_text(step, context)
        _log.debug(message)
