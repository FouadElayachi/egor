import sys

from knack.log import get_logger

from .checker import BasicChecker

logger = get_logger(__name__)


class Step:
    """
    An abstraction representing a phase, in a multi-phase process
    """

    def __init__(self):
        self.next_step = None

    def execute(self, execution_context):
        raise NotImplementedError()

    def name(self):
        raise NotImplementedError()


class ExecutionPipeline:
    """
    An assembly of steps in one single class, the execution order matters
    """

    def __init__(self, steps):
        if steps is None:
            steps = []
        self.steps = steps

    def execute(self, execution_context):
        for step in self.steps:
            try:
                execution_context = step.execute(execution_context)
            except:
                logger.error("Could not execute step {} {}".format(
                    step.name(), sys.exc_info()))
                break


class CompileStep(Step):
    """
    Compile the source code and report any errors back to the user
    """

    def execute(self, execution_context):
        raise NotImplementedError()

    def name(self):
        return "Compile step"


class RunStep(Step):

    def execute(self, execution_context):
        raise NotImplementedError()

    def name(self):
        return "Run step"


class CleanupStep(Step):
    """
    doing any necessary cleanup, such as removing working directories, and binary files ...
    """

    def execute(self, execution_context):
        raise NotImplementedError()

    def name(self):
        return "Cleanup step"


class TestingStep(Step):
    """
        Testing the contents of the output file
    """

    def execute(self, execution_context):
        checker = BasicChecker()
        report = checker.check(execution_context)
        print('rapprot {}'.format(report))
        return execution_context

    def name(self):
        return "Testing step"
