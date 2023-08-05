from datetime import datetime
import click
import os
import re
import codecs
import json
import pathlib
from shuvel.rule import Severity
from shuvel.result import Result
import shuvel.utils as utils
from rich.progress import Progress


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    utils.print_version()
    ctx.exit()


def set_verbose(ctx, param, value):
    utils.set_verbose()


@click.group()
@click.option("-v", "--version", is_flag=True, callback=print_version, expose_value=False, is_eager=True)
@click.option("-d", "--debug", is_flag=True, callback=set_verbose, expose_value=False, is_eager=True)
def shuvel_cli():
    pass


@click.command()
@click.option("-r", "--rules",
              help="Comma-seperated list of rule names and categories to run, wildcards accepted [*]",
              required=False,
              default="*",
              type=str)
@click.option("-s", "--sev",
              help="Only show results of this severity or higher [Info]",
              required=False,
              default="Info",
              type=click.Choice(["High", "Low", "Info"], case_sensitive=False))
@click.option("-t", "--target",
              help="Path to the directory with the source code to run against [.]",
              required=False,
              default=os.getcwd(),
              type=str)
@click.option("-R", "--rules-dir",
              help=f"Path to the rules directory [{utils.get_rules_dir()}]",
              required=False,
              default=utils.get_rules_dir(),
              type=str)
@click.option("--sarif",
              help="Export results into a SARIF log [No]",
              is_flag=False,
              flag_value=datetime.now().strftime("%Y%m%d-%H%M%S-shuvel.sarif.json"),
              required=False)
def run(rules, sev, target, rules_dir, sarif):
    """Run a set of rules against the target folder"""
    all_rules = utils.load_all_rules([""], rules_dir)

    severity = Severity(sev.lower())

    user_sel_rules = [x.strip() for x in rules.split(",")]

    target_files = []
    target_fq_dir = os.path.abspath(target)
    dirlist = [target_fq_dir]
    results = []

    utils.print_info(f"Running against the target directory `{target_fq_dir}`.")

    while len(dirlist) > 0:
        for (dirpath, dirnames, filenames) in os.walk(dirlist.pop()):
            dirlist.extend(dirnames)
            target_files.extend(map(lambda n: os.path.join(*n), zip([dirpath] * len(filenames), filenames)))

    rules_to_run = []
    for rule in all_rules:
        # First see if the rule we have loaded is supposed to run now
        if utils.should_rule_run(user_sel_rules, severity, rule):
            rules_to_run.append(rule)

    with Progress() as progress_bar:
        total_progress = len(rules_to_run) * len(target_files)
        task = progress_bar.add_task("Scanning...", total=total_progress)

        for rule in rules_to_run:
            # Run this rule against the entire codebase. In the future we can make it smarter so that
            # specific rules run only against specific files based on extentions, but for now deal with it.
            if rule.ignore_case:
                p = re.compile(rule.pattern, re.IGNORECASE)
            else:
                p = re.compile(rule.pattern)

            for target_file in target_files:
                with codecs.open(target_file, "r", encoding="utf-8", errors="ignore") as fd:
                    lines = fd.readlines()
                    i = 0
                    for line in lines:
                        i += 1
                        m = p.search(line)
                        if m is not None:
                            tmp_result = Result(target_file, i, line.strip(), rule)
                            results.append(tmp_result)
                progress_bar.update(task, advance=1)

    utils.print_info("Results:")
    for result in results:
        utils.print_info(f"{result.rel_file_path}:{result.line_num}")
        utils.print_info(f"    Match:    {result.line_str}")
        utils.print_info(f"    Rule:     {result.rule.name}")
        utils.print_info(f"    Severity: {result.rule.severity}")
        utils.print_info(f"    Desc:     {result.rule.description}")
        if result.rule.references:
            utils.print_info("    Refs:")
            for ref in result.rule.references:
                utils.print_info(f"        - {ref}")

    if sarif:
        sarif_d = {}
        sarif_d["version"] = "2.1.0"
        sarif_d["$schema"] = "https://www.schemastore.org/schemas/json/sarif-2.1.0-rtm.4.json"
        sarif_d["runs"] = []
        run_d = {}
        run_d["tool"] = {}
        run_d["tool"]["driver"] = {}
        run_d["tool"]["driver"]["name"] = "shuvel"
        run_d["tool"]["driver"]["informationUri"] = "https://gitlab.com/TheTwitchy/shuvel"
        run_d["results"] = []

        for result in results:
            result_d = {}
            result_d["ruleId"] = result.rule.name

            if result.rule.severity == Severity.HIGH:
                result_d["level"] = "error"
            elif result.rule.severity == Severity.LOW:
                result_d["level"] = "warning"
            else:
                result_d["level"] = "note"

            result_d["message"] = {"text": result.rule.description}
            location_d = {}
            location_d["physicalLocation"] = {}
            location_d["physicalLocation"]["artifactLocation"] = {
                "uri": pathlib.Path(os.path.join(target, result.rel_file_path)).as_uri()
            }
            location_d["physicalLocation"]["region"] = {"startLine": result.line_num, "startColumn": 1}

            result_d["locations"] = [location_d]

            run_d["results"].append(result_d)

        sarif_d["runs"].append(run_d)

        with open(sarif, "w") as fd:
            fd.write(json.dumps(sarif_d))


@click.command()
@click.option("-R", "--rules-dir",
              help="Path to the rules directory",
              required=False,
              default=utils.get_rules_dir(),
              type=str)
def test(rules_dir):
    """Load a set of rules, useful for testing"""
    utils.print_info(f"Loading all rules and validating correctness from `{rules_dir}`.")
    utils.load_all_rules([""], rules_dir)
    utils.print_info("All rules loaded successfully.")


@click.command()
@click.option("-R", "--rules-dir",
              help="Path to the rules directory",
              required=False,
              default=utils.get_rules_dir(),
              type=str)
def rules(rules_dir):
    """Show all loaded rules"""
    utils.print_info(f"Showing all rules from `{rules_dir}`.")
    all_rules = utils.load_all_rules([""], rules_dir)
    all_rules = sorted(all_rules, key=lambda x: x.name)

    for rule_obj in all_rules:
        utils.print_info(rule_obj.name)


shuvel_cli.add_command(run)
shuvel_cli.add_command(test)
shuvel_cli.add_command(rules)

if __name__ == "__main__":
    shuvel_cli()
