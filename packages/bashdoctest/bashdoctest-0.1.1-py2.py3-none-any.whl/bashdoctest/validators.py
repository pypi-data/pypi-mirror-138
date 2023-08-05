import traceback
import doctest
import subprocess
from click.testing import CliRunner


class CommandValidator(object):

    def __init__(self, options=0):
        super(CommandValidator, self).__init__()
        self.options = options | doctest.REPORT_NDIFF

    def validate(self, command, args, expected, options):

        stdout, stderr = self.run_command(command, args)

        checker = doctest.OutputChecker()

        options = self.options | options
        if checker.check_output(
                expected.rstrip(),
                stdout.rstrip() + stderr.rstrip(),
                options):
            return

        self.want = expected.rstrip()
        msg = checker.output_difference(
            self,
            stdout.rstrip() + stderr.rstrip(),
            options)

        raise ValueError(msg)


class ClickValidator(CommandValidator):

    def __init__(self, app, prefix=None, options=0):
        super(ClickValidator, self).__init__(options)

        self.app = app

        if prefix is None:
            prefix = []

        self.prefix = prefix

    def run_command(self, command, args):

        runner = CliRunner()

        result = runner.invoke(self.app, self.prefix + args)

        if result.exit_code and not isinstance(result.exc_info[1], SystemExit):
            tb = ''.join(traceback.format_exception(*result.exc_info))
        else:
            tb = ''

        return result.output, tb


class SkipValidator(CommandValidator):

    def __init__(self):
        super(SkipValidator, self).__init__()

    def validate(self, command, args, expected, options):
        pass


class SubprocessValidator(CommandValidator):

    def __init__(self, options=0):
        super(SubprocessValidator, self).__init__(options)

    def run_command(self, command, args):

        p = subprocess.Popen(
            [command] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        return tuple(map(lambda s: s.decode('utf-8'), p.communicate()))
