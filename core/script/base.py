# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## SA Script base
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Python modules
import re
import logging
import functools
import time
import warnings
## NOC modules
from noc.lib.log import PrefixLoggerAdapter
from noc.lib.validators import is_int
from context import ConfigurationContextManager, CacheContextManager


class BaseScript(object):
    """
    Service Activation script base class
    """
    # Script name in form of <vendor>.<system>.<name>
    name = None
    # Enable call cache
    # If True, script result will be cached and reused
    # during lifetime of parent script
    cache = False
    # Implemented interface
    interface = None
    # @todo: Remove
    # Legacy list of implemented interface
    # Replaced with *interface*
    implements = None
    # Scripts required by generic script.
    # For common scripts - empty list
    # For generics - list of pairs (script_name, interface)
    requires = []
    #
    base_logger = logging.getLogger(name or "script")
    #
    _execute_chain = []

    # Common errors
    # LoginError = LoginError
    # CLISyntaxError = CLISyntaxError
    # CLIOperationError = CLIOperationError
    # CLITransportError = CLITransportError
    # CLIDisconnectedError = CLIDisconnectedError
    # TimeOutError = TimeOutError
    # NotSupportedError = NotSupportedError
    # UnexpectedResultError = UnexpectedResultError

    hexbin = {
        "0": "0000", "1": "0001", "2": "0010", "3": "0011",
        "4": "0100", "5": "0101", "6": "0110", "7": "0111",
        "8": "1000", "9": "1001", "a": "1010", "b": "1011",
        "c": "1100", "d": "1101", "e": "1110", "f": "1111"
    }

    def __init__(self, credentials, args=None, capabilities=None,
                 version=None, parent=None, timeout=None):
        if not self.interface and self.implements:
            warnings.warn(
                "Option Script.implements is obsolete and replaced "
                "with Script.interface",
                DeprecationWarning
            )
        self.parent = parent
        self.logger = PrefixLoggerAdapter(self.base_logger, "<ADDRESS>")
        self.profile = None
        self.credentials = credentials or {}
        self.version = version or {}
        self.capabilities = capabilities
        self.timeout = timeout or self.get_timeout()
        self.start_time = None
        self.args = self.clean_input(args or {})

    def clean_input(self, args):
        """
        Cleanup input parameters against interface
        """
        return self.interface.script_clean_input(self.profile, args)

    def clean_output(self, result):
        """
        Clean script result against interface
        """
        return self.interface.script_clean_result(self.profile, result)

    def run(self):
        """
        Run script
        """
        self.start_time = time.time()
        self.logger.info("Running. Input arguments: %s, timeout %s",
                         self.args, self.timeout)
        # Use cached result when available
        cache_hit = False
        if self.cache and self.parent:
            try:
                result = self.get_cache(self.name, self.args)
                self.logger.debug("Cache hit")
                cache_hit = True
            except KeyError:
                pass
        # Execute script
        if not cache_hit:
            result = self.execute()
        # Clean result
        result = self.clean_output(result)
        self.logger.debug("Result: %s", result)
        runtime = time.time() - self.start_time
        self.logger.info("Complete (%.2fms)", runtime * 1000)
        return result

    @classmethod
    def compile_match_filter(cls, *args, **kwargs):
        """
        Compile arguments into version check function
        Returns callable accepting self and version hash arguments
        """
        c = [lambda self, x, g=f: g(x) for f in args]
        for k, v in kwargs.items():
            # Split to field name and lookup operator
            if "__" in k:
                f, o = k.split("__")
            else:
                f = k
                o = "exact"
                # Check field name
            if f not in ("vendor", "platform", "version", "image"):
                raise Exception("Invalid field '%s'" % f)
                # Compile lookup functions
            if o == "exact":
                c += [lambda self, x, f=f, v=v: x[f] == v]
            elif o == "iexact":
                c += [lambda self, x, f=f, v=v: x[f].lower() == v.lower()]
            elif o == "startswith":
                c += [lambda self, x, f=f, v=v: x[f].startswith(v)]
            elif o == "istartswith":
                c += [lambda self, x, f=f, v=v: x[f].lower().startswith(v.lower())]
            elif o == "endswith":
                c += [lambda self, x, f=f, v=v: x[f].endswith(v)]
            elif o == "iendswith":
                c += [lambda self, x, f=f, v=v: x[f].lower().endswith(v.lower())]
            elif o == "contains":
                c += [lambda self, x, f=f, v=v: v in x[f]]
            elif o == "icontains":
                c += [lambda self, x, f=f, v=v: v.lower() in x[f].lower()]
            elif o == "in":
                c += [lambda self, x, f=f, v=v: x[f] in v]
            elif o == "regex":
                c += [lambda self, x, f=f, v=re.compile(v): v.search(x[f]) is not None]
            elif o == "iregex":
                c += [lambda self, x, f=f, v=re.compile(v, re.IGNORECASE): v.search(x[f]) is not None]
            elif o == "isempty":  # Empty string or null
                c += [lambda self, x, f=f, v=v: not x[f] if v else x[f]]
            elif f == "version":
                if o == "lt":  # <
                    c += [lambda self, x, v=v: self.profile.cmp_version(x["version"], v) < 0]
                elif o == "lte":  # <=
                    c += [lambda self, x, v=v: self.profile.cmp_version(x["version"], v) <= 0]
                elif o == "gt":  # >
                    c += [lambda self, x, v=v: self.profile.cmp_version(x["version"], v) > 0]
                elif o == "gte":  # >=
                    c += [lambda self, x, v=v: self.profile.cmp_version(x["version"], v) >= 0]
                else:
                    raise Exception("Invalid lookup operation: %s" % o)
            else:
                raise Exception("Invalid lookup operation: %s" % o)
        # Combine expressions into single lambda
        return reduce(
            lambda x, y: lambda self, v, x=x, y=y: (
                x(self, v) and y(self, v)
            ),
            c,
            lambda self, x: True
        )

    @classmethod
    def match(cls, *args, **kwargs):
        """
        execute method decorator
        """
        @functools.wraps
        def wrap(f):
            # Append to the execute chain
            cls._execute_chain += [(x, f)]
            return f

        # Compile check function
        x = cls.compile_match_filter(*args, **kwargs)
        # Return decorated function
        return wrap

    def match_version(self, *args, **kwargs):
        """
        inline version for BaseScript.match
        """
        return self.compile_match_filter(*args, **kwargs)(
            self,
            self.scripts.get_version()
        )

    def execute(self, **kwargs):
        """
        Default script behavior:
        Pass through _execute_chain and call appropriative handler
        """
        if self._execute_chain and not self.name.endswith(".get_version"):
            # Get version information
            v = self.scripts.get_version()
            # Find and execute proper handler
            for c, f in self._execute_chain:
                if c(self, v):
                    return f(self, **kwargs)
                # Raise error
            raise self.NotSupportedError()

    def cleaned_config(self, config):
        """
        Clean up config from all unnecessary trash
        """
        return self.profile.cleaned_config(config)

    def strip_first_lines(self, text, lines=1):
        """Strip first lines"""
        t = text.split("\n")
        if len(t) <= lines:
            return ""
        else:
            return "\n".join(t[lines:])

    def expand_rangelist(self, s):
        """
        Expand expressions like "1,2,5-7" to [1, 2, 5, 6, 7]
        """
        result = {}
        for x in s.split(","):
            x = x.strip()
            if x == "":
                continue
            if "-" in x:
                l, r = [int(y) for y in x.split("-")]
                if l > r:
                    x = r
                    r = l
                    l = x
                for i in range(l, r + 1):
                    result[i] = None
            else:
                result[int(x)] = None
        return sorted(result.keys())

    rx_detect_sep = re.compile("^(.*?)\d+$")

    def expand_interface_range(self, s):
        """
        Convert interface range expression to a list
        of interfaces
        "Gi 1/1-3,Gi 1/7" -> ["Gi 1/1", "Gi 1/2", "Gi 1/3", "Gi 1/7"]
        "1:1-3" -> ["1:1", "1:2", "1:3"]
        "1:1-1:3" -> ["1:1", "1:2", "1:3"]
        :param s: Comma-separated list
        :return:
        """
        r = set()
        for x in s.split(","):
            x = x.strip()
            if not x:
                continue
            if "-" in x:
                # Expand range
                f, t = [y.strip() for y in x.split("-")]
                # Detect common prefix
                match = self.rx_detect_sep.match(f)
                if not match:
                    raise ValueError(x)
                prefix = match.group(1)
                # Detect range boundaries
                start = int(f[len(prefix):])
                if is_int(t):
                    stop = int(t)  # Just integer
                else:
                    if not t.startswith(prefix):
                        raise ValueError(x)
                    stop = int(t[len(prefix):])  # Prefixed
                if start > stop:
                    raise ValueError(x)
                for i in range(start, stop + 1):
                    r.add(prefix + str(i))
            else:
                r.add(x)
        return sorted(r)

    def hexstring_to_mac(self, s):
        """Convert a 6-octet string to MAC address"""
        return ":".join(["%02X" % ord(x) for x in s])

    @property
    def root(self):
        """Get root script"""
        if self.parent:
            return self.parent.root
        else:
            return self

    def get_cache(self, key1, key2):
        """Get cached result or raise KeyError"""
        s = self.root
        return s.call_cache[repr(key1)][repr(key2)]

    def set_cache(self, key1, key2, value):
        """Set cached result"""
        key1 = repr(key1)
        key2 = repr(key2)
        s = self.root
        if key1 not in s.call_cache:
            s.call_cache[key1] = {}
        s.call_cache[key1][key2] = value

    def configure(self):
        """Returns configuration context"""
        return ConfigurationContextManager(self)

    def cached(self):
        """
        Return cached context managed. All nested CLI and SNMP GET/GETNEXT
        calls will be cached.

        Usage:

        with self.cached():
            self.cli(".....)
            self.scripts.script()
        """
        return CacheContextManager(self)

    def enter_config(self):
        """Enter configuration mote"""
        if self.profile.command_enter_config:
            self.cli(self.profile.command_enter_config)

    def leave_config(self):
        """Leave configuration mode"""
        if self.profile.command_leave_config:
            self.cli(self.profile.command_leave_config)
            self.cli("")  # Guardian empty command to wait until configuration is finally written

    def save_config(self, immediately=False):
        """Save current config"""
        if immediately:
            if self.profile.command_save_config:
                self.cli(self.profile.command_save_config)
        else:
            self.schedule_to_save()

    def schedule_to_save(self):
        self.need_to_save = True
        if self.parent:
            self.parent.schedule_to_save()

    @property
    def motd(self):
        """Return message of the day"""
        if self.activator.use_canned_session:
            return self.activator.get_motd()
        if (not self.cli_provider and
            self.access_profile.scheme in (SSH, TELNET)):
            self.request_cli_provider()
            return self.cli_provider.motd
        return ""

    def re_search(self, rx, s, flags=0):
        """
        Match s against regular expression rx using re.search
        Raise UnexpectedResultError if regular expression is not matched.
        Returns match object.
        rx can be string or compiled regular expression
        """
        if isinstance(rx, basestring):
            rx = re.compile(rx, flags)
        match = rx.search(s)
        if match is None:
            raise self.UnexpectedResultError()
        return match

    def re_match(self, rx, s, flags=0):
        """
        Match s against regular expression rx using re.match
        Raise UnexpectedResultError if regular expression is not matched.
        Returns match object.
        rx can be string or compiled regular expression
        """
        if isinstance(rx, basestring):
            rx = re.compile(rx, flags)
        match = rx.match(s)
        if match is None:
            raise self.UnexpectedResultError()
        return match

    _match_lines_cache = {}

    @classmethod
    def match_lines(cls, rx, s):
        k = id(rx)
        if k not in cls._match_lines_cache:
            _rx = [re.compile(l, re.IGNORECASE) for l in rx]
            cls._match_lines_cache[k] = _rx
        else:
            _rx = cls._match_lines_cache[k]
        ctx = {}
        idx = 0
        r = _rx[0]
        for l in s.splitlines():
            l = l.strip()
            match = r.search(l)
            if match:
                ctx.update(match.groupdict())
                idx += 1
                if idx == len(_rx):
                    return ctx
                r = _rx[idx]
        return None

    def find_re(self, iter, s):
        """
        Find first matching regular expression
        or raise Unexpected result error
        """
        for r in iter:
            if r.search(s):
                return r
        raise self.UnexpectedResultError()

    def hex_to_bin(self, s):
        """
        Convert hexadecimal string to boolean string.
        All non-hexadecimal characters are ignored
        :param s: Input string
        :return: Boolean string
        :rtype: str
        """
        return "".join(
            self.hexbin[c] for c in
            "".join("%02x" % ord(d) for d in s)
        )

    def push_prompt_pattern(self, pattern):
        self.request_cli_provider()
        self.cli_provider.push_prompt_pattern(pattern)

    def pop_prompt_pattern(self):
        self.cli_provider.pop_prompt_pattern()

    def has_oid(self, oid):
        """
        Check object responses to oid
        """
        try:
            n = self.snmp.get(oid)
        except self.snmp.TimeOutError:
            return
        return n is not None and n != ""

    @classmethod
    def get_timeout(cls):
        return script_registry.get_timeout(cls.name)