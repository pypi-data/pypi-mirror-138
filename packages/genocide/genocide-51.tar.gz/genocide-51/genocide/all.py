# This file is placed in the Public Domain.


"OTP-CR-117/19"


def __dir__():
    return (
        "cfg",
        "cmd",
        "dbs",
        "evt",
        "flt",
        "fnc",
        "fnd",
        "irc",
        "jsn",
        "krn",
        "log",
        "opt",
        "prs",
        "req",
        "rpt",
        "tbl",
        "tdo",
        "thr",
        "tmr",
        "udp",
        "usr",
        "wsd"
    )


from genocide.tbl import Tbl


from genocide import cfg
from genocide import cmd
from genocide import dbs
from genocide import evt
from genocide import flt
from genocide import fnc
from genocide import jsn
from genocide import krn
from genocide import opt
from genocide import prs
from genocide import rpt
from genocide import tbl
from genocide import thr
from genocide import tmr

from genocide import fnd
from genocide import irc
from genocide import log
from genocide import opt
from genocide import req
from genocide import sta
from genocide import tdo
from genocide import udp
from genocide import usr
from genocide import wsd


for mn in __dir__():
    md = getattr(locals(), mn, None)
    if md:
        Tbl.add(md)
