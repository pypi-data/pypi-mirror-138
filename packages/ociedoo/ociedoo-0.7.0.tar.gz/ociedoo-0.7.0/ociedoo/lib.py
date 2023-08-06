# Copyright 2018-2020 Coop IT Easy SCRLfs (<http://coopiteasy.be>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

"""Small function used across the project."""

import gzip
import re
import shlex
import subprocess
import time
from configparser import ConfigParser
from os import path
from pathlib import Path

import sh

from ociedoo import GZIPMT, REDBNAME


def get_all_db(db_user=""):
    """
    Get all databases that belongs to :db_user:. If :db_user: is empty,
    list all available databases.

    :param db_user: postgresql database user
    :param type: str
    :returns: list of database names
    :returns type: list
    """
    psql_out = sh.psql("-l").strip()
    psql_out_lines = psql_out.split("\n")
    # Remove title lines and last line
    psql_out_lines = psql_out_lines[3:-1]
    # Extract database name and owner
    dbs_owners = [
        (line.split("|")[0].strip(), line.split("|")[1].strip())
        for line in psql_out_lines
    ]
    # Remove empty lines
    dbs_owners = [(db, owner) for (db, owner) in dbs_owners if db]
    # Filter databases if db_user is not empty
    if db_user:
        dbs = [db for (db, owner) in dbs_owners if owner == db_user]
    else:
        dbs = [db for (db, owner) in dbs_owners]
    return dbs


def sql_rename_db(old_dbname, new_dbname):
    """
    Return SQL to rename :old_dbname: to :new_dbname:.

    :old_dbname: and :new_dbname: must be different and not empty.
    :returns: The SQL query to rename :old_dbname: to :new_dbname:.
    """
    if not re.match(REDBNAME, old_dbname):
        raise ValueError(
            "'%s' is not a valid or existing database name." % old_dbname
        )
    if not re.match(REDBNAME, new_dbname):
        raise ValueError(
            "'%s' is not a valid name for a new database." % new_dbname
        )
    if old_dbname == new_dbname:
        raise ValueError(
            "The new database name must be different than "
            "the previous one: '%s' == '%s'" % (old_dbname, new_dbname)
        )
    query = 'ALTER DATABASE "%s" RENAME TO "%s"' % (old_dbname, new_dbname)
    return query


def close_connections(database):
    """
    Return the SQL to close connection to :database:.
    Raise an error if command fails.
    """
    query_to_free_database = """
        SELECT pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE datname = '{}' AND pid != pg_backend_pid()
    """.format(
        database
    )
    subprocess.run(
        ["psql", "postgres", "-c", query_to_free_database],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def get_file_content(filename, pbar=None):
    """
    Read :filename: and return its content. :filename: is decompressed
    if needed.
    """
    # TODO: Maybe using mimetypes python lib is better...
    filemt = sh.mimetype("--brief", filename).strip()
    if filemt == GZIPMT:
        with gzip.open(path.expanduser(filename)) as file:
            for line in file:
                if pbar:
                    pbar.update(1)
                if line[0:2] != "--":  # ignore comments
                    yield line
    else:
        with open(path.expanduser(filename)) as file:
            for line in file:
                if pbar:
                    pbar.update(1)
                if line[0:2] != "--":  # ignore comments
                    yield line


def linecount(filename):
    """
    Count number of line in :filename:. :filename: is decompressed if
    needed.
    """
    filemt = sh.mimetype("--brief", filename).strip()
    counter = 0
    if filemt == GZIPMT:
        with gzip.open(path.expanduser(filename), "r") as file:
            while file.readline():
                counter += 1
    else:
        with open(path.expanduser(filename)) as file:
            while file.readline():
                counter += 1
    return counter


def is_daemon_running(daemon_name=""):
    """Check if :daemon_name: is running or not."""
    try:
        sh.systemctl("is-active", daemon_name)
    except sh.ErrorReturnCode:
        return False
    else:
        return True


def stop_daemon(daemon_name=""):
    """Stop :daemon_name:."""
    try:
        sh.sudo.systemctl("stop", daemon_name)
        time.sleep(1)
    except sh.ErrorReturnCode:
        return False
    else:
        return True


def start_daemon(daemon_name=""):
    """Start :daemon_name:."""
    try:
        sh.sudo.systemctl("start", daemon_name)
    except sh.ErrorReturnCode:
        return False
    else:
        return True


def get_addons_path(configfile, working_dir):
    """
    Return the lis of addons path found in :configfile:.
    """
    config_path = Path(configfile)
    working_dir_path = Path(working_dir)
    conf = ConfigParser(default_section="options")
    conf.read(str(config_path.expanduser()))
    ap_str = conf.get("options", "addons_path", fallback="")
    ap_list = [Path(path.strip()).expanduser() for path in ap_str.split(",")]
    ap_list_absolute = [
        str(path) if path.is_absolute() else str(working_dir_path / path)
        for path in ap_list
    ]
    return ap_list_absolute


def get_odoo_version(database):
    """Return the odoo version as a integer."""
    query = "SELECT latest_version FROM ir_module_module WHERE name = 'base';"
    try:
        psql_out = sh.psql(
            "--no-psqlrc",
            "--quiet",
            "--tuples-only",
            "--no-align",
            "--dbname",
            database,
            "--command",
            query,
        )
        version = int(psql_out.strip().split(".")[0])
    except sh.ErrorReturnCode:
        version = None
    return version


def get_bin_odoo_version(profile):
    """Return odoo version based on the binary given in profile."""
    odoo_path = path.expanduser(profile.get("odoo-binary-path", "odoo"))
    odoo_working_dir = path.expanduser(profile.get("working-directory", "."))
    odoo_cmd = [
        str(odoo_path),
        "--version",
    ]
    result = subprocess.run(
        odoo_cmd,
        cwd=odoo_working_dir if odoo_working_dir else None,
        stdout=subprocess.PIPE,
        universal_newlines=True,
        check=True,
    )
    matches = re.match(r"Odoo Server (?P<version>\d+)\..*", result.stdout)
    if matches:
        return int(matches.group("version"))
    return None


def get_installed_modules(database):
    """Return the list of installed modules on a database."""
    query = (
        "SELECT name FROM ir_module_module WHERE state = 'installed' "
        "ORDER BY name;"
    )
    modules = sh.psql(
        "--no-psqlrc",
        "--tuples-only",
        "--no-align",
        "--quiet",
        "--dbname",
        database,
        "--command",
        query,
    )
    if modules:
        return modules.split("\n")
    return []


def get_profile(cfg, profile_name=None):
    """Return the profile named profile_name."""
    if profile_name:
        profile = [
            prof for prof in cfg["profile"] if prof["name"] == profile_name
        ][0]
    else:
        profile = cfg["profile"][0]
    return profile


def run_odoo(
    profile,
    database,
    logfile=None,
    other_args=None,
    stdout=None,
    stderr=None,
    stdin=None,
):
    """Run odoo command"""
    other_args = other_args if other_args is not None else []
    odoo_path = path.expanduser(profile.get("odoo-binary-path", "odoo"))
    odoo_conf_path = (
        path.expanduser(profile["odoo-config-path"])
        if "odoo-config-path" in profile
        else None
    )
    odoo_working_dir = path.expanduser(profile.get("working-directory", "."))
    odoo_default_options_list = shlex.split(profile.get("default-options", ""))
    odoo_cmd = [
        str(odoo_path),
        *odoo_default_options_list,
        "--config",
        str(odoo_conf_path),
        "--db-filter",
        "^%s$" % database,
        "-d",
        database,
        "--logfile",
        str(logfile) if logfile else "/dev/stdout",
        "--workers",
        "0",
        "--max-cron-threads",
        "0",
        *other_args,
    ]
    return subprocess.Popen(
        odoo_cmd,
        cwd=odoo_working_dir if odoo_working_dir else None,
        stdout=stdout,
        stderr=stderr,
        stdin=stdin,
    )
