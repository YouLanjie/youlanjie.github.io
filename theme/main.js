// 添加导航栏
(function() {
	function toggleTheme() {
		theme = document.documentElement.getAttribute('theme');
		theme = theme === "dark" ? "light" : "dark"
		document.documentElement.setAttribute('theme', theme);
		localStorage.setItem('theme', theme);
		document.getElementById("theme-toggle-button").innerText = "Theme("+theme+")"
	}
	// 主题切换按钮
	let button = document.createElement('a')
	button.className = "theme-toggle"
	button.id = "theme-toggle-button"
	button.style = "color:var(--fgLink);"
	button.addEventListener('click', toggleTheme)
	theme = localStorage.getItem('theme') || "dark"
	button.innerText = "Theme("+theme+")"
	document.documentElement.setAttribute('theme', theme);

	// 导航栏
	let header = document.createElement('header')
	header.insertAdjacentHTML("beforeend", "<a href='/' alt='home'><img src='/img/icon.jpg' height='35' alt='icon' id='header_icon'/></a>&nbsp;&nbsp;")
	header.insertAdjacentHTML("beforeend", "<a href='/timeline.html'>TimeLine</a>&nbsp;&nbsp;")
	header.insertAdjacentHTML("beforeend", "<a href='/about.html'>About</a>&nbsp;&nbsp;")
	header.insertAdjacentElement("beforeend", button)
	header.role = "navigation"

	let div = document.createElement('div')
	div.id = "preamble"
	div.className = "status"
	div.insertAdjacentElement("afterbegin", header)

	csstheme = localStorage.getItem('csstheme') || "main"
	if (csstheme == "main") {
		document.body.insertAdjacentElement("afterbegin", div)
	}
})();
// 为表格增加父节点
(function() {
	let tables = document.getElementsByTagName('table')
	if ( tables.length == 0 ) {
		return;
	}
	for (let i = 0; i < tables.length; i++) {
		let div = document.createElement("div")
		div.className = "tables"
		tables[i].insertAdjacentElement("beforebegin", div)
		div.insertAdjacentElement("afterbegin", tables[i])
	}
})();
// 为pre增加双击切换严格等宽字体功能
(function() {
	let pres = document.getElementsByClassName("src")
	if ( pres.length == 0 ) {
		return;
	}
	for (let i = 0; i < pres.length; i++) {
		pres[i].addEventListener("dblclick", function(event) {
			if (event.currentTarget.classList.contains('monofont')) {
				event.currentTarget.classList.remove("monofont")
			} else {
				event.currentTarget.classList.add("monofont")
			}
		})
	}
})();
// 为footnote增加双击footnote侧栏展开功能
(function() {
	let fn = document.getElementById("footnotes")
	if ( ! fn ) {
		return;
	}
	fn.addEventListener("dblclick", function(event) {
		sty = window.getComputedStyle(event.currentTarget)
		if (sty.position != "fixed") {
			return
		}
		if (fn.style.maxWidth == "") {
			fn.style.maxWidth = "98%"
			fn.style.top = "2%"
			fn.style.zIndex = 1
		} else {
			fn.style = ""
		}
	})
})();
// 为图片增设fancybox效果
(function() {
	var script = document.createElement("script")
	script.setAttribute("type", "text/javascript");
	// script.setAttribute("src", "https://cdn.jsdelivr.net/npm/@fancyapps/ui/dist/fancybox.umd.js")
	// script.setAttribute("src", "https://cdn.jsdelivr.net/npm/@fancyapps/ui/dist/fancybox/fancybox.umd.js")
	script.setAttribute("src", "/theme/fancybox.umd.js")

	var link = document.createElement("link")
	link.setAttribute("rel", "stylesheet")
	link.setAttribute("href", "/theme/fancybox.css")
	// link.setAttribute("href", "https://cdn.jsdelivr.net/npm/@fancyapps/ui/dist/fancybox.css")

	document.getElementsByTagName("head")[0].appendChild(link)
	document.getElementsByTagName("head")[0].appendChild(script)

	window.onload = function() {
		Fancybox.bind('[data-fancybox]', {})
	}

	let imgs = document.getElementsByTagName("img")
	if ( imgs.length == 0 ) {
		return;
	}
	for (let i = 0; i < imgs.length; i++) {
		if (imgs[i].id == "header_icon") {
			continue
		}
		imgs[i].setAttribute("data-fancybox", "gallery")
	}
})();

function setTheme(theme_name) {
	if (!theme_name in ["main", "ohtd", "rtd"]) {
		theme_name = "main"
	}
	localStorage.setItem('csstheme', theme_name);
	document.getElementById("thname").innerText = localStorage.getItem('csstheme')
}
// 切换css主题
(function() {
	csstheme = localStorage.getItem('csstheme') || "main"

	if (csstheme != "main") {
		links = document.head.getElementsByTagName("link")
		for (let i = 0; i < links.length; i++) {
			if (links[i].href.endsWith("/theme/main.css")) {
				document.head.removeChild(links[i])
				break
			}
		}
	}
	if (csstheme == "ohtd") {
		document.head.insertAdjacentHTML("beforeend", '<link rel="stylesheet" type="text/css" href="/theme/org-html-theme-dull/org-html-theme-dull.css"/>')
		let script = document.createElement("script")
		script.type = "text/javascript"
		script.src = "/theme/org-html-theme-dull/org-html-theme-dull.js"
		document.head.insertAdjacentElement("beforeend", script)
	}
	if (csstheme == "rtd") {
		document.head.insertAdjacentHTML("beforeend", '<link rel="stylesheet" type="text/css" href="/theme/read_the_docs/css/htmlize.css"/>')
		document.head.insertAdjacentHTML("beforeend", '<link rel="stylesheet" type="text/css" href="/theme/read_the_docs/css/readtheorg.css"/>')
		urls = ["/theme/read_the_docs/jquery.min.js","/theme/read_the_docs/bootstrap.min.js",
			"/theme/read_the_docs/js/jquery.stickytableheaders.min.js", "/theme/read_the_docs/js/readtheorg.js"]
		for (let i = 0; i < urls.length; i++) {
			let script = document.createElement("script")
			script.type = "text/javascript"
			script.src = urls[i]
			document.head.insertAdjacentElement("beforeend", script)
		}
	}
})();

// 切换css字体
function setFont(font_name) {
	if (!font_name in ["Serif", "Sans"]) {
		font_name = "Serif"
	}
	localStorage.setItem('cssfont', font_name);
	document.getElementById("ftname").innerText = localStorage.getItem('cssfont')
}
(function() {
	cssfont = localStorage.getItem('cssfont') || "Sans"
	console.log("cssf:"+cssfont);
	if (cssfont == "Serif") {
		document.head.insertAdjacentHTML("beforeend","<style>#content{font-family:'Noto Serif CJK SC', 'serif'}</style>")
	}
})();
