//---------------------------------------------------------------------
// NOC.gis.street.Lookup
//---------------------------------------------------------------------
// Copyright (C) 2007-2014 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.gis.street.Lookup");

Ext.define("NOC.gis.street.Lookup", {
    extend: "NOC.core.Lookup",
    url: "/gis/division/lookup/"
});
