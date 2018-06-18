var App = App || {};
var $services = {};
(function (options) {
    var version = 0.2;
    if (!(options === undefined)) {
        if (!(options.service === undefined)) {
            for (var i in options.service) {
                $services[options.service[i]] = $services[options.service[i]] || {};
                var file = App.require.script + "services/" + options.service[i] + ".js";
                document.write('<script type="text/javascript" src="' + file + '?v=' + version + '"></scr' + 'ipt>');
            }
        }
    }
    return $services;
})(App.filerequired);