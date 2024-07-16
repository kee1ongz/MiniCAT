var t = require("../../E49FED46E8E8E88C82F9854141F4A813.js");

Page({
    data: {
        logs: []
    },
    onLoad: function() {
        this.setData({
            logs: (wx.getStorageSync("logs") || []).map(function(a) {
                return t.formatTime(new Date(a));
            })
        });
    }
});