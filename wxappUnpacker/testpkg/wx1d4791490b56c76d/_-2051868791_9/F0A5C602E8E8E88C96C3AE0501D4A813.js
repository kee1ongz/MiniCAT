var e = require("@babel/runtime/helpers/interopRequireDefault.js").default;

Object.defineProperty(exports, "__esModule", {
    value: !0
}), exports.default = function(e) {
    return e.url = "".concat(a).concat(e.url), e.headers = r(r({}, e.headers), {}, {
        CityCode: s.attr.domain
    }), new Promise(function(r, a) {
        wx.request({
            url: (0, t.default)(e.url, e.params),
            data: e.data,
            header: e.headers,
            responseType: e.responseType,
            method: e.method,
            success: function(t) {
                if (200 === t.statusCode && t.data) r(t.data); else {
                    var s = new Error("response status is not 200");
                    s.request = e, s.response = t, a(s);
                }
            },
            fail: function(e) {
                a(e);
            }
        });
    });
};

var r = require("@babel/runtime/helpers/objectSpread2.js"), t = e(require("72450617E8E8E88C14236E1055B4A813.js")), a = "https://webapi.fooww.com", s = wx.getExtConfigSync();