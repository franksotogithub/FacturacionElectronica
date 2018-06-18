var App = App || {};
(function (App) {
    App.obj = {};
    var require = (function () {
        function require() {
            var version = 20;
            this.base_url = "http://localhost:8051/";
            this.server = "http://localhost:8051/";
            this.script = this.base_url + "static/custom/js/scripts/";
            this.requiredFiles = ['utils.js', 'services.js'];

            this.requireobj = [];
			this.dowload = function(path, requires){
                for (i in this.requiredFiles ) {
                    var file =  this.requiredFiles[i];
                    document.write('<scr' + 'ipt type="text/javascript" src="' + path + file + '?v=' + version + '"></scr' + 'ipt>');
                }


			};

			// ejecutamos tareas internas del objeto
			this.dowload(this.script);
        }
        return require;
    })();

	var init = (function(){
		function init(options) {
            this.options = options;
            var keys = Object.keys(this.options);
            this.table = {};
            this.service = {};
            this.alert;

            /* ejecutamos los init de los requeridos */
            if(keys.indexOf('utils') >= 0) {
                $utils.init(this.options['utils']);
            }

            /* llama todos los metodos */
            var require = App.require;
            for (i in require.requireobj) {
                var key = $.trim(require.requireobj[i]);
                if(keys.indexOf(key) >= 0) {
                    this[key] = require.scriptsFiles[key].object(this.options[key]);
                }else {
                    this[key] = require.scriptsFiles[key].object();
                }
            }
		}
		return init;
	})();

	App.init = init;
    App.require = new require();

})(App || (App = {}));
