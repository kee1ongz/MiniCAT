Page({
    data: {
        array: [ {
            message: "foo"
        }, {
            message: "bar"
        } ],
        array1: [ {
            message: "foo1"
        }, {
            message: "bar1"
        } ],
        phone: "18254121538"
    },
    onLoad: function(o) {
        console.log("id:" + o.query);
        var e = this.getOpenerEventChannel();
        e.emit("acceptDataFromOpenedPage", {
            data: "test"
        }), e.emit("someEvent", {
            data: "test"
        }), e.on("acceptDataFromOpenerPage", function(o) {
            console.log(o);
        }), wx.login({
            success: function(o) {
                o.code ? console.log("获取code成功" + o.code) : console.log("登录失败！" + o.errMsg);
            }
        });
    },
    onReady: function() {},
    onShow: function() {},
    onHide: function() {},
    onUnload: function() {},
    onPullDownRefresh: function() {},
    onReachBottom: function() {},
    onShareAppMessage: function() {},
    jumpToWeizhan: function() {
        wx.navigateTo({
            url: "/pages/index/index?url=https://rikaze.fooww.com/weizhan/230008647/houseList-1-0-0-0-0-0-0-0-0-0-0-.aspx"
        });
    },
    jumpToUcard: function() {
        this.setData({
            array: this.data.array1
        }), console.log("daf"), wx.navigateToMiniProgram({
            appId: "wxff896b72df04748f"
        });
    },
    Login: function(o) {
        wx.login({
            success: function(o) {
                o.code ? (console.log("获取code成功" + o.code), wx.request({
                    url: "https://test-webapi.fooww.com/api/WeiXinGeteway/Custom/GetWxUserInfo",
                    data: {
                        code: o.code
                    }
                })) : console.log("登录失败！" + o.errMsg);
            }
        });
    },
    getPhoneNumber: function(o) {
        console.log(o.detail.errMsg), console.log(o.detail.iv), console.log(o.detail.encryptedData), 
        wx.login({
            success: function(e) {
                e.code ? (console.log("获取code成功" + e.code), wx.request({
                    url: "https://test-webapi.fooww.com/api/WeiXinGeteway/Custom/GetWxUserInfo",
                    data: {
                        code: e.code,
                        iv: o.detail.iv,
                        encryptedData: o.detail.encryptedData
                    },
                    header: {
                        "content-type": "application/json"
                    },
                    success: function(o) {
                        console.log(o.data);
                    }
                })) : console.log("登录失败！" + e.errMsg);
            }
        });
    },
    CallPhone: function() {
        wx.makePhoneCall({
            phoneNumber: this.data.phone,
            success: function() {
                console.log("调起拨打成功回调");
            },
            fail: function(o) {
                console.log(o);
            },
            complete: function(o) {
                console.log(o);
            }
        });
    }
});