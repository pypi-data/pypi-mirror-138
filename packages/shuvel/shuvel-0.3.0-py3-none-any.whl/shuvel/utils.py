import os
import pathlib
import configparser
import rich
import json
import re
from rich.console import Console

from shuvel import __version__, PROG_NAME
from shuvel.rule import Rule, Severity

CONFIG_DIR = "shuvel"
CONFIG_FILENAME = "shuvel-config.ini"
RULES_DIR = "rules"
RULE_NAME_REGEX = r"^[a-z\d_]+\.[a-z\d_\.]+$"

console = Console()

global is_verbose
is_verbose = False


# This function from https://github.com/tensorflow/tensorboard/blob/master/tensorboard/uploader/util.py
# Apache 2 licensed
def get_user_config_directory():
    """Returns a platform-specific root directory for user config settings."""
    # On Windows, prefer %LOCALAPPDATA%, then %APPDATA%, since we can expect the
    # AppData directories to be ACLed to be visible only to the user and admin
    # users (https://stackoverflow.com/a/7617601/1179226). If neither is set,
    # return None instead of falling back to something that may be world-readable.
    if os.name == "nt":
        appdata = os.getenv("LOCALAPPDATA")
        if appdata:
            return appdata
        appdata = os.getenv("APPDATA")
        if appdata:
            return appdata
        return None
    # On non-windows, use XDG_CONFIG_HOME if set, else default to ~/.config.
    xdg_config_home = os.getenv("XDG_CONFIG_HOME")
    if xdg_config_home:
        return xdg_config_home
    return os.path.join(os.path.expanduser("~"), ".config")


def get_shuvel_config_dir() -> str:
    config_dir = pathlib.Path(get_user_config_directory(), CONFIG_DIR)
    # Create the directory if it doesn't exist yet.
    config_dir.mkdir(parents=True, exist_ok=True)
    return str(config_dir)


def get_rules_dir() -> str:
    rules_dir = pathlib.Path(get_shuvel_config_dir(), RULES_DIR)
    # Create the directory if it doesn't exist yet.
    rules_dir.mkdir(parents=True, exist_ok=True)
    return str(rules_dir)


def get_config_file_location() -> str:
    return str(pathlib.Path(get_shuvel_config_dir(), CONFIG_FILENAME))


def get_config():
    try:
        config = configparser.ConfigParser()
        config.sections()
        config.read(get_config_file_location())
        return config
    except configparser.Error:
        print_error("Unable to read config file at " + get_config_file_location())
        raise FileNotFoundError


def set_verbose():
    global is_verbose
    is_verbose = True


def _print_line(header, msg):
    rich.print(header, msg)


def print_info(msg):
    _print_line("[[bold blue]INFO[/bold blue]]", msg)


def print_success(msg):
    _print_line("[[bold green]SUCCESS[/bold green]]", msg)


def print_warning(msg):
    _print_line("[[bold yellow]WARN[/bold yellow]]", msg)


def print_error(msg, fatal=True):
    _print_line("[[bold red]ERROR[/bold red]]", msg)

    if fatal:
        quit(-1)


def print_debug(msg):
    if is_verbose:
        _print_line("[[bold purple]DEBUG[/bold purple]]", msg)


def print_version():
    rich.print("[bold]%s[/bold] v%s" % (PROG_NAME, __version__))


def working():
    return console.status("Working...")


def load_all_rules(categories: list[str], rules_dir: str) -> list[Rule]:
    # Get a fully qualified path to where rules are stored
    rules_dir_fq = os.path.abspath(rules_dir)

    print_debug(f"Loading all rules from {rules_dir_fq}.")

    # Get all JSON files in the rules directory
    rules_files = []

    dirlist = [rules_dir_fq]

    while len(dirlist) > 0:
        for (dirpath, dirnames, filenames) in os.walk(dirlist.pop()):
            dirlist.extend(dirnames)
            rules_files.extend(map(lambda n: os.path.join(*n), zip([dirpath] * len(filenames), filenames)))

    rules_arr = []

    for rule_file in rules_files:
        # Only load JSON files
        with open(rule_file, "r") as fd:
            try:
                # Try to load it as a JSON file.
                rules_dict = json.loads(fd.read())
                # Check for the magic value (so we know it's a valid rules file)
                if rules_dict["shuvel_magic"] == 69420:
                    for rule in rules_dict["rules"]:
                        # Check for a valid name. A name looks like `c_cpp.curse_words` or `java.spring.get_request`.
                        # Basically, the name helps define it's category, where the final part of the name is the
                        # specific rule name.
                        try:
                            name = rule["name"]
                            re_match = re.match(RULE_NAME_REGEX, name)
                            if re_match is None:
                                print_error(f"The rule name `{name}` is not valid. Only lowercase letters, numbers, " +
                                            "underscores, and periods are allowed.")

                            # Check against all current rules to see if one with the same name already exists
                            for rule_obj in rules_arr:
                                if name == rule_obj.name:
                                    print_error(f"The rule name `{name}` is not valid, as another rule with the same " +
                                                "name already exists. Only unique names are allowed.")

                        except KeyError:
                            print_error(
                                f"A rule in `{rule_file}` does not have a 'name' field.")

                        # Check for a valid pattern
                        try:
                            pattern = rule["pattern"]
                            try:
                                re.compile(pattern)
                            except re.error as e:
                                print_error(f"The rule {name} has an invalid regex pattern. Error is `{e.msg}`.")
                        except KeyError:
                            print_error(f"The rule {name} does not have a required 'pattern' field.")

                        # Check for a valid description, or use an empty one
                        try:
                            desc = rule["desc"]
                        except KeyError:
                            desc = ""
                            print_warning(f"The rule {name} does not have a 'desc' field. If you are the rule"
                                          "author, it is recommended to set this.")

                        # Check for a valid severity, or use INFO
                        try:
                            severity_str = rule["severity"]
                            if severity_str.lower() == "high":
                                severity = Severity.HIGH
                            elif severity_str.lower() == "low":
                                severity = Severity.LOW
                            elif severity_str.lower() == "info":
                                severity = Severity.INFO
                            else:
                                severity = Severity.INFO
                                print_error(f"The rule {name} has an invalid severity of '{severity_str}'. "
                                            "Allowed values are 'high', 'low', or 'info'.")
                        except KeyError:
                            severity = Severity.INFO
                            print_warning(f"The rule {name} does not have a 'severity'. If you are the rule "
                                          "author, it is recommended to set this.")

                        # Check for a valid ignore-case flag, default to FALSE
                        try:
                            ignore_case = rule["ignore_case"]
                            if not isinstance(ignore_case, bool):
                                ignore_case = False
                                print_warning(f"The rule {name} has an incorrect 'ignore_case' flag."
                                              " It should be either `true` or `false`.")
                        except KeyError:
                            ignore_case = False
                            # No errors here, it is optional.

                        # Check for a valid list of references, or use an empty list
                        try:
                            refs = rule["refs"]
                        except KeyError:
                            print_warning(f"The rule {name} does not have a 'refs' listing. If you are the rule "
                                          "author, it is recommended to set this.")

                        tmp_rule = Rule(name, pattern, desc, severity, ignore_case, refs)
                        print_debug(f"Loaded the rule `{name}` from `{rule_file}`.")
                        rules_arr.append(tmp_rule)
                else:
                    print_debug(f"Skipping the JSON file {rule_file} as it does not appear to be a Shuvel rule file.")
            except json.decoder.JSONDecodeError:
                # If not JSON, skip it.
                print_debug(f"Skipping the file {rule_file} as it does not appear to be a JSON file.")
                continue
    return rules_arr


def should_rule_run(user_sel_rules: list[str], min_severity: Severity, rule_obj: Rule) -> bool:
    # Check reported severity
    if min_severity == Severity.LOW:
        if rule_obj.severity == Severity.INFO:
            print_debug(f"User rule was skipped {rule_obj.name} as the severity is too low.")
            return False
    elif min_severity == Severity.HIGH:
        if rule_obj.severity == Severity.INFO or rule_obj.severity == Severity.LOW:
            print_debug(f"User rule was skipped {rule_obj.name} as the severity is too low.")
            return False

    # This next line gets the category of a rule, so `AAA.BBB.CCC` becomes `AAA.BBB`, as
    # CCC is usually the specific rule name.
    rule_category = ".".join(rule_obj.name.split(".")[:-1])

    for user_rule_sel in user_sel_rules:
        if user_rule_sel[-1] == "*":
            # Run all rules in a given category
            user_sel_category = ".".join(user_rule_sel.split(".")[:-1])

            if user_sel_category == "" or user_sel_category == rule_category:
                print_debug(f"Wildcard rule {user_rule_sel} matches {rule_obj.name}.")
                return True
        else:
            # Run a specific rule
            ret = rule_obj.name == user_rule_sel
            if ret:
                print_debug(f"User rule {rule_obj.name} was will be run by name.")
                return True
    return False
