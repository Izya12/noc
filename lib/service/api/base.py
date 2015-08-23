# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Service API handler
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Python modules
import json
## Third-party modules
import tornado.web
## NOC modules
from noc.lib.debug import error_report


class ServiceAPIRequestHandler(tornado.web.RequestHandler):
    """
    HTTP JSON-RPC request handler
    """
    SUPPORTED_METHODS = ("POST",)

    def initialize(self, service, api_class):
        self.service = service
        self.api = api_class(service)

    def post(self, *args, **kwargs):
        # Parse JSON
        try:
            req = json.loads(self.request.body)
        except ValueError, why:
            return self.api_error(why)
        # Parse request
        id = req.get("id", "0")
        params = req.get("params", [])
        method = req.get("method")
        if not method or not hasattr(self.api, method):
            return self.api_error(
                "Invalid method: '%s'" % method,
                id=id
            )
        h = getattr(self.api, method)
        if not getattr(h, "api", False):
            return self.api_error(
                "Method is not callable: '%s'" % method,
                id=id
            )
        # lock = getattr(h, "lock", None)
        # if lock:
        #     # Locked call
        #     try:
        #         lock_name = lock % self.service.config
        #         with self.service.lock(lock_name):
        #             result = h(*params)
        #     except Exception, why:
        #         return self.api_error(
        #             "Failed: %s" % why,
        #             id=id
        #         )
        # else:
        try:
            result = h(*params)
        except Exception, why:
            return self.api_error(
                "Failed: %s" % why,
                id=id
            )
        self.write(json.dumps({
            "id": id,
            "error": None,
            "result": result
        }))

    def api_error(self, msg, id=None):
        rsp = {
            "error": str(msg)
        }
        if id:
            rsp["id"] = id
        self.write(json.dumps(rsp))


class ServiceSubscriber(object):
    def __init__(self, service, api_class):
        self.service = service
        self.api_class = api_class
        self.service.connect_writer()

    def get_topic(self):
        return self.api_class.get_service_topic(
            self.api_class.level,
            api_name=self.api_class.name,
            service_name=self.service.name,
            pool=self.service.config.pool,
            dc=self.service.config.dc,
            node=self.service.config.node
        )

    def on_message(self, message):
        # Parse JSON
        try:
            req = json.loads(message.body)
        except ValueError, why:
            return self.api_error(message, why)
        # Parse request
        tid = req.get("id", "0")
        params = req.get("params", [])
        method = req.get("method")
        reply_to = req.get("from")
        if not method or not hasattr(self.api_class, method):
            self.service.logger.error("Invalid API method %s", method)
            return self.reply(
                reply_to, tid,
                error="Invalid API method %s" % method
            )
        api = self.api_class(self.service)
        h = getattr(api, method)
        if not hasattr(h, "api"):
            return self.reply(
                reply_to, tid,
                "Method is not callable: '%s'" % method
            )
        try:
            result = h(*params)
        except Exception, why:
            error_report()
            return self.reply(reply_to, tid, "Failed: %s" % why)
        return self.reply(reply_to, tid, result=result)

    def reply(self, reply_to, tid, error=None, result=None):
        msg = {
            "id": tid
        }
        if error:
            self.service.logger.error("[API ERROR] %s", error)
            msg["error"] = error
        elif result:
            msg["result"] = result
        if reply_to:
            self.service.publish(reply_to, msg)
        return True


class ServiceAPI(object):
    """
    Service API declares a set of functions accessible
    via HTTP and NSQ JSON-RPC.

    API methods are denoted by @api decorator
    """
    # Name and version of the service
    # RPC URL will be /v<verson>/<name>/
    name = "test"
    # Tornado JSON-RPC request handler
    http_request_handler = ServiceAPIRequestHandler
    # API LEVEL Constants
    # Do not register and advertise
    AL_NONE = 0
    # Advertise at global level
    AL_GLOBAL = 1
    # Advertise at pool level
    AL_POOL = 2
    # Advertise at node level
    AL_NODE = 3
    # Advertise at service level
    AL_SERVICE = 4
    # API level
    level = AL_NONE

    def __init__(self, service):
        self.service = service

    @classmethod
    def get_service_url(cls):
        return r"/%s/" % cls.name

    @classmethod
    def get_service_topic(cls, level=None, api_name=None,
                          service_name=None, pool=None,
                          dc=None, node=None):
        api_name = api_name or cls.name
        level = level or cls.level
        if level == cls.AL_GLOBAL:
            return "rpc.%s" % api_name
        elif level == cls.AL_POOL:
            return "rpc.%s.%s" % (api_name, pool)
        elif level == cls.AL_NODE:
            return "rpc.%s.%s.%s" % (api_name, dc, node)
        elif level == cls.AL_SERVICE:
            return "rpc.%s.%s.%s.%s" % (api_name, dc, node, service_name)
        else:
            return None

    @classmethod
    def get_http_request_handler(cls):
        return cls.http_request_handler


def api(method):
    """
    API method decorator
    """
    method.api = True
    return method


class lock(object):
    """
    Decorator to lock api method call with named lock
    """
    def __init__(self, name):
        self.name = name

    def __call__(self, method):
        method.lock = self.name
        return method