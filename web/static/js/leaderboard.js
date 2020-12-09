var per = 25;
var page = 1;
var state = {};
var lastPage = page;
var xhr = new XMLHttpRequest();
var table = document.getElementById('board');

function updateState() {
	xhr.open('GET', '/api/public/leaderboard/' + per + '/' + page);
	xhr.send();
}

function prevPage() {
	lastPage = page;
	page -= 1;
	updateState();
}

function nextPage() {
	lastPage = page;
	page += 1;
	updateState();
}

xhr.onerror = () => console.log('request failed');

xhr.onload = () => {
	if (xhr.status != 200) {
		console.log('leaderboard API bad response');
		page = lastPage;
		return;
	} else {
		state = JSON.parse(xhr.response);
		updateBoard();
	}
}

function updateBoard() {

	// parse the response and set the subheading
	let sub = document.getElementById('sub');
	let p = '';
	if (Number(state.teams) > per) {
		p = ', ' + state.pages + ' pages' + ' (with ' + per + ' teams per page)'
		document.getElementById('controls').style.display = 'block';
	} else {
		document.getElementById('controls').style.display = 'none';
	}
	sub.innerHTML = state.teams  + ' teams participating' + p;
	let num = document.getElementById('page');
	num.innerHTML = page;

	// clear table and set header
	while (table.firstChild) {
		table.removeChild(table.firstChild);
	}
	let row = document.createElement('tr');
	let id = document.createElement('td'); id.innerHTML = 'Team ID';
	let points = document.createElement('td'); points.innerHTML = 'Points';
	let start = document.createElement('td'); start.innerHTML = 'Started';
	row.appendChild(id);
	row.appendChild(points);
	row.appendChild(start);
	table.appendChild(row);

	// insert table data
	for (const place in state.board) {
		let row = document.createElement('tr');
		row.onclick = () => location.href='/api/public/team/' + state.board[place].id;
		let id = document.createElement('td'); id.innerHTML = state.board[place].id;
		let points = document.createElement('td'); points.innerHTML = state.board[place].points;
		let start = document.createElement('td'); start.innerHTML = state.board[place].start;
		row.appendChild(id);
		row.appendChild(points);
		row.appendChild(start);
		table.appendChild(row);
	}
}

updateState();
