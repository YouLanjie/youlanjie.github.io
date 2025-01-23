(function() {
	let header = document.createElement('header')
	header.insertAdjacentHTML("beforeend", "<a href='/'><img src='/img/icon.jpg' height='35'/></a>")
	header.insertAdjacentHTML("beforeend", "<a href='/'>   Home   </a>")
	header.insertAdjacentHTML("beforeend", "<a href='/src/post.html'>   Blog   </a>")
	header.insertAdjacentHTML("beforeend", "<a href='/src/timeline.html'>   TimeLine   </a>")
	header.insertAdjacentHTML("beforeend", "<a href='/about.html'>   About   </a>")
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
