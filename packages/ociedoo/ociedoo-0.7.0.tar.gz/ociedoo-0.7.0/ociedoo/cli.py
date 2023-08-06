# Copyright 2018-2020 Coop IT Easy SCRLfs (<http://coopiteasy.be>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

"""CLI interface"""

import datetime
import os
import signal
import subprocess
import time
from pathlib import Path
from pprint import pformat

import click
import sh
from passlib.context import CryptContext

import ociedoo
from ociedoo import PGRNAME, check, complete, config, lib

# Context settings
CONTEXT_SETTINGS = {"auto_envvar_prefix": PGRNAME.upper()}


# Other callback function


def cb_print_cmd(cmd, success, exit_code):
    """Print the command that has been run on stdout"""
    click.echo("Running: %s" % cmd.ran)


# CLI commands


@click.group(
    context_settings=CONTEXT_SETTINGS,
    short_help="Simplify the management of Odoo instances.",
)
@click.option(
    "conf",
    "--config",
    "-c",
    type=click.Path(exists=True),
    autocompletion=complete.file_completion,
    metavar="CONFIG-FILE",
    help="ociedoo config file.",
)
@click.version_option(version=ociedoo.__version__)
@click.pass_context
def main(ctx, conf):
    """
    This is a CLI tool to simplify the management of Odoo instances.

    To get help on a particular command run:

        ociedoo COMMAND --help

    This program needs a configuration file to work properly. This file
    can be referenced via the `--config` or found in the following
    locations: .ociedoo.conf, XDG_CONFIG_HOME/ociedoo/config,
    ~/.ociedoo.conf, XDG_CONFIG_DIRS/ociedoo/config,
    /etc/ociedoo/config. This list is from the more important to the
    less important. Also the environment variable OCIEDOO_CONF act as
    using `--config`. In such a case only the specified config file is
    read, else all files found are merged.

    Options always beats the configuration file.
    """
    if not isinstance(ctx.obj, dict):
        ctx.obj = {}
    if conf:
        config.config_file_path = [conf]
    config.load()
    ctx.obj["cfg"] = config


@main.command(
    context_settings=dict(
        ignore_unknown_options=True,
    ),
    short_help="Run Odoo with default options.",
)
@click.argument(
    "database",
    callback=check.check_database_exist,
    autocompletion=complete.databases_complete,
)
@click.argument("odoo_args", nargs=-1, type=click.UNPROCESSED)
@click.option(
    "profile_name",
    "--profile",
    "-p",
    callback=check.check_profile_exists,
    autocompletion=complete.profile_complete,
    metavar="PROFILE",
    help="""name of a profile defined in the ociedoo config file.
    [Default: first profile found].""",
)
@click.option(
    "modules",
    "-u",
    "--update",
    metavar="MODULES",
    autocompletion=complete.modules_complete_list,
    help="Update MODULES.",
)
@click.pass_context
def run(ctx, profile_name, database, modules, odoo_args):
    """
    Run Odoo with some defaults options given in a PROFILE.

    Defaults can be a special port, some default debug options, special
    odoo configuration file, etc.

    PROFILE is the name of a profile given in the configuration file of
    ociedoo. In the configuration file, profiles are defined as sections
    that begins with 'profile-'. For example, section '[profile-simple]'
    is the section named 'simple'.

    DATABASE is the database on witch module can be updated and on which
    odoo will be launched.

    ODOO_ARGS is arguments directly given to the odoo command.
    """
    cfg = ctx.obj["cfg"]

    profile = lib.get_profile(cfg, profile_name)

    if modules:
        update_option = ("-u", modules)
    else:
        update_option = ()

    try:
        process = lib.run_odoo(
            profile=profile,
            database=database,
            other_args=update_option + odoo_args,
        )
        if process.wait():
            ctx.fail("Error: Odoo terminate with code %d" % process.returncode)
    except KeyboardInterrupt:
        click.echo("CTRL-C: program will terminate properly.", err=True)
        try:
            process.send_signal(signal.SIGINT)
            process.wait()
        except KeyboardInterrupt:
            click.echo("CTRL-C: program will exit now.", err=True)
            process.kill()
            ctx.exit(101)
        ctx.exit(100)
    ctx.exit()


@main.command(
    context_settings=dict(
        ignore_unknown_options=True,
    ),
    short_help="Update odoo modules on databases.",
)
@click.argument("modules", autocompletion=complete.modules_complete_list)
@click.argument("odoo_args", nargs=-1, type=click.UNPROCESSED)
@click.option(
    "profile_name",
    "--profile",
    "-p",
    callback=check.check_profile_exists,
    autocompletion=complete.profile_complete,
    metavar="PROFILE",
    help="""name of a profile defined in the ociedoo config file.
    [Default: first profile found].""",
)
@click.option(
    "databases",
    "--dbname",
    "-d",
    autocompletion=complete.databases_complete_list,
    metavar="DBNAMES",
    help="""names of the database to update.
    [Default: databases where MODULES are installed].""",
)
@click.option(
    "restart_mode",
    "--restart-before",
    "--ninja",
    flag_value="restart-before",
    help="Restart Odoo daemon before performing updates.",
)
@click.option(
    "restart_mode",
    "--no-restart",
    flag_value="no-restart",
    help="Do not restart Odoo daemon for performing updates.",
)
@click.option(
    "restart_mode",
    "--stop-before-start-after",
    flag_value="stop-odoo",
    help="Stop Odoo before performing updates and restart it after.",
)
@click.option("-y", "--yes", is_flag=True, help="Answer yes to questions.")
@click.pass_context
def update_module(
    ctx, modules, odoo_args, databases, profile_name, restart_mode, yes
):
    """
    Update MODULES on each database where at least one of MODULES are
    installed.

    Odoo is run with some default options in order to update MODULES.

    Several databases are updated simultaneously.

    When running Odoo, the defaults options are:

        - write log in a new file (one for each database)

        - stop after init

        - multithread mode (workers = 0)

        - No cron threads (max-cron-threads = 0)

    More options can be given to Odoo via ODOO_ARGS.

    MODULES can contain 'all' to update all modules or a coma separated
    list of modules name. MODULES list cannot contain spaces.

    DBNAMES can contain 'all' to update all databases or a list of
    database name separated by a coma and without spaces. 'all' refers
    to all databases that belongs to the user defined in the
    `database_user` field in the configuration file. Only databases that
    belongs to this user can be used, others will be ignored.

    ODOO_ARGS standard options that the Odoo binary accepts. For example
    it is useful to supply debug option when something goes wrong.
    """
    cfg = ctx.obj["cfg"]

    profile = lib.get_profile(cfg, profile_name)
    db_user = profile.get("database-user")
    odoo_daemon_name = profile.get("daemon-name")
    logdir = Path(profile.get("odoo-log-dir")).expanduser()
    update_options = ["-u", modules, "--stop-after-init"]

    version = lib.get_bin_odoo_version(profile)
    if version > 10:
        update_options.append("--no-http")
    else:
        update_options.append("--no-xmlrpc")

    if databases:
        if databases.strip() == "all":
            dbs = lib.get_all_db(db_user)
        else:
            arg_dbs = [db.strip() for db in databases.split(",")]
            dbs = [db for db in lib.get_all_db(db_user) if db in arg_dbs]
            ignored_dbs = set(arg_dbs) - set(dbs)
            for db in ignored_dbs:
                click.echo(
                    "Warning: Ignore '%s' because it is not a database that "
                    "belongs to %s." % (db, db_user)
                )
    else:
        alldbs = lib.get_all_db(db_user)
        args_modules = {mod.strip() for mod in modules.split(",")}
        dbs = []
        for db in alldbs:
            installed_modules = set(lib.get_installed_modules(db))
            if args_modules & installed_modules:
                dbs.append(db)
        click.echo(
            "Info: The following databases will be updated: %s" % ",".join(dbs)
        )

    if restart_mode == "restart-before":
        question = (
            "%s will be restarted. Do you want to continue ?"
            % odoo_daemon_name
        )
        if yes or click.confirm(question):
            # Restart odoo daemon
            if lib.is_daemon_running(odoo_daemon_name) and not lib.stop_daemon(
                odoo_daemon_name
            ):
                ctx.fail(
                    "Fail to stop %s daemon. To do so try: sudo "
                    "systemctl stop %s" % (odoo_daemon_name, odoo_daemon_name)
                )
            if not lib.start_daemon(odoo_daemon_name):
                ctx.fail(
                    "Fail to start %s daemon. To do so try: sudo "
                    "systemctl start %s" % (odoo_daemon_name, odoo_daemon_name)
                )
    elif restart_mode == "stop-odoo":
        # Stop odoo daemon
        if lib.is_daemon_running(odoo_daemon_name):
            question = (
                "%s is running do you want to stop it ?" % odoo_daemon_name
            )
            if yes or click.confirm(question):
                if not lib.stop_daemon(odoo_daemon_name):
                    ctx.fail(
                        "Fail to stop %s daemon. To do so try: sudo "
                        "systemctl stop %s"
                        % (odoo_daemon_name, odoo_daemon_name)
                    )
            else:
                click.echo(
                    "%s is running. Cannot perform updates." % odoo_daemon_name
                )
                ctx.abort()

    processes = []
    for db in dbs:
        processes.append(
            {
                "db": db,
                "fun": lib.run_odoo,
                "kwargs": {
                    "profile": profile,
                    "database": db,
                    "logfile": (
                        logdir
                        / "update-{}-{}.log".format(
                            db,
                            datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"),
                        )
                    ),
                    "other_args": update_options + list(odoo_args),
                    "stdout": subprocess.DEVNULL,
                    "stderr": subprocess.DEVNULL,
                    "stdin": subprocess.DEVNULL,
                },
                "proc": None,
            }
        )

    def all_proc_done(processes):
        """Return True if all processes are done."""
        all_proc_done = True
        for process in processes:
            if process["proc"] is None or process["proc"].poll() is None:
                all_proc_done = False
                break
        return all_proc_done

    def all_proc_success(processes):
        """Return True if all processes are done and success."""
        all_proc_success = True
        for process in processes:
            if (
                process["proc"] is None
                or process["proc"].poll() is None
                or process["proc"].poll()
            ):
                all_proc_success = False
                break
        return all_proc_success

    def prune_failed_proc(processes):
        """Delete failed processes as there where not executed."""
        for process in processes:
            if process["proc"].returncode:
                process["proc"] = None

    def count_running_proc(processes):
        """Return the number of running processes."""
        nb_running_proc = 0
        for process in processes:
            if process["proc"] is not None and process["proc"].poll() is None:
                nb_running_proc += 1
        return nb_running_proc

    def proc_status(processes):
        """Return a list of string representation of proc status."""
        status = []
        for process in processes:
            state = " "
            if process["proc"] is not None:
                if process["proc"].poll() is None:
                    state = "."
                elif process["proc"].poll():
                    state = "x"
                else:
                    state = "v"
            status.append("[{}] {}".format(state, process["db"]))
        return status

    max_proc = os.cpu_count() if os.cpu_count() else 1
    try:
        while not all_proc_success(processes):
            if count_running_proc(processes) < max_proc:
                if all_proc_done(processes):
                    click.echo()
                    if yes or click.confirm(
                        "There is failed jobs. Do you want to try again ?"
                    ):
                        prune_failed_proc(processes)
                    else:
                        break
                # Launch next proc
                for process in processes:
                    if process["proc"] is None:
                        process["proc"] = process["fun"](**process["kwargs"])
                        break
            # Show status on stdout
            click.echo("\r" + ", ".join(proc_status(processes)), nl=False)
            time.sleep(0.1)
        click.echo("\r" + ", ".join(proc_status(processes)), nl=False)
    except KeyboardInterrupt:
        click.echo()
        click.echo("CTRL-C: program will terminate properly.", err=True)
        try:
            for process in processes:
                if (
                    process["proc"] is not None
                    and process["proc"].poll() is None
                ):
                    process["proc"].send_signal(signal.SIGINT)
                    process["proc"].wait()
        except KeyboardInterrupt:
            click.echo("CTRL-C: program will exit now.", err=True)
            for process in processes:
                if (
                    process["proc"] is not None
                    and process["proc"].poll() is None
                ):
                    process["proc"].kill()
            ctx.exit(101)
        ctx.exit(100)
    click.echo()
    if not all_proc_success(processes):
        ctx.fail(
            "Errors when updatating the following databases: {}".format(
                ",".join(
                    process["db"]
                    for process in processes
                    if process["proc"].returncode
                )
            )
        )

    if restart_mode == "stop-odoo":
        # Start odoo daemon
        if not lib.is_daemon_running(odoo_daemon_name):
            question = (
                "%s is not running do you want to start it ?"
                % odoo_daemon_name
            )
            if yes or click.confirm(question):
                if not lib.start_daemon(odoo_daemon_name):
                    ctx.fail(
                        "Fail to start %s daemon. To do so try: sudo "
                        "systemctl start %s"
                        % (odoo_daemon_name, odoo_daemon_name)
                    )


@main.command(short_help="Set password for a user.")
@click.argument(
    "database",
    callback=check.check_database_exist,
    autocompletion=complete.databases_complete,
)
@click.option(
    "--login",
    metavar="LOGIN",
    default="admin",
    help="Specify the user for who the password should be set. "
    "Default to 'admin'.",
)
@click.option(
    "--password",
    metavar="PASSWORD",
    prompt="New password",
    hide_input=True,
    confirmation_prompt=True,
    help="Set the admin password to PASSWORD.",
)
@click.pass_context
def set_password(ctx, database, login, password):
    """
    Set the password for a user of DATABASE. The default user is
    'admin', but can be specified with the --login option. The password
    is stored in the database in an encrypted way.

    When running this command you will be prompt to type the password,
    except if the --password is used. --password option should be used
    for scripting. DO NOT not use --password option when using
    interactive shell.

    Setting password for an odoo database version less than 8.0 is not
    supported.
    """
    # Check that login exist in database
    raw_query = "SELECT count(*) FROM res_users WHERE login = '%s'"
    query = raw_query % login
    try:
        nb_login = sh.psql(
            "--no-psqlrc",
            "--no-align",
            "--tuples-only",
            "--dbname",
            database,
            "--command",
            query,
        )
    except sh.ErrorReturnCode as err:
        click.echo(err, err=True)
        ctx.exit(1)
    if not int(nb_login.strip()):
        click.echo(
            "Error: Login '%s' does not exists in database '%s'. "
            "No password changed." % (login, database),
            err=True,
        )
        ctx.exit(1)

    # Get database version
    version = lib.get_odoo_version(database=database)
    if not version:
        click.echo(
            "Error: Could not find Odoo version in %s" % database, err=True
        )
        ctx.exit(1)

    # Encrypt password
    new_pwd_crypt = CryptContext(["pbkdf2_sha512"]).encrypt(password)

    # Set password
    if version >= 12:
        raw_query = "UPDATE res_users SET password='%s' WHERE login='%s';"
        query = raw_query % (new_pwd_crypt, login)
    elif version >= 8:
        raw_query = (
            "UPDATE res_users SET password='', password_crypt='%s' "
            "WHERE login='%s';"
        )
        query = raw_query % (new_pwd_crypt, login)
    else:
        click.echo(
            "Error: Password setting not supported for Odoo version %s"
            % version,
            err=True,
        )
        ctx.exit(1)
    try:
        sh.psql(
            "--dbname",
            database,
            "--command",
            query,
        )
    except sh.ErrorReturnCode as err:
        click.echo(err, err=True)
        ctx.exit(1)


@main.command(short_help="List installed modules on a database.")
@click.argument(
    "database",
    callback=check.check_database_exist,
    autocompletion=complete.databases_complete,
)
@click.pass_context
def list_module(ctx, database):
    """
    List all installed modules in the database named DATABASE.
    """
    try:
        modules = lib.get_installed_modules(database)
    except sh.ErrorReturnCode as err:
        click.echo(err, err=True)
        ctx.exit(1)
    for mod in modules:
        click.echo(mod)


@main.command(short_help="List existing databases.")
@click.argument("user", required=False)
@click.option(
    "profile_name",
    "--profile",
    "-p",
    callback=check.check_profile_exists,
    autocompletion=complete.profile_complete,
    metavar="PROFILE",
    help="""name of a profile defined in the ociedoo config file.
    [Default: first profile found].""",
)
@click.option(
    "all_user",
    "--all",
    is_flag=True,
    help="Ignore USER and show all databases",
)
@click.option(
    "--module",
    metavar="MODULE",
    help="List only database with MODULE installed.",
)
@click.option(
    "separator",
    "--sep",
    metavar="SEPARATOR",
    default="\n",
    help="Separator between databases names on. Default new line.",
)
@click.pass_context
def list_db(ctx, user, profile_name, all_user, module, separator):
    """
    List all the database names that belongs to USER. If USER is not
    specified, the USER from the field `database_user` in the
    configuration file is used.
    """
    cfg = ctx.obj["cfg"]
    profile = lib.get_profile(cfg, profile_name)
    if all_user:
        dbs = lib.get_all_db()
    elif user:
        dbs = lib.get_all_db(user)
    else:
        dbs = lib.get_all_db(profile["database-user"])
    # Filter dbs if module is given
    if module:
        dbs = (db for db in dbs if module in lib.get_installed_modules(db))
    # Two different case for the same thing, because if separator is new
    # line then the output can be feed in real time, not all in a block
    # like when using, for example, a coma as separator.
    if separator in ("\n", "\\n"):
        for db in dbs:
            click.echo(db)
    else:
        click.echo(separator.join(dbs))


@main.command(short_help="Rename databases.")
@click.argument(
    "oldname",
    callback=check.check_database_exist,
    autocompletion=complete.databases_complete,
)
@click.argument("newname", callback=check.check_database_not_exist)
@click.pass_context
def rename_db(ctx, oldname, newname):
    """
    Rename OLDNAME database to NEWNAME.
    """
    try:
        query_to_rename = lib.sql_rename_db(oldname, newname)
    except ValueError as e:
        ctx.fail(e)
    lib.close_connections(oldname)
    result = subprocess.run(
        ["psql", "postgres", "-c", query_to_rename],
        check=False,
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode:
        click.echo("Error: {}".format(result.stderr), err=True)
    ctx.exit(result.returncode)


@main.command(short_help="Delete databases.")
@click.argument(
    "dbname",
    callback=check.check_database_exist,
    autocompletion=complete.databases_complete,
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Delete DBNAME even if it has opened connections.",
)
@click.pass_context
def drop_db(ctx, dbname, force):
    """
    Delete DBNAME.
    """
    if force:
        lib.close_connections(dbname)
    result = subprocess.run(
        ["dropdb", dbname],
        check=False,
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode:
        click.echo("Error: {}".format(result.stderr), err=True)
    ctx.exit(result.returncode)


@main.command(short_help="Copy databases.")
@click.argument(
    "oldname",
    callback=check.check_database_exist,
    autocompletion=complete.databases_complete,
)
@click.argument("newname", callback=check.check_database_not_exist)
@click.pass_context
def copy_db(ctx, oldname, newname):
    """
    Copy OLDNAME database to NEWNAME.
    """
    try:
        sh.createdb("--template", oldname, newname)
    except sh.ErrorReturnCode as err:
        click.echo("Error: ", nl=False, err=True)
        click.echo(err.stderr, err=True)
        ctx.exit(1)


@main.command(short_help="Restore database.")
@click.argument("database", autocompletion=complete.databases_complete)
@click.argument(
    "backup",
    type=click.Path(exists=True),
    autocompletion=complete.file_completion([".sql", ".sql.gz"]),
)
@click.argument(
    "posthook",
    required=False,
    type=click.Path(exists=True),
    autocompletion=complete.file_completion([".sql", ".sql.gz"]),
)
@click.option(
    "profile_name",
    "--profile",
    "-p",
    callback=check.check_profile_exists,
    autocompletion=complete.profile_complete,
    metavar="PROFILE",
    help="""name of a profile defined in the ociedoo config file.
    [Default: first profile found].""",
)
@click.option(
    "--force", "-f", is_flag=True, help="Delete DATABASE if it exist."
)
@click.option(
    "--autosave/--no-autosave",
    default=None,
    help="Backup DATABASE to a new name with pattern "
    "DATABASE-save-YYYY-MM-DD before restoring BACKUP to "
    "DATABASE. Beats --force.",
)
@click.option(
    "--save",
    metavar="SAVENAME",
    callback=check.check_database_not_exist,
    help="Rename DATABASE to SAVENAME instead of deleting it. "
    "Beats --autosave.",
)
@click.option(
    "--login",
    metavar="LOGIN",
    default="admin",
    help="Specify the user for who the password should be set. "
    "Default to 'admin'.",
)
@click.option(
    "pwd",
    "--set-password",
    metavar="PASSWORD",
    required=False,
    help="Prompt for a new user password for DATABASE. "
    "Default user is 'admin'. Set user with --login.",
)
@click.option(
    "no_pwd",
    "--no-set-password",
    is_flag=True,
    help="Do not ask to change a user password. " "Beats --set-password.",
)
@click.option(
    "--disable-posthook",
    is_flag=True,
    default=False,
    help="Disable POSTHOOK execution.",
)
@click.pass_context
def restore_db(
    ctx,
    database,
    backup,
    profile_name,
    posthook,
    force,
    autosave,
    save,
    login,
    pwd,
    no_pwd,
    disable_posthook,
):
    """
    Restore BACKUP on DATABASE.

    BACKUP is a regular sql file or a gzipped version of a regular sql
    file.

    DATABASE can be a new database name or an existing one. If database
    is an existing one see options `--autosave`, `--save` and `--force`.

    A new password for the 'admin' user will be asked. Use
    --no-set-password to not change password. Use --login if the login
    of the admin is not 'admin'.

    POSTHOOK is a regular sql file or a gzipped version of it that
    contains sql instructions that will be executed on DATABASE after
    the restoration of the BACKUP. POSTHOOK can be configured in the
    configuration file. The value of POSTHOOK will replace the one in
    the configuration file. POSTHOOK is not executed if option
    `--disable-posthook` is given, or if POSTHOOK is empty or not given.
    """
    cfg = ctx.obj["cfg"]
    profile = lib.get_profile(cfg, profile_name)

    # Get value from config if not provided in the command line
    if autosave is None:
        autosave = profile["restore"].get("autosave")
    if not posthook:
        posthook = profile["restore"].get("posthook", "").strip()
        if posthook and not Path(posthook).expanduser().exists():
            ctx.echo(
                "Error: file '%s' given in as 'posthook' in the "
                "configuration file does not exist." % posthook,
                err=True,
            )
            ctx.exit(1)

    # Ask for a password if needed
    if not no_pwd:
        pwd = click.prompt(
            "New password for user '%s'" % login,
            hide_input=True,
            confirmation_prompt=True,
        )

    # Save or drop db
    if database in lib.get_all_db():
        if save:
            try:
                ctx.invoke(rename_db, oldname=database, newname=save)
            except click.exceptions.Exit as err:
                if err.exit_code:
                    raise
        elif autosave:
            newname = "%s-save-%s" % (database, str(datetime.date.today()))
            try:
                ctx.invoke(rename_db, oldname=database, newname=newname)
            except click.exceptions.Exit as err:
                if err.exit_code:
                    click.echo(
                        "Take a look at --no-autosave or --save", err=True
                    )
                    raise
        elif force:
            try:
                sh.dropdb(database, _done=cb_print_cmd)
            except sh.ErrorReturnCode as err:
                click.echo("Error: ", nl=False, err=True)
                click.echo(err.stderr, err=True)
                ctx.exit(1)
        else:
            ctx.fail(
                "Database '%s' already exists. Look at --force, "
                "--autosave or --save options." % database
            )
    # Create new db
    try:
        sh.createdb(database, _done=cb_print_cmd)
    except sh.ErrorReturnCode as err:
        click.echo("Error: ", nl=False, err=True)
        click.echo(err.stderr, err=True)
        ctx.exit(1)
    # Import db from a sql file with progression bar
    with click.progressbar(
        length=lib.linecount(backup), label="Restoring database"
    ) as pbar:
        psqlproc = sh.psql(
            database,
            _in=lib.get_file_content(backup, pbar),
            _bg=True,
        )
        psqlproc.wait()

    # Apply posthook
    if not disable_posthook and posthook:
        with click.progressbar(
            length=lib.linecount(posthook), label="Applying posthook"
        ) as pbar:
            try:
                sh.psql(
                    database,
                    _in=lib.get_file_content(posthook, pbar),
                )
            except sh.ErrorReturnCode as err:
                click.echo(err, err=True)
                ctx.exit(1)

    # Set admin password and admin login
    if not no_pwd:
        ctx.invoke(set_password, database=database, login=login, password=pwd)


@main.command()
@click.option(
    "profile_name",
    "--profile",
    "-p",
    callback=check.check_profile_exists,
    autocompletion=complete.profile_complete,
    metavar="PROFILE",
    help="""name of a profile defined in the ociedoo config file.
    [Default: first profile found].""",
)
@click.pass_context
def start_odoo(ctx, profile_name):
    """
    Start odoo daemon.
    """
    cfg = ctx.obj["cfg"]
    profile = lib.get_profile(cfg, profile_name)
    odoo_daemon_name = profile.get("daemon-name")
    if not lib.is_daemon_running(odoo_daemon_name):
        if not lib.start_daemon(odoo_daemon_name):
            ctx.fail(
                "Fail to start %s daemon. To do so try: sudo "
                "systemctl start %s" % (odoo_daemon_name, odoo_daemon_name)
            )


@main.command()
@click.option(
    "profile_name",
    "--profile",
    "-p",
    callback=check.check_profile_exists,
    autocompletion=complete.profile_complete,
    metavar="PROFILE",
    help="""name of a profile defined in the ociedoo config file.
    [Default: first profile found].""",
)
@click.pass_context
def stop_odoo(ctx, profile_name):
    """
    Stop odoo daemon.
    """
    cfg = ctx.obj["cfg"]
    profile = lib.get_profile(cfg, profile_name)
    odoo_daemon_name = profile.get("daemon-name")
    if lib.is_daemon_running(odoo_daemon_name):
        if not lib.stop_daemon(odoo_daemon_name):
            ctx.fail(
                "Fail to stop %s daemon. To do so try: sudo "
                "systemctl stop %s" % (odoo_daemon_name, odoo_daemon_name)
            )


@main.command()
@click.option(
    "profile_name",
    "--profile",
    "-p",
    callback=check.check_profile_exists,
    autocompletion=complete.profile_complete,
    metavar="PROFILE",
    help="""name of a profile defined in the ociedoo config file.
    [Default: first profile found].""",
)
@click.pass_context
def status_odoo(ctx, profile_name):
    """
    Status of tho odoo daemon.
    """
    cfg = ctx.obj["cfg"]
    profile = lib.get_profile(cfg, profile_name)
    odoo_daemon_name = profile.get("daemon-name")
    try:
        sh.systemctl.status(odoo_daemon_name, _fg=True)
    except sh.ErrorReturnCode as err:
        ctx.exit(err.exit_code)


@main.command("config")
@click.option(
    "--source-files",
    is_flag=True,
    default=False,
    help="Show only configuration files that are loaded from "
    "the most important to the less important. Fail if there "
    "is no configuration file loaded.",
)
@click.option(
    "--pager", is_flag=True, default=False, help="Send output to a pager."
)
@click.pass_context
def configuration(ctx, source_files, pager):
    """
    Show the current configuration.
    """
    cfg = ctx.obj["cfg"]

    if source_files:
        file_list = cfg.config_sources
        if not file_list:
            ctx.exit(1)  # No config file loaded
        # To get file from the most important to the less, we need to
        # reverse the list
        file_list.reverse()
        file_list_str = "\n".join(str(path) for path in file_list)
        if pager:
            click.echo_via_pager(file_list_str)
        else:
            click.echo(file_list_str)
    else:
        if pager:
            click.echo_via_pager(pformat(cfg))
        else:
            click.echo(pformat(cfg))
