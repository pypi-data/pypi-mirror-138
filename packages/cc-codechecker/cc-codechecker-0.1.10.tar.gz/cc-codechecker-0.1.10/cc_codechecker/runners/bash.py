"""Bash runner.

Give definitions for runner for Bash projects.
"""
# Standard Library
import subprocess

# Codechecker
from cc_codechecker.runner import Runner


class Bash(Runner): # pragma: no cover
  """Bash runner.

  Support for bash projects.
  """

  def position(self) -> str:
    """Get the bash position.

    Returns:
      str: path to the bash executable.
    """
    args = ['command -v bash']
    bash_pos = subprocess.check_output(
      args,
      encoding='locale',
      shell=True,
      stderr=subprocess.STDOUT,
    )
    if self._locals.verbose:
      print(f'Bash position {bash_pos}')

    return bash_pos

  def version(self) -> str:
    """Get current bash installation.

    Run a check on current system for an installed bash. If bash is not
    installed, Projects targetting this platform could not be executed.
    Using the POSIX standard command *command* make us more cross-platform.
    Look at this page for more info:
    https://pubs.opengroup.org/onlinepubs/9sssssssssssssssss699919799/utilities/command.html.

    Returns:
      str: installed version
    """
    bash_path = self._check_position()
    args = ['echo $BASH_VERSION']
    bash_ver = subprocess.check_output(
      args,
      encoding='locale',
      executable=bash_path,
      shell=True,
      stderr=subprocess.STDOUT,
    )
    if self._locals.verbose:
      print(f'Bash version {bash_ver}')
    return bash_ver.rstrip('\n')

  def run(self, *args, **kwargs) -> tuple[int, str]:
    """Run the bash project.

    Run the project in the bash folder. I don't know if it is shell injection
    prune.

    Returns:
      tuple[int, str]: return code and message.
    """
    bash_path = self._check_position()

    cmd: list[str] = ['./bash/program.sh']
    bash_run = subprocess.run(
      cmd,
      capture_output=True,
      check=False,
      encoding='locale',
      executable=bash_path,
      shell=True, # Is this shell injection prune?
    )

    run_verbose = kwargs['verbose'] \
      if 'verbose' in kwargs \
      else self._locals.verbose
    if run_verbose:
      print(f'Bash run {bash_run}')

    return (bash_run.returncode, bash_run.stdout)

  def _check_position(self) -> str:
    """Find bash executable.

    Raise a Value Error if executable is not found.

    Raises:
      ValueError: Bash executable not installed.

    Returns:
      str: bash executable path.
    """
    bash_path = self.position().rstrip('\n')
    if not bash_path:
      raise ValueError('Bash executable not installed')

    return bash_path
