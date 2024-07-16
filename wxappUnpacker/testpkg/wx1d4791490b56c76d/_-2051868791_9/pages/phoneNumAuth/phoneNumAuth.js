var a = require("../../@babel/runtime/helpers/objectSpread2");

require("../../@babel/runtime/helpers/Arrayincludes");

var t = require("../../54D671E4E8E8E88C32B019E36494A813.js");

Page({
    data: {
        showPrivacy: !1,
        hasViewPrivacy: !1,
        domain: "webapi.fooww.com",
        name: "欢迎光临",
        nextPage: "",
        pkFoowwUser: "",
        pkCompany: "",
        loginStatus: 2,
        backText: "",
        wxPrivacyTitle: "",
        privacyInfo: {
            privacyTitle: "",
            privacyContent: [ "", "" ],
            privacyName: "",
            privacyUrl: "",
            privacyPolicyUrl: "",
            privacyTitleFilter: []
        },
        logEventData: {
            pkFoowwUser: "",
            pkWeizhan: "",
            nickName: "",
            openId: "",
            iShareStatus: ""
        },
        logEventDataOptions: {}
    },
    onLoad: function(a) {
        var t = this;
        this.setData({
            backText: "1" === "".concat(a.loginStatus) ? "跳过" : "返回",
            loginStatus: parseInt(a.loginStatus),
            nextPage: a.lastFromUrl,
            beforFromUrl: a.beforFromUrl,
            pkCompany: a.pkCompany,
            pkFoowwUser: a.pkFoowwUser,
            cellphone: a.cellphone,
            logEventData: {
                pkFoowwUser: a.pkFoowwUser,
                beforFromUrl: decodeURIComponent(a.beforFromUrl),
                pkWeizhan: a.pkWeizhan,
                nickName: a.nickName,
                openId: a.openId,
                iShareStatus: a.iShareStatus
            }
        }), wx.getPrivacySetting({
            success: function(a) {
                a.needAuthorization && t.setData({
                    wxPrivacyTitle: a.privacyContractName ? a.privacyContractName : ""
                }), t.getPrivacyProtocolInfo();
            },
            fail: function() {}
        }), this.getEventDataForSite(), wx.onNeedPrivacyAuthorization(function(a) {
            t.setData({
                showPrivacy: !0
            }), t.resolvePrivacyAuthorization = a;
        });
        var e = [ "develop", "trial" ].includes(wx.getAccountInfoSync().miniProgram.envVersion);
        this.setData({
            domain: e ? "test-" + this.data.domain : this.data.domain
        });
    },
    handleAgreePrivacyAuthorization: function() {
        this.resolvePrivacyAuthorization({
            buttonId: "agree-auth-btn",
            event: "agree"
        }), this.setData({
            showPrivacy: !1
        });
    },
    handleDisagreePrivacyAuthorization: function() {
        this.resolvePrivacyAuthorization({
            event: "disagree"
        }), this.setData({
            showPrivacy: !1
        });
    },
    onShareAppMessage: function(a) {
        return "button" !== a.from && this.addEventLogXCX(1105, {
            share_type: 1
        }), {
            title: "在线预约看房",
            path: "/pages/index/index"
        };
    },
    backTap: function() {
        this.addEventLogXCX(1129), "2" === "".concat(this.data.loginStatus) ? wx.redirectTo({
            url: "/pages/index/index?url=" + this.data.beforFromUrl
        }) : "1" === "".concat(this.data.loginStatus) && wx.redirectTo({
            url: "/pages/index/index?url=" + this.data.nextPage
        });
    },
    getEventDataForSite: function() {
        var e = this;
        (0, t.GetLogEventData)({
            pkWeizhan: this.data.logEventData.pkWeizhan,
            currentPageUrl: "_Pages_phoneNumAuth",
            prePageUrl: this.data.logEventData.beforFromUrl,
            isXCX: 1
        }).then(function(t) {
            if (t.isok) {
                var i = e.data.logEventData;
                e.setData({
                    logEventDataOptions: a(a({}, t.data), {}, {
                        nick_name: i.nickName,
                        pk_fooww_user: i.pkFoowwUser,
                        open_id: i.openId
                    })
                });
            }
        });
    },
    addEventLogXCX: function(e, i) {
        (0, t.addEventLog)({
            pk_user: this.data.pkFoowwUser,
            source_id: 12,
            event_id: e,
            curr_page_id: this.data.logEventDataOptions.curr_page_id,
            pre_page_id: this.data.logEventDataOptions.pre_page_id,
            event_data: a(a({}, this.data.logEventDataOptions), i)
        });
    },
    addEventLogXCX_1126: function() {
        this.addEventLogXCX(1126);
    },
    sendGetPhoneErrorMessage: function(a, t) {
        var e = this, i = wx.getAccountInfoSync().miniProgram.appId;
        wx.request({
            url: "https://" + e.data.domain + "/api/AddWeizhanVisitorCellphonesBadLog",
            method: "post",
            data: {
                PKCompany: e.data.pkCompany,
                PKFoowwUser: e.data.pkFoowwUser,
                ExtAppid: i,
                ExtOpenID: e.data.logEventData.openId,
                IPKUser: "",
                LastFromUrl: e.data.nextPage,
                EventType: -1,
                ExtErrorMessage: t
            },
            success: function() {},
            fail: function() {}
        });
    },
    getPhoneNumber: function(a) {
        var t = this;
        if (a.detail.errno && a.detail.errno > 0) {
            var e = this;
            if ("1400001" === "".concat(a.detail.errno)) return wx.showModal({
                title: "",
                showCancel: !0,
                confirmText: "立即拨打",
                content: "请拨打电话，为您提供更多服务~",
                success: function(a) {
                    a.confirm && wx.makePhoneCall({
                        phoneNumber: e.data.cellphone
                    });
                }
            }), void this.sendGetPhoneErrorMessage(a, JSON.stringify(a.detail));
        }
        if ("getPhoneNumber:ok" == a.detail.errMsg) {
            this.addEventLogXCX(1128);
            var i = wx.getAccountInfoSync().miniProgram.appId;
            wx.login({
                success: function(e) {
                    var o = a.detail.iv, n = a.detail.encryptedData, r = t;
                    wx.request({
                        url: "https://" + r.data.domain + "/api/Visitor/Login/BindCellphone",
                        method: "post",
                        data: {
                            appid: i,
                            code: e.code,
                            encryptedData: n,
                            iv: o,
                            pkFoowwUser: r.data.pkFoowwUser,
                            pkCompany: r.data.pkCompany,
                            lastFromUrl: r.data.nextPage,
                            eventType: 1,
                            weizhanXCXMode: 2,
                            weizhanAPPID: 1
                        },
                        success: function(a) {
                            a.data.isok ? wx.redirectTo({
                                url: "/pages/index/index?url=" + r.data.nextPage
                            }) : wx.showToast({
                                title: "授权失败，请重试",
                                icon: "none"
                            });
                        }
                    });
                }
            });
        } else (a.detail.errMsg.indexOf("denied") > -1 || a.detail.errMsg.indexOf("deny") > -1) && (this.addEventLogXCX(1127), 
        wx.showToast({
            title: "您拒绝了手机号授权登录，部分功能将无法使用",
            icon: "none"
        }));
    },
    getPrivacyProtocolInfo: function() {
        var a = this;
        wx.request({
            url: "https://" + a.data.domain + "/api/Weizhan/Common/GetCommonSetting" + "?weizhanXCXMode=2&pkCompany=".concat(this.data.pkCompany),
            method: "get",
            data: {},
            success: function(t) {
                var e = t.data;
                if (e.isok) {
                    var i = a.data.wxPrivacyTitle || e.data.privacyTitleDefault || "用户隐私保护指引";
                    e.data.privacyTitleFilter.forEach(function(a) {
                        i = i.replaceAll(a, "");
                    });
                    var o = e.data.privacyContent ? e.data.privacyContent.split("{PrivacyName}") : [ "", "" ], n = a.data.wxPrivacyTitle || i;
                    a.setData({
                        privacyInfo: {
                            privacyTitle: i,
                            privacyName: n,
                            privacyContent: o,
                            privacyUrl: e.data.privacyUrl,
                            privacyPolicyUrl: e.data.privacyPolicyUrl,
                            privacyTitleFilter: e.data.privacyTitleFilter
                        }
                    });
                }
            }
        });
    },
    openprivacyPolicyUrl: function() {
        this.data.privacyInfo.privacyPolicyUrl ? wx.navigateTo({
            url: "/pages/index/index?url=" + this.data.privacyInfo.privacyPolicyUrl
        }) : wx.showToast({
            title: "获取隐私协议失败，请退出重新进入小程序",
            icon: "none"
        });
    },
    openPrivacyUrl: function() {
        this.data.privacyInfo.privacyUrl ? wx.navigateTo({
            url: "/pages/index/index?url=" + this.data.privacyInfo.privacyUrl
        }) : wx.showToast({
            title: "获取隐私协议失败，请退出重新进入小程序",
            icon: "none"
        });
    },
    notAuthNotification: function() {
        wx.showToast({
            title: "请先阅读并勾选隐私协议",
            icon: "none"
        });
    },
    changeHasViewPrivacy: function() {
        this.setData({
            hasViewPrivacy: !this.data.hasViewPrivacy
        });
    }
});