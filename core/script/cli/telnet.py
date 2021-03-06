# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Telnet CLI
##----------------------------------------------------------------------
## Copyright (C) 2007-2016 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Tornado modules
from tornado.iostream import IOStream
import tornado.gen
## NOC modules
from base import CLI

IAC = chr(0xFF)  # Interpret As Command
DONT = chr(0xFE)
DO = chr(0xFD)
WONT = chr(0xFC)
WILL = chr(0xFB)
SB = chr(0xFA)
SE = chr(0xF0)
NAWS = chr(0x1F)
AO = chr(0xF5)
AYT = chr(0xF6)

IAC_CMD = {
    DO: "DO",
    DONT: "DONT",
    WILL: "WILL",
    WONT: "WONT"
}

IGNORED_CMD = set([AO, AYT])

TELNET_OPTIONS = {
    0: "BINARY",
    1: "ECHO",
    2: "RCP",
    3: "SGA",
    4: "NAMS",
    5: "STATUS",
    6: "TM",
    7: "RCTE",
    8: "NAOL",
    9: "NAOP",
    10: "NAOCRD",
    11: "NAOHTS",
    12: "NAOHTD",
    13: "NAOFFD",
    14: "NAOVTS",
    15: "NAOVTD",
    16: "NAOLFD",
    17: "XASCII",
    18: "LOGOUT",
    19: "BM",
    20: "DET",
    21: "SUPDUP",
    22: "SUPDUPOUTPUT",
    23: "SNDLOC",
    24: "TTYPE",
    25: "EOR",
    26: "TUID",
    27: "OUTMRK",
    28: "TTYLOC",
    29: "3270REGIME",
    30: "X3PAD",
    31: "NAWS",
    32: "TSPEED",
    33: "LFLOW",
    34: "LINEMODE",
    35: "XDISPLOC",
    36: "OLD_ENVIRON",
    37: "AUTHENTICATION",
    38: "ENCRYPT",
    39: "NEW_ENVIRON",
    255: "EXOPL",
}

# ECHO+SGA+TTYPE+NAWS
ACCEPTED_TELNET_OPTIONS = "\x01\x03\x18\x1f"


class TelnetIOStream(IOStream):
    def __init__(self, sock, cli, *args, **kwargs):
        super(TelnetIOStream, self).__init__(sock, *args, **kwargs)
        self.cli = cli
        self.logger = cli.logger
        self.iac_seq = ""
        self.out_iac_seq = []
        self.naws = cli.profile.get_telnet_naws()

    @tornado.gen.coroutine
    def startup(self):
        if self.cli.profile.telnet_send_on_connect:
            self.logger.debug("Sending %r on connect",
                              self.cli.profile.telnet_send_on_connect)
            yield self.write(self.cli.profile.telnet_send_on_connect)

    def read_from_fd(self):
        chunk = super(TelnetIOStream, self).read_from_fd()
        if self.iac_seq and chunk:
            # Restore incomplete IAC context
            chunk = self.iac_seq + chunk
            self.iac_seq = ""
        r = []
        while chunk:
            left, seq, right = chunk.partition(IAC)
            r += [left]
            if seq:
                # Process IAC sequence
                if not right or len(right) == 1:
                    # Incomplete sequence
                    # Collect for next round
                    self.iac_seq = IAC + right
                    break
                elif right[0] == IAC:
                    # <IAC> <IAC> leads to single <IAC>
                    r += [IAC]
                    chunk = right[1:]
                elif right[0] in IGNORED_CMD:
                    # Ignore command
                    chunk = right[1:]
                elif right[0] != SB:
                    # Process IAC <cmd> <opt>
                    self.process_iac(right[0], right[1])
                    chunk = right[2:]
                else:
                    # Process IAC SB ... SE sequence
                    if SE not in right:
                        self.iac_seq = IAC + right
                        break
                    else:
                        i = right.index(SE)
                        self.process_iac_sb(right[1:i - 1])
                        chunk = right[i:]
            else:
                # Return leftovers
                break
        if self.out_iac_seq:
            self.write_to_fd("".join(self.out_iac_seq))
            self.out_iac_seq = []
        return "".join(r)

    def write(self, data, callback=None):
        data = data.replace(IAC, IAC + IAC)
        return super(TelnetIOStream, self).write(data,
                                                 callback=callback)

    def send_iac(self, cmd, opt):
        """
        Send IAC response
        """
        self.logger.debug("Send %s", self.iac_repr(cmd, opt))
        self.out_iac_seq += [IAC + cmd + opt]
        # self.write_to_fd(IAC + cmd + opt)

    def send_iac_sb(self, opt, data=None):
        sb = IAC + SB + opt
        if data:
            sb += data
        sb += IAC + SE
        self.logger.debug("Send IAC SB %r %r IAC SE",
                          opt, data)
        self.out_iac_seq += [sb]
        #self.write_to_fd(sb)

    def process_iac(self, cmd, opt):
        """
        Process IAC command.
        """
        self.logger.debug("Received %s", self.iac_repr(cmd, opt))
        if cmd == DO:
            r = WILL if opt in ACCEPTED_TELNET_OPTIONS else WONT
        elif cmd == DONT:
            r = WONT
        elif cmd == WILL:
            r = DO if opt in ACCEPTED_TELNET_OPTIONS else DONT
        elif cmd == WONT:
            r = DONT
        else:
            return  # Ignore invalid IAC command
        self.send_iac(r, opt)
        # Send NAWS response
        if cmd == DO and opt == NAWS:
            self.send_iac_sb(opt, self.naws)

    def process_iac_sb(self, sb):
        self.logger.debug("Received IAC SB %s SE", sb.encode("hex"))
        if sb == "\x18\x01":  # TTYPE SEND
            self.out_iac_seq += [IAC + SB + "\x18\x00XTERM" + IAC + SE]

    def iac_repr(self, cmd, opt):
        """
        Human-readable IAC sequence
        :param cmd:
        :param opt:
        :return:
        """
        if isinstance(opt, basestring):
            opt = ord(opt)
        return "%s %s" % (
            IAC_CMD.get(cmd, cmd),
            TELNET_OPTIONS.get(opt, opt),
        )


class TelnetCLI(CLI):
    name = "telnet"
    default_port = 23
    iostream_class = TelnetIOStream
