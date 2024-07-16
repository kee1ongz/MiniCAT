App({
    onLaunch: function(o) {},
    onShow: function(o) {},
    onHide: function() {},
    onError: function(o) {
        console.log("app onError"), wx.redirectTo({
            url: "pages/index/index"
        });
    },
    globalData: null,
    onPageNotFound: function(o) {
        console.log("app onPageNotFound"), wx.redirectTo({
            url: "pages/index/index"
        });
    }
});