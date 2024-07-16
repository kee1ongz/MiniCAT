var e = require("@babel/runtime/helpers/interopRequireDefault.js").default;

Object.defineProperty(exports, "__esModule", {
    value: !0
}), exports.GetLogEventData = function(e) {
    return (0, t.default)({
        url: "/api/logEvent/getLogEventData",
        method: "post",
        data: e
    });
}, exports.addEventLog = function(e) {
    return (0, t.default)({
        url: "/api/logEvent/addLog",
        method: "post",
        data: e
    });
};

var t = e(require("9BA18D97E8E8E88CFDC7E590C2E4A813.js"));