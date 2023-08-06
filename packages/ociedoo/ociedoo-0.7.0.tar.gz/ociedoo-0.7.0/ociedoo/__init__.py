# Copyright 2018-2020 Coop IT Easy SCRLfs (<http://coopiteasy.be>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

"""Constant shared across the module"""

from pathlib import Path

from prgconfig import PrgConfig

__productname__ = "ociedoo"
__version__ = "0.7.0"
__license__ = "GPL-3.0-or-later"

# Path for default value for config file
PGRNAME = "ociedoo"
DEFAULTSPATH = str(Path(__file__).parent / Path("defaults"))
DEFAULT_CONF = str(Path(DEFAULTSPATH) / "config")

config = PrgConfig(prg_name=PGRNAME, defaults_file=Path(DEFAULT_CONF))

# DB rules
REDBNAME = "^([a-zA-Z0-9-._]+)$"

# Mime-Type
GZIPMT = "application/gzip"
SQLMT = "application/sql"
