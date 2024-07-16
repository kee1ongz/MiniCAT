var e = require("@babel/runtime/helpers/interopRequireDefault.js").default;

Object.defineProperty(exports, "__esModule", {
    value: !0
}), exports.GetSceneQRCodeContent = function(e) {
    return (0, t.default)({
        url: "/api/WeixinGateway/SceneQRCode/GetContent",
        method: "GET",
        params: e
    });
};

var t = e(require("F0A5C602E8E8E88C96C3AE0501D4A813.js"));