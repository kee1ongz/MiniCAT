Object.defineProperty(exports, "__esModule", {
    value: !0
}), exports.commonLog = void 0;

var e = {
    online: "https://webapi.fooww.com",
    test: "https://test-webapi.fooww.com"
}, o = {
    sendBinderrorLoadLogUrl: "/api/WeixinGateway/WeappLog/WeappLog"
}, t = {
    sendOnLoadLog: function(e) {
        getCurrentPages();
        var t = {
            logType: 0,
            enentType: "onLoad",
            coreParameter: e && e.scene,
            logContent: r(e)
        };
        n(o.sendBinderrorLoadLogUrl, t);
    },
    sendBinderrorLoadLog: function(e) {
        var t = {
            logType: 0,
            enentType: "binderrorLoad",
            coreParameter: e.detail.src,
            logContent: r(e)
        };
        n(o.sendBinderrorLoadLogUrl, t);
    }
};

function n(o, t) {
    var n = wx.getExtConfigSync(), c = wx.getAccountInfoSync().miniProgram.appId, s = n.attr.siteid, i = n.attr.domain, g = getCurrentPages(), p = {};
    try {
        wx.getSystemInfo({
            success: function(e) {
                p = e;
            }
        });
    } catch (e) {
        e = VM2_INTERNAL_STATE_DO_NOT_USE_OR_PROGRAM_WILL_FAIL.handleException(e);
        p = e;
    }
    var d = {
        appid: c || "",
        domain: i || "",
        siteID: s || "",
        localTimeStr: a() || "",
        pagePath: g && g[0].route || "unkown",
        pageContent: r(g),
        systemInfoContent: r(p),
        logType: t.logType || 0,
        enentType: t.enentType || "unkown",
        coreParameter: t.coreParameter || "",
        logContent: t.logContent || ""
    };
    o = e.online + o;
    try {
        wx.request({
            url: o,
            data: d,
            method: "post",
            dataType: "json",
            header: {
                "content-type": "application/json"
            },
            complete: function(e) {},
            success: function(e) {},
            fail: function(e) {}
        });
    } catch (e) {
        e = VM2_INTERNAL_STATE_DO_NOT_USE_OR_PROGRAM_WILL_FAIL.handleException(e);
        console.log("catch"), console.log(e.message);
    }
}

function r(e) {
    return e && JSON.stringify(e) || "";
}

function a() {
    var e = new Date(), o = e.getFullYear(), t = e.getMonth() + 1, n = e.getDate(), r = e.getHours(), a = e.getMinutes(), c = e.getSeconds();
    return t >= 1 && t <= 9 && (t = "0" + t), n >= 0 && n <= 9 && (n = "0" + n), r >= 0 && r <= 9 && (r = "0" + r), 
    a >= 0 && a <= 9 && (a = "0" + a), c >= 0 && c <= 9 && (c = "0" + c), o + "-" + t + "-" + n + " " + r + ":" + a + ":" + c;
}

exports.commonLog = t;