(function() {
	function toggleTheme() {
		theme = document.documentElement.getAttribute('theme');
		theme = theme === "dark" ? "light" : "dark"
		document.documentElement.setAttribute('theme', theme);
		localStorage.setItem('theme', theme);
		document.getElementById("theme-toggle-button").innerText = "Theme("+theme+")"
	}
	let button = document.createElement('a')
	button.className = "theme-toggle"
	button.id = "theme-toggle-button"
	button.style = "color:var(--fgLink);"
	button.addEventListener('click', toggleTheme)
	theme = localStorage.getItem('theme') || "dark"
	button.innerText = "Theme("+theme+")"
	document.documentElement.setAttribute('theme', theme);

	let header = document.createElement('header')
	header.insertAdjacentHTML("beforeend", "<a href='/' alt='home'><img src='/img/icon.jpg' height='35' alt='icon'/></a>&nbsp;&nbsp;")
	header.insertAdjacentHTML("beforeend", "<a href='/timeline.html'>TimeLine</a>&nbsp;&nbsp;")
	header.insertAdjacentHTML("beforeend", "<a href='/about.html'>About</a>&nbsp;&nbsp;")
	header.insertAdjacentElement("beforeend", button)
	header.role = "navigation"

	let div = document.createElement('div')
	div.id = "preamble"
	div.className = "status"
	div.insertAdjacentElement("afterbegin", header)
	document.body.insertAdjacentElement("afterbegin", div)
})();
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
(function() {
	console.log("TEST!!!!")
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
