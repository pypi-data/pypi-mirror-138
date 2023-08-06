"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import enum
import logging
import os
import shutil
import subprocess
import sys
import tempfile
from collections import OrderedDict, defaultdict
from typing import Dict, Iterable, List, Optional, Set, Tuple

import yaml
from pydantic import BaseModel, constr

import irt.module_sources
from inmanta.module import DummyProject, InmantaModuleRequirement
from inmanta.moduletool import Module, ModuleConverter, ModuleTool, ModuleV1, ModuleV2
from irt import util
from irt.git import GitRepo
from irt.project import ProductConfig, ProductProject, PythonVersion
from irt.release import BuildType
from irt.util import Pip

LOGGER = logging.getLogger(__name__)

MODULE_FILE = "module.yml"


@enum.unique
class InstallMode(enum.Enum):
    release = "release"
    prerelease = "prerelease"
    master = "master"


class ModuleSetDefinition(BaseModel):
    """
    :param publish_repo: The (customer facing) repository in cloudsmith where the
                         V2 modules have to be published.
    """

    class Config:
        underscore_attrs_are_private = True

    name: str
    modules: List[
        constr(
            regex=r"^(?P<name>[a-z0-9_]+)(?P<version_constraint>(\s*~=\s*[0-9]+\.[0-9]+(\.[0-9]+)?)?)$"
        )
    ]
    modules_filter: Dict[str, bool] = {}
    exclude: List[str] = []
    module_sources: List[str] = []
    extra_modules: Dict[str, List[str]] = {}

    # This field is not part of the model. Only used internally.
    # Map the name of a module to a version constraint on the corresponding python package
    _module_names_to_version_constraint: Dict[str, InmantaModuleRequirement]
    publish_repo: Optional[str] = None

    def __init__(self, **kwargs):
        super(ModuleSetDefinition, self).__init__(**kwargs)
        self.__set_module_names_to_version_constraint()

    def __set_module_names_to_version_constraint(self) -> None:
        """
        Initialize the _module_names_to_version_constraint variable
        """
        self._module_names_to_version_constraint = {}
        for current_module_requirement in self.modules:
            module_name = current_module_requirement.split("~=")[0]
            req = InmantaModuleRequirement.parse(current_module_requirement)
            if module_name in self._module_names_to_version_constraint:
                raise Exception(
                    f"Module {module_name} occurs more than once in the modules section of the module set file."
                )
            self._module_names_to_version_constraint[module_name] = req

    def get_version_constraint_for(self, module_name: str) -> InmantaModuleRequirement:
        """
        Return the version constraint for the given module defined in the module set file.
        The key of the returned Requirement object contains the name of the corresponding
        Python package and not the name of the module.
        """
        if module_name not in self._module_names_to_version_constraint:
            return InmantaModuleRequirement.parse(module_name)
        return self._module_names_to_version_constraint[module_name]

    def get_module_set(
        self, sources: Dict[str, "irt.module_sources.ModuleData"]
    ) -> Dict[str, "irt.module_sources.ModuleData"]:
        module_set = {}
        excludes_set = set(self.exclude)

        # First find listed modules
        for name in self._module_names_to_version_constraint.keys():
            mod = sources.get(name, None)

            if mod is None:
                LOGGER.error("Unable to find module %s in module sources.", name)
                sys.exit(1)

            if name not in excludes_set:
                module_set[name] = mod

        # helper methods
        def filter_modules(
            sources: Dict[str, "irt.module_sources.ModuleData"],
            filters: Dict[str, bool],
        ) -> Dict[str, "irt.module_sources.ModuleData"]:
            matched = {}
            for module in sources.values():
                if module["name"] not in matched and match(module, filters):
                    matched[module["name"]] = module

            return matched

        def match(
            module: "irt.module_sources.ModuleData", filters: Dict[str, bool]
        ) -> bool:
            for key, value in filters.items():
                if key not in module:
                    return False

                if module[key] != value:
                    return False
            return True

        # Apply filters
        if self.modules_filter:
            mods = filter_modules(sources, self.modules_filter)
            for name, the_mod in mods.items():
                if name not in module_set and name not in excludes_set:
                    module_set[name] = the_mod
        return module_set

    def is_wildcard_module_set(self) -> bool:
        """
        A module set is a wildcard module set iff it can include modules which are not
        explicitly listed in the `modules` section of the module set file. This occurs
        when `modules_filter` are specified.
        """
        return len(self.modules_filter) > 0

    @classmethod
    def from_file(cls, module_set_file: str) -> "ModuleSetDefinition":
        with open(module_set_file) as fd:
            set_def_dct = yaml.safe_load(fd)
            return ModuleSetDefinition(**set_def_dct)

    def get_modules_in_module_set(self) -> List[str]:
        """
        Return the modules in this module set file.
        """
        if not self.is_wildcard_module_set():
            # Returning explicitly listed modules is sufficient
            return [
                mod_name for mod_name in self._module_names_to_version_constraint.keys()
            ]
        raise NotImplementedError(
            "Cannot get modules in module set for a wildcard module set."
        )


def download_set(
    python_path: str,
    set_def: ModuleSetDefinition,
    sources: irt.module_sources.ModuleSourceManager,
    set_dir: str,
    install_mode: InstallMode = InstallMode.release,
    pip_index_url: Optional[str] = None,
    remote: Optional[str] = None,
) -> Dict[str, irt.module_sources.ModuleData]:
    """
    :param python_path: The python path for an environment where the appropriate inmanta product has been installed.
    :param set_def: modules set definition
    :param sources: sources to use to find modules
    :param set_dir: destination folder
    :param pip_index_url: The pip index to use for downloading module's dependencies.
    :param remote: override url for all downloads
    """
    LOGGER.info("Downloading modules in module set %s to %s", set_def.name, set_dir)

    # reduce sources to those in the set definition
    sources = sources.for_sources(set_def.module_sources)
    # list all available modules, from cache or discover
    modules = sources.get_modules()
    # apply the module set to the list of available modules
    modules = set_def.get_module_set(modules)

    LOGGER.info("Attempting to get modules [%s]", ",".join(modules.keys()))

    # remove all existing modules from target directory
    set_dir = os.path.abspath(set_dir)
    if os.path.exists(set_dir):
        shutil.rmtree(set_dir)
    os.makedirs(set_dir)

    tmp_dir: str = tempfile.mkdtemp()
    compiler_venv_dir = os.path.join(tmp_dir, ".env")

    if not remote:
        # Construct a list of remote location based on all known urls, add tokens
        def project_url(
            module_name: str,
            module_url: str,
            token: Optional[str],
            username: Optional[str],
        ) -> str:
            result: str = module_url.replace(f"{module_name}.git", "{}.git")
            return util.add_userinfo_to_url(result, username, token)

        repo_list = list(
            {
                project_url(
                    module["name"],
                    module["url"],
                    module.get("token", None),
                    module.get("username", None),
                )
                for module in modules.values()
            }
        )
    else:
        # override the remote
        if "{}" not in remote and "{0}" not in remote and not remote.endswith("/"):
            # Make sure that remote and with a slash. The module name will be appended
            # at the end by the compiler.
            remote = f"{remote}/"
        repo_list = [remote]

    LOGGER.info("Pulling from sources [%s]", ",".join(repo_list))

    with open(os.path.join(tmp_dir, "project.yml"), "w") as fd:
        project_yaml: Dict[str, object] = {
            "name": "temp-project",
            "modulepath": set_dir,
            "downloadpath": set_dir,
            "repo": repo_list,
            "install_mode": install_mode.value,
            "requires": [constraint for constraint in set_def.modules],
        }
        yaml.dump(project_yaml, fd)
    with open(os.path.join(tmp_dir, "main.cf"), "w") as fd:
        fd.write("\n".join(f"import {name}" for name in modules.keys()))

    # load project from a separate process with the appropriate venv to make sure no version conflicts can arise between the
    # modules' requirements and this project's internal dependencies
    script_path: str = os.path.join(tmp_dir, "load_inmanta_project.py")
    with open(script_path, "w") as fd:
        fd.write(
            f"""
from inmanta.module import Project

import logging
import sys

log_level = logging.DEBUG
log = logging.getLogger()
log.setLevel(log_level)
stream = logging.StreamHandler(sys.stdout)
stream.setLevel(log_level)
log.addHandler(stream)
logging.captureWarnings(True)

try:
  # 1. modules V2 requires explicit install
  # 2. Use a separate venv for the compiler to make sure that the inmanta product installed in python_path is not overridden.
  Project("{tmp_dir}", autostd=False, venv_path="{compiler_venv_dir}").load(install=True)
except TypeError:
  # We are running on an old version of inmanta-core that doesn't support V2 modules and still creates
  # a separate compiler venv by default.
  Project("{tmp_dir}", autostd=False).load()
            """.strip()
        )

    try:
        # download modules
        util.subprocess_log(
            subprocess.check_call,
            [python_path, script_path],
            logger=LOGGER,
            env={**os.environ, "PIP_INDEX_URL": pip_index_url}
            if pip_index_url is not None
            else None,
        )
        # Verify module set completeness.
        # Doing this in a test case is not sufficient because modules might get updated at any time.
        downloaded: Set[str] = set(os.listdir(set_dir))
        provided: Set[str] = set(modules.keys())
        if downloaded != provided:
            LOGGER.exception(
                "Incomplete module set. One or more modules in the set have a dependency on modules not in the set: %s",
                downloaded.difference(provided),
            )
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        LOGGER.exception(str(e))
        sys.exit(1)
    finally:
        shutil.rmtree(tmp_dir)
    return modules


def load_modules(
    module_set: str, source_dir: str
) -> Tuple[
    ModuleSetDefinition,
    Dict[str, irt.module_sources.ModuleData],
    Dict[str, irt.module_sources.ModuleSourceFile],
]:
    """
    Parses the module_set file and returns a tuple of the parsed object, the actual module data objects and the sources
    objects.

    to be phased out
    """
    set_def = ModuleSetDefinition.from_file(module_set)

    # Load module sources
    sources: Dict[str, irt.module_sources.ModuleSourceFile] = OrderedDict()
    for ms in set_def.module_sources:
        ms_file = os.path.join(source_dir, ms + ".yml")
        if not os.path.exists(ms_file):
            LOGGER.error(
                "Unable to find module source file %s (%s does not exist)."
                " Perhaps you should load it with `irt github-list` or `irt gitlab-list`.",
                ms,
                ms_file,
            )
            sys.exit(1)

        with open(ms_file, "r") as fd:
            sources[ms] = yaml.safe_load(fd)

    return (
        set_def,
        set_def.get_module_set(
            {
                module["name"]: module
                for source in sources.values()
                for module in source["modules"].values()
            }
        ),
        sources,
    )


class PythonEnvironment:
    """
    Class representing a Python (virtual) environment.
    """

    def __init__(self, python_path: str, build_type: BuildType) -> None:
        self.python_path = os.path.abspath(python_path)
        self.venv_dir = os.path.abspath(os.path.dirname(os.path.dirname(python_path)))
        self.build_type = build_type
        self.pip = build_type.get_pip(self.python_path)

    def create_clone(self, venv_dir_clone: str) -> "PythonEnvironment":
        """
        Clone this Python environment into a new python environment
        with `venv_dir_clone` as the top-level directory of the virtual environment.
        The given directory must not already exist.
        """
        shutil.copytree(self.venv_dir, venv_dir_clone)
        python_path = os.path.join(venv_dir_clone, self.get_rel_path_to_python_binary())
        return PythonEnvironment(python_path, self.build_type)

    def restore(self, python_environ: "PythonEnvironment") -> None:
        """
        Restore the state of the given Python environment into this Python environment.
        """
        shutil.rmtree(self.venv_dir)
        self.python_path = python_environ.create_clone(self.venv_dir).python_path
        self.build_type = python_environ.build_type
        self.pip = python_environ.build_type.get_pip(self.python_path)

    def get_rel_path_to_python_binary(self) -> str:
        """
        Return the path to the python binary expressed relatively to the root of this
        virtual environment.
        """
        python_binary = os.path.basename(self.python_path)
        _, bin_dir = os.path.split(os.path.dirname(self.python_path))
        return os.path.normpath(os.path.join(".", bin_dir, python_binary))


class ModuleSetTester:
    """
    Class that provides the functionality to run the module set tests.

    General principle: There are two separate venv

    * V1 venv:
        * Contains the product and pytest-inmanta-extensions.
        * When the tests run on a module the requirements.txt and
          the requirements.dev.txt of that module are additionally
          installed in the venv.
    * V2 venv
        * Contains the product, pytest-inmanta-extensions and all modules
          in the module set installed as a V2 module.
        * When the tests run on a module, the requirements.dev.txt file
          of that module is additionally installed in the venv.

    After testing a certain module, the state of each venv is reset
    by restoring from a snapshot created at the beginning of the test run.
    """

    def __init__(
        self,
        sources: irt.module_sources.ModuleSourceManager,
        product_repo: str,
        branch: str,
        build_type: BuildType,
        working_dir: str,
        github_token: str,
    ) -> None:
        self.sources = sources
        self.product_repo = product_repo
        self.branch = branch
        self.build_type = build_type
        self.working_dir = working_dir
        self.github_token = github_token

        # product install requires empty directory
        self.working_dir_v1 = os.path.join(self.working_dir, "v1")
        (
            self.product_config,
            self.v1_python_environ,
        ) = self._install_product_and_pytest_inmanta_ext_in_venv(self.working_dir_v1)

        # ISO4 doesn't support V2 modules
        if not self._running_against_iso4_module_set():
            # product install requires empty directory
            self.working_dir_v2 = os.path.join(self.working_dir, "v2")
            self.v2_python_environ: PythonEnvironment
            (
                _,
                self.v2_python_environ,
            ) = self._install_product_and_pytest_inmanta_ext_in_venv(
                self.working_dir_v2
            )

        self._flake8_failed: List[str] = []
        self._pytest_failed: Dict[str, List[Module.GENERATION]] = defaultdict(list)
        self._test_run_finished = False

    def _install_product_and_pytest_inmanta_ext_in_venv(
        self, working_dir: str
    ) -> Tuple[ProductConfig, PythonEnvironment]:
        """
        Create venv containing product and pytest-inmanta-extensions.
        """
        product_config, python_path = install_product(
            self.branch,
            self.github_token,
            self.product_repo,
            self.build_type,
            working_dir,
        )
        python_environment = PythonEnvironment(python_path, self.build_type)
        python_environment.pip.set_env_vars()
        install_pytest_inmanta_extensions(python_environment.pip)
        return product_config, python_environment

    def _running_against_iso4_module_set(self) -> bool:
        """
        Return true iff we are running the tests against the ISO4 module set.
        """
        module_set_file_name = os.path.basename(self.product_config.module_set.path)
        return module_set_file_name == "inmanta-service-orchestrator-4.yml"

    def test_module_set(self) -> None:
        """
        Execute the module set test.
        """
        if self._test_run_finished:
            raise Exception(
                "Calling test_module_set() twice on the same instance is not supported."
            )
        self._test_run_finished = True

        # Populate directory containing v1 modules
        v1_modules: List[ModuleV1]
        v1_module_data: Dict[str, irt.module_sources.ModuleData]
        v1_modules, v1_module_data = self._download_v1_module_set()
        # Install requirements.txt file of each module into the v1 venv
        v1_requirements_txt_files = [
            req_file
            for module in v1_modules
            for req_file in util.get_requirements_files(
                module.path, exclude_dev_reqs=True
            )
        ]
        self.v1_python_environ.pip.install(requires_files=v1_requirements_txt_files)
        # Create a snapshot be able to uninstall the dev requirements that are installed
        # before running the tests for a certain module.
        v1_venv_snapshot_dir = os.path.join(self.working_dir_v1, "env_snapshot")
        v1_python_environ_snap = self.v1_python_environ.create_clone(
            v1_venv_snapshot_dir
        )

        if not self._running_against_iso4_module_set():
            # Populate directory containing v2 modules
            v2_modules_dir = os.path.join(self.working_dir, "v2_modules")
            v2_modules_dct: Dict[str, ModuleV2] = {
                mod.name: mod
                for mod in self._convert_all_v1_modules_to_v2_modules(
                    v1_modules, v2_modules_dir
                )
            }
            # Install the v2 modules into the v2 venv
            module_tool = ModuleTool()
            v2_artifacts = [
                module_tool.build(path=mod.path) for mod in v2_modules_dct.values()
            ]
            self.v2_python_environ.pip.install(pkg=v2_artifacts)
            # Create a snapshot be able to uninstall the dev requirements that are installed
            # before running the tests for a certain module.
            v2_venv_snapshot_dir = os.path.join(self.working_dir_v2, "env_snapshot")
            v2_python_environ_snap: PythonEnvironment = (
                self.v2_python_environ.create_clone(v2_venv_snapshot_dir)
            )

        for v1_module in v1_modules:
            # Get module version and git commit
            commit_hash = GitRepo(clone_dir=v1_module.path).get_commit()[0:6]

            # Print module name in box for readability
            module_version = v1_module_data[v1_module.name]["version"]
            info_string = f"{v1_module.name} {module_version} {commit_hash}"
            LOGGER.info(
                "\n***%s***\n*** %s ***\n***%s***\n",
                "*" * (len(info_string) + 2),
                info_string,
                "*" * (len(info_string) + 2),
            )

            # Run tests on the V1 module
            self._setup_venv_for_module(
                self.v1_python_environ, v1_module, v1_python_environ_snap
            )
            self._run_flake(self.v1_python_environ, v1_module)
            self._run_pytest(self.v1_python_environ, v1_module)

            if not self._running_against_iso4_module_set():
                # Run pytest when the v2 module is installed in the venv
                v2_module: ModuleV2 = v2_modules_dct[v1_module.name]
                self._setup_venv_for_module(
                    self.v2_python_environ, v2_module, v2_python_environ_snap
                )
                self._run_pytest(self.v2_python_environ, v2_module)

            # module name at the end, to make it easy to find the results
            LOGGER.info(
                "\n+++ %s +++\n",
                info_string,
            )

        # For jenkins readability
        LOGGER.info("\n")
        LOGGER.info(("=" * 50) + " SUMMARY " + ("=" * 50))
        if not self._flake8_failed and not self._pytest_failed:
            LOGGER.info("All tests succeeded.")
        else:
            if self._flake8_failed:
                LOGGER.info(
                    "\nModules that did not pass flake8 linting:\n\t"
                    + ", ".join(self._flake8_failed)
                )
            if self._pytest_failed:
                failures = [
                    f"{module_name} ({', '.join(gen.name for gen in generations)})"
                    for module_name, generations in self._pytest_failed.items()
                ]
                LOGGER.info("\nModules with failing tests:\n\t" + ", ".join(failures))
            sys.exit(1)

    def _download_v1_module_set(
        self,
    ) -> Tuple[List[ModuleV1], Dict[str, irt.module_sources.ModuleData]]:
        """
        Download the V1 modules into the <workspace>/modules directory and
        return the corresponding list of ModuleV1 objects.
        """
        module_set_config = self.product_config.module_set
        remote: Optional[str]
        if (
            self.build_type.is_stable_release()
            and module_set_config.publish_repo is not None
        ):
            # Checkout stable module releases from the location they were published to
            remote = module_set_config.publish_repo
        else:
            remote = None

        module_set, modules_dir, _ = download_module_set_for_product(
            self.v1_python_environ.python_path,
            self.working_dir,
            self.product_config,
            self.sources,
            self.github_token,
            remote,
        )
        modules: List[Optional[ModuleV1]] = [
            ModuleV1.from_path(os.path.join(modules_dir, module_name))
            for module_name in module_set.keys()
        ]
        # It's safe to assume that all are found by the ModuleV1.from_path() method
        # because download_module_set_for_product() performs a completeness check
        assert all(mod is not None for mod in modules)
        return modules, module_set

    def _convert_all_v1_modules_to_v2_modules(
        self, v1_modules: Iterable[ModuleV1], v2_modules_dir: str
    ) -> List[ModuleV2]:
        """
        Convert the given list of V1 modules into V2 modules and store those V2 modules into `v2_modules_dir`.
        """
        result = []
        for module_v1 in v1_modules:
            # ModuleConverter.convert needs a project to be set
            module_v1 = ModuleV1(project=DummyProject(), path=module_v1.path)
            module_converter = ModuleConverter(module_v1)
            module_v2_path = os.path.join(v2_modules_dir, module_v1.name)
            module_converter.convert(output_directory=module_v2_path)
            module_v2: Optional[ModuleV2] = ModuleV2.from_path(module_v2_path)
            if module_v2 is None:
                raise Exception(
                    f"Module {module_v1.name} not found at: {module_v2_path}"
                )
            result.append(module_v2)
        return result

    def _setup_venv_for_module(
        self,
        python_environ: PythonEnvironment,
        module: Module,
        python_environ_snap: PythonEnvironment,
    ) -> None:
        """
        This method restores the given snapshot in the `python_environ` and installs the development
        requirements needed to be able to run the flake8 and pytest checks on the given module.
        """
        LOGGER.info(
            "Setup venv for tests of module %s (%s)",
            module.name,
            module.GENERATION.name,
        )
        # Restore venv from snapshot
        python_environ.restore(python_environ_snap)
        # Install development requirements
        python_environ.pip.install(
            requires_files=util.get_requirements_files(
                module.path, exclude_prod_reqs=True
            )
        )

    def _run_pytest(self, python_environ: PythonEnvironment, module: Module) -> None:
        """
        Run pytest on the given module.
        """
        LOGGER.info("Running tests for: %s (%s)", module.name, module.GENERATION.name)
        tests = os.path.join(module.path, "tests")
        if os.path.isdir(tests):
            pytest_stdout_log = os.path.join(module.path, "pytest-stdout.log")
            pytest_log = os.path.join(module.path, "pytest-log.log")

            process = util.subprocess_log(
                subprocess.Popen,
                [
                    python_environ.python_path,
                    "-m",
                    "pytest",
                    "-vvv",
                    "-s",
                    f"--log-file={pytest_log}",
                    "--log-file-level=DEBUG",
                    tests,
                ],
                logger=LOGGER,
                cwd=module.path,
                env=self._get_env_vars_for_pytest(python_environ.venv_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            # Stream output to file and to stdout
            try:
                with open(pytest_stdout_log, "wb") as f:
                    for line in iter(process.stdout.readline, b""):
                        print(line.decode(), end="", flush=True)
                        f.write(line)
            finally:
                # 1) Set the returncode.
                # 2) Ensure the process has terminated in case of an IOError
                process.communicate()

            if process.returncode != 0:
                LOGGER.error(
                    "Tests on module %s (%s) failed",
                    module.name,
                    module.GENERATION.name,
                )
                self._pytest_failed[module.name].append(module.GENERATION)
            else:
                LOGGER.info(
                    "Tests on module %s (%s) succeeded",
                    module.name,
                    module.GENERATION.name,
                )

        else:
            LOGGER.warning("Module %s doesn't have any tests", module.name)

    def _get_env_vars_for_pytest(self, venv_path: str) -> Dict[str, str]:
        """
        Return the environment variables that should be provided to pytest to run the tests of
        the given module.
        """
        env = os.environ.copy()
        env["INMANTA_TEST_ENV"] = venv_path
        env["INMANTA_TEST_INFRA_SETUP"] = "true"
        return env

    def _run_flake(self, python_environ: PythonEnvironment, module: ModuleV1) -> None:
        """
        Run the flake8 check on the given module.
        """
        LOGGER.info("Checking code formatting for: %s", module.name)
        # Make sure flake8 is installed
        cmd = [
            python_environ.python_path,
            "-m",
            "pip",
            "install",
            "flake8",
            "flake8-black",
            "flake8-isort",
            "flake8-copyright",
        ]
        completed_process = util.subprocess_log(
            subprocess.run,
            cmd,
            logger=LOGGER,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if completed_process.returncode:
            LOGGER.error(
                "Failed to install flake8 or one of it's requirements\n%s",
                completed_process.stdout,
            )

        lint_list: List[str] = [
            os.path.join(module.path, directory)
            for directory in ["plugins", "tests"]
            if os.path.exists(os.path.join(module.path, directory))
        ]
        if len(lint_list) > 0:
            cmd = [python_environ.python_path, "-m", "flake8"]
            if not os.path.exists(os.path.join(module.path, "setup.cfg")):
                cmd.extend(
                    [
                        "--ignore=H405,H404,H302,H306,H301,H101,E252,E203,F722,W503",
                        "--builtins=string,number,bool",
                        "--exclude=**/.env,.venv,.git,.tox,dist,doc,**egg",
                        "--max-line-length=128",
                        "--copyright-check",
                        "--copyright-author=Inmanta",
                    ]
                )

            LOGGER.debug("Running style checker on %s", ", ".join(lint_list))
            completed_process = util.subprocess_log(
                subprocess.run,
                cmd + lint_list,
                logger=LOGGER,
                cwd=module.path,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            if completed_process.returncode:
                LOGGER.error(
                    "Style check failed for module %s\n%s",
                    module.name,
                    completed_process.stdout,
                )
                self._flake8_failed.append(module.name)
            else:
                LOGGER.info("Style check succeeded for module %s", module.name)


def download_module_set_for_product(
    python_path: str,
    working_dir: str,
    product_config: ProductConfig,
    sources: irt.module_sources.ModuleSourceManager,
    github_token: str,
    remote: Optional[str] = None,
) -> Tuple[Dict[str, irt.module_sources.ModuleData], str, ModuleSetDefinition]:
    # Clone module set repository
    module_set_dir = os.path.join(working_dir, "module_set_repo")
    module_set_file = product_config.module_set.clone_module_set_repo(
        module_set_dir, token=github_token
    )
    module_set_definition = ModuleSetDefinition.from_file(module_set_file)
    # Download modules
    modules_dir = os.path.join(working_dir, "modules")
    os.makedirs(modules_dir, exist_ok=True)
    module_set = download_set(
        python_path,
        module_set_definition,
        sources,
        modules_dir,
        remote=remote,
    )
    return module_set, modules_dir, module_set_definition


def install_pytest_inmanta_extensions(pip: Pip) -> None:
    """
    install pytest-inmanta-extensions to make sure it is matched with core

    The following table explains which python package is expected for each product install:

    | product | inmanta | inmanta-core | inmanta-service-orchestrator |
    |---------|---------|--------------|------------------------------|
    |  OSS    |   yes   |     yes      |             no               |
    |  ISO3   |   yes   |     no       |             yes              |
    |  ISO4+  |   no    |     yes      |             yes              |
    """
    lines = pip.list()
    version_lookup = {
        line["name"]: line["version"]
        for line in lines
        if line["name"].startswith("inmanta")
    }
    if (
        "inmanta-service-orchestrator" in version_lookup
        and "inmanta-core" in version_lookup
        and "inmanta" in version_lookup
    ):
        raise Exception(
            "The inmanta-core and the inmanta package cannot be installed simultaneously when "
            "running against the ISO product."
        )
    for core_package_name in ["inmanta-core", "inmanta"]:
        # This ensures that inmanta-core is used if it exists (any release except ISO3)
        # Otherwise inmanta is used (ISO3)
        if core_package_name in version_lookup:
            core_version = version_lookup[core_package_name]
            pip.install(
                f"{core_package_name}[pytest-inmanta-extensions]=={core_version}"
            )
            return


def install_product(
    branch: str,
    github_token: str,
    product_repo: str,
    build_type: BuildType,
    working_dir: str,
) -> Tuple[ProductConfig, str]:
    if os.path.exists(working_dir) and os.listdir(working_dir):
        raise Exception(f"Working directory {working_dir} is not empty")

    # Clone product repository
    product_directory = os.path.join(working_dir, "product_repo")
    util.clone_repo(product_repo, product_directory, branch, github_token)
    product: ProductProject = ProductProject(product_directory)
    product_config: ProductConfig = product.get_project_config()

    # Install product (required for module download)
    LOGGER.info("Creating venv")
    python_version: Optional[PythonVersion] = product_config.build.rpm.python_version
    if python_version:
        python_binary = python_version.get_name_python_binary()
    else:
        python_binary = sys.executable
    python_path: str = util.ensure_tmp_env(working_dir, python_binary)
    product.install(
        python_path,
        working_dir,
        branch,
        build_type,
        github_token,
    )
    return product_config, python_path
