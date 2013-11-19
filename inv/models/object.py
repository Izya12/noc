## -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## ObjectModel model
##----------------------------------------------------------------------
## Copyright (C) 2007-2013 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Third-party modules
from mongoengine.document import Document
from mongoengine.fields import StringField, DictField, ObjectIdField
## NOC modules
from connectiontype import ConnectionType
from objectmodel import ObjectModel
from modelinterface import ModelInterface
from error import ConnectionError, ModelDataError
from noc.lib.nosql import PlainReferenceField
from noc.lib.utils import deep_merge


class Object(Document):
    """
    Inventory object
    """
    meta = {
        "collection": "noc.objects",
        "allow_inheritance": False,
        "indexes": ["data", "container"]
    }

    name = StringField()
    model = PlainReferenceField(ObjectModel)
    data = DictField()
    container = ObjectIdField(required=False)

    def __unicode__(self):
        return unicode(self.name or self.id)

    def get_data(self, interface, key):
        mi = ModelInterface.objects.filter(name=interface).first()
        if not mi:
            raise ModelDataError("Invalid interface '%s'" % interface)
        attr = mi.get_attr(key)
        if not attr:
            raise ModelDataError("Invalid attribute '%s.%s'" % (
                interface, key))
        if attr.is_const:
            # Lookup model
            return self.model.get_data(interface, key)
        else:
            v = self.data.get(interface, {})
            return v.get(key)

    def set_data(self, interface, key, value):
        # @todo: Check interface restrictions
        if interface not in self.data:
            self.data[interface] = {}
        self.data[interface][key] = value

    def reset_data(self, interface, key):
        if interface in self.data and key in self.data[interface]:
            del self.data[interface][key]

    def has_connection(self, name):
        return self.model.get_connection(name) is not None

    def get_p2p_connection(self, name):
        """
        Get neighbor for p2p connection (s and mf types)
        Returns connection, remote object, remote connection or
        None, None, None
        """
        c = ObjectConnection.objects.filter(
            __raw__={
                "connection": {
                    "$elemMatch": {
                        "object": self.id,
                        "name": name
                    }
                }
            }
        ).first()
        if c:
            for x in c.connection:
                if x.object.id != self.id:
                    return c, x.object, x.name
        # Strange things happen
        return None, None, None

    def disconnect_p2p(self, name):
        """
        Remove connection *name*
        """
        c = self.get_p2p_connection(name)[0]
        if c:
            c.delete()

    def connect_p2p(self, name, remote_object, remote_name, data,
                    reconnect=False):
        lc = self.model.get_model_connection(name)
        if lc is None:
            raise ConnectionError("Local connection not found: %s" % name)
        rc = remote_object.model.get_model_connection(remote_name)
        if rc is None:
            raise ConnectionError("Remote connection not found: %s" % remote_name)
        # Check genders are compatible
        r_gender = ConnectionType.OPPOSITE_GENDER[rc.gender]
        if lc.gender != r_gender:
            raise ConnectionError("Incompatible genders: %s - %s" % (
                lc.gender, rc.gender
            ))
        # Check directions are compatible
        if ((lc.direction == "i" and rc.direction != "o") or
                (lc.direction == "o" and rc.direction != "i") or
                (lc.direction == "s" and rc.direction != "s")):
            raise ConnectionError("Incompatible directions: %s - %s" % (
                lc.direction, rc.direction))
        # Check types are compatible
        c_types = lc.type.get_compatible_types(lc.gender)
        if rc.type.id not in c_types:
            raise ConnectionError("Incompatible connection types: %s - %s" % (
                lc.type.name, rc.type.name
            ))
        # Check existing connecitons
        if lc.type.genders in ("s", "m", "f", "mf"):
            ec, r_object, r_name = self.get_p2p_connection(name)
            if ec is not None:
                # Connection exists
                if reconnect:
                    if (r_object.id == remote_object.id and
                        r_name == remote_name):
                        # Same connection exists
                        n_data = deep_merge(ec.data, data)
                        if n_data != ec.data:
                            # Update data
                            ec.data = n_data
                            ec.save()
                        return
                    self.disconnect_p2p(name)
                else:
                    raise ConnectionError("Already connected")
        # Create connection
        c = ObjectConnection(
            connection=[
                ObjectConnectionItem(object=self, name=name),
                ObjectConnectionItem(object=remote_object,
                                     name=remote_name)
            ],
            data=data
        ).save()
        # Disconnect from container on o-connection
        if lc.direction == "o" and self.parent:
            self.parent = None
            self.save()
        return c

    def put_into(self, container):
        """
        Put object into container
        """
        if not container.get_data("container", "container"):
            raise ValueError("Must be put into container")
        # Disconnect all o-connections
        for c in self.model.connections:
            if c.direction == "o":
                c, _, _ = self.get_p2p_connection(c.name)
                if c:
                    self.disconnect_p2p(c.name)
        # Connect to parent
        self.container = container.id
        self.save()

    def get_content(self):
        """
        Returns all items directly put into container
        """
        return Object.objects.filter(container=self.id)

    def get_name_path(self):
        """
        Return list of container names
        """
        np = [unicode(self)]
        c = self.container
        while c:
            o = Object.objects.filter(id=c).first()
            if o:
                np = [unicode(o)] + np
                c = o.container
            else:
                break
        return np



## Avoid circular references
from objectconnection import ObjectConnection, ObjectConnectionItem