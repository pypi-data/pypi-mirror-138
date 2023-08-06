// Be careful editing the contents of this file!

/** @param {URL} url */
function loadCss(url) {
	var link = document.createElement("link");
	link.type = "text/css";
	link.rel = "stylesheet";
	link.href = url.href;
	document.getElementsByTagName("head")[0].appendChild(link);
}

define(["@jupyter-widgets/base"], function (base) {
	return import("./widget.js").then(mod => {
		loadCss(new URL("./widget.css", mod.importMeta));
		return mod.default(base)
	});
})
