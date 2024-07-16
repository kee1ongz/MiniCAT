var e = require("@babel/runtime/helpers/typeof.js");

function r(r, t) {
    if (null != r) if ("object" === e(r) || n(r) || (r = [ r ]), n(r)) for (var l = 0, i = r.length; l < i; l++) t.call(null, r[l], l, r); else for (var c in r) Object.prototype.hasOwnProperty.call(r, c) && t.call(null, r[c], c, r);
}

function n(e) {
    return "[object Array]" === toString.call(e);
}

function t(e) {
    return encodeURIComponent(e).replace(/%40/gi, "@").replace(/%3A/gi, ":").replace(/%24/g, "$").replace(/%2C/gi, ",").replace(/%20/g, "+").replace(/%5B/gi, "[").replace(/%5D/gi, "]");
}

module.exports = function(l, i, c) {
    if (!i) return l;
    var o, a;
    if (c) o = c(i); else if (a = i, "undefined" != typeof URLSearchParams && a instanceof URLSearchParams) o = i.toString(); else {
        var u = [];
        r(i, function(l, i) {
            null != l && (n(l) && (i += "[]"), n(l) || (l = [ l ]), r(l, function(r) {
                !function(e) {
                    return "[object Date]" === toString.call(e);
                }(r) ? function(r) {
                    return null !== r && "object" === e(r);
                }(r) && (r = JSON.stringify(r)) : r = r.toISOString(), u.push(t(i) + "=" + t(r));
            }));
        }), o = u.join("&");
    }
    return o && (l += (-1 === l.indexOf("?") ? "?" : "&") + o), l;
};