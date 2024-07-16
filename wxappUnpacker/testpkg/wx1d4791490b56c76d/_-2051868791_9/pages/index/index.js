var e = require("../../@babel/runtime/helpers/objectSpread2"), t = require("../../41FB9925E8E8E88C279DF122D5C4A813.js"), n = require("../../49ACD982E8E8E88C2FCAB185D4A4A813.js"), o = require("../../54D671E4E8E8E88C32B019E36494A813.js");

getApp();

function a(e) {
    var t = wx.getExtConfigSync(), n = i(t.attr.host, t.attr.siteid);
    e.setData({
        MY_HOME: n
    });
}

function i(e, t) {
    var n = e, o = wx.getStorageSync("pkuser");
    return o && -1 == o.indexOf("=") && (n = u(t, e, o)), n;
}

function r(e, t, n) {
    if (t.indexOf("=") >= 0) return "";
    var o = e.data.MY_HOME;
    if (!t || 0 == t.length) {
        var a = o, i = new RegExp("/" + n + "-(.*?)/").exec(a);
        i && i.length > 0 && (t = i[1]);
    }
    return t && t.length > 0 && -1 == t.indexOf("=") && wx.setStorageSync("pkuser", t), 
    t;
}

function s(e, t, n) {
    var o = e.data.MY_HOME, a = new RegExp("/" + n + "-(.*?)/").exec(o);
    return a && a.length > 0 && (t = a[1]), t && t.length > 0 && -1 == t.indexOf("=") && wx.setStorageSync("pkuser", t), 
    t;
}

function d(e) {
    var t = e.data.MY_HOME, n = e.data.Host, o = e.data.SiteID, a = e.data.PKUser, i = o;
    a.length > 0 && (i += "-" + a);
    var r = "https://" + n + ".fooww.com/weizhan-app/" + i + "/", s = "https://" + n + ".fooww.com/weizhan/" + i + "/", d = "https://w.fooww.com/" + n + "/" + i + "/";
    if (!(t.replace("?dev_mode=1", "") == r || t.replace("?dev_mode=1", "") == s || t.replace("?dev_mode=1", "") == d)) return t;
    var u = 1, c = wx.getStorageSync("iscollected");
    return 1 == c || (c || (u = 0), 0 == u && (-1 == t.indexOf("?") ? t += "?" : t += "&", 
    t += "isCollected=" + u)), t;
}

function u(e, t, n) {
    return e ? t.replace(e, e + "-" + n) : t;
}

function c(e, t) {
    return e && t ? t + "house/poster?id=" + e : t;
}

function l(e) {
    if (!e) return "";
    for (var t, n = [], o = e.slice(e.indexOf("?") + 1).split("&"), a = 0; a < o.length; a++) t = o[a].split("="), 
    n.push(t[0]), n[t[0]] = t[1];
    return n;
}

function h(e, t, n) {
    return t && n ? (-1 == e.indexOf("?") ? e += "?" : e += "&", e += t + "=" + n) : e;
}

Page({
    data: {
        MY_HOME: "",
        Host: "",
        SiteID: "",
        PKUser: "",
        CurrentTitle: "",
        logEventData: {}
    },
    bindViewTap: function() {
        wx.navigateTo({
            url: "../../logs/logs"
        });
    },
    onLoad: function(e) {
        var t = this, o = wx.getExtConfigSync(), l = o.attr.siteid, h = o.attr.host, f = decodeURIComponent(e.scene || ""), g = e.housePosterID, p = this;
        if (this.setData({
            SiteID: l,
            Host: o.attr.domain
        }), f) (0, n.GetSceneQRCodeContent)({
            scene: f
        }).then(function(e) {
            if (e.isok && e.data) t.setData({
                MY_HOME: e.data
            }), t.setData({
                PKUser: s(p, f, l)
            }); else {
                var n = function(e, t, n) {
                    var o = t;
                    o = n.indexOf("housePosterID") >= 0 ? c(n.replace("housePosterID=", ""), t) : u(e, t, n);
                    return o;
                }(l, h, f);
                t.setData({
                    MY_HOME: n
                });
            }
        }); else if (g) {
            var v = c(g, h);
            this.setData({
                MY_HOME: v
            });
        } else if (void 0 !== e.url) this.setData({
            MY_HOME: decodeURIComponent(e.url)
        }); else if (void 0 !== e.h) {
            var w = function(e, t, n) {
                var o = t, a = -1, i = "";
                if (!e) return o;
                "zu" == e || "rent" == e || 0 == e ? a = 0 : "shou" == e || "second" == e || 1 == e ? a = 1 : "xin" == e || "new" == e || 2 == e ? a = 2 : e.length > 1 && (a = e.substring(0, 1), 
                i = e.substring(1));
                a >= 0 && !i ? o = t + "/house/list/?ext=h" + a : a >= 0 && i && (o = t + "/house/detail/" + a + "-" + i);
                return o;
            }(e.h, h);
            this.setData({
                MY_HOME: w
            });
        } else {
            var x = i(h, l);
            this.setData({
                MY_HOME: x
            });
        }
        this.setData({
            PKUser: r(this, f, l)
        }), this.setData({
            MY_HOME: d(this)
        }), this.data.MY_HOME || a(this);
    },
    onShow: function(e) {},
    onReady: function(e) {},
    onHide: function(e) {},
    onUnload: function(e) {},
    onPullDownRefresh: function(e) {},
    onReachBottom: function(e) {},
    onPageScroll: function(e) {},
    onError: function(e) {},
    onPageNotFound: function(e) {},
    onShareAppMessage: function(e) {
        var t = !1;
        wx.getSystemInfo({
            success: function(e) {
                t = e.system.toLowerCase().indexOf("android") >= 0;
            }
        });
        var n = wx.getExtConfigSync(), o = e.webViewUrl, a = n.attr.title, i = "", r = function(e, t) {
            var n = l(e = e.replace("#PKHouseVideo", "&PKHouseVideo"));
            if (n.length > 0) {
                var o = t.charAt(0).toUpperCase() + t.slice(1);
                return n[t] || n[o];
            }
            return "";
        }(o, "community"), s = o.toLowerCase(), d = s.indexOf("/house/vr") >= 0 || s.indexOf("/housevr-") >= 0, u = s.indexOf("/house/video") >= 0 || s.indexOf("/housevideo-") >= 0, c = s.indexOf("/user/contract") >= 0 || s.indexOf("/usercontract") >= 0;
        d ? (t || (i = h("https://tool.fooww.com/logo-housevr-share-640x512.png", "_v", Date.parse(new Date()))), 
        r.length > 0 && (a = decodeURI(r) + " 『VR全景』")) : u ? (t || (i = h("https://tool.fooww.com/logo-housevideo-share-640x512.png", "_v", Date.parse(new Date()))), 
        r.length > 0 && (a = decodeURI(r) + " 『视频展示』")) : c ? (i = h("https://tool.fooww.com/logo-contract-share-640x512.png", "_v", Date.parse(new Date())), 
        a = "点击查询最新『合同进度』") : this.data.CurrentTitle.length > 0 && (a = this.data.CurrentTitle), 
        e.from;
        var f = "/pages/index/index?url=" + encodeURIComponent(o);
        return this.addEventLogXCX(1105), {
            title: a,
            path: f,
            imageUrl: i,
            success: function() {
                wx.showToast({
                    title: "分享成功~",
                    icon: "success",
                    duration: 1800
                });
            },
            fail: function() {}
        };
    },
    bindmessage: function(e) {
        var t = e.detail.data;
        t.length > 0 && this.setData({
            CurrentTitle: t[t.length - 1].title,
            logEventData: t[t.length - 1].eventDataForSite
        });
    },
    binderrorLoad: function(e) {
        t.commonLog.sendBinderrorLoadLog(e), a(this);
    },
    bindloading: function(e) {
        this.data.MY_HOME.indexOf("isCollected") >= 0 && wx.setStorageSync("iscollected", 1);
    },
    addEventLogXCX: function(t) {
        this.data.logEventData.curr_page_id && (0, o.addEventLog)({
            pk_user: this.data.pkFoowwUser,
            source_id: 12,
            event_id: t,
            curr_page_id: this.data.logEventData.curr_page_id,
            pre_page_id: this.data.logEventData.pre_page_id,
            event_data: e({}, this.data.logEventData)
        });
    }
});