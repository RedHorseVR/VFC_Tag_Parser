// === Final Pretty Printed Code ===
function showLineInfo(message = '') {
	const e = new Error();
	const stack = e.stack.split('\n');

	const lineInfo = stack[2].trim();
	console.log(`${message} LINE Executing at: ${lineInfo}`);
}
async function getCredentials() {
	try {
		const response = await fetch(addAPIKEY('/api/get-credentials'), {
			headers: { 'Cache-Control': 'no-cache' },
		});
		if (!response.ok) {
			throw new Error('Network response was not ok');
		}

		const text = await response.text();
		let data = JSON.parse(text);
		let L = data.result.length;
		if (data.result[L - 1].type === 'BLANK') {
			return JSON.parse('[]');
		} else {
			return data.result;
		}
	} catch (error) {
		console.info('EMPTY WALLET ON SERVER :', error);
		return JSON.parse('[]');
	}
}

async function Confirmation(prompt, callback) {
	var result = confirm(prompt);

	if (result) {
		return callback();
	} else {
		ReLoad();
		return;
	}
}

function togglePopup(message) {
	var popup = document.getElementById('myPopup');
	popup.classList.toggle('show');
}
function toggleHelp(ID) {
	alert('help toggle ' + ID);
	var popup = document.getElementById(ID);
	popup.classList.toggle('show');
}
let userData;

async function loadJsonFile() {
	try {
		const response = await fetch(JSON_FILE);
		if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

		data = await response.json();
		window.credentials = data;

		return true;
	} catch (error) {
		console.error(`INFO Error loading JSON:`, error);
		showLineInfo();

		sessionStorage.setItem('sessionAIprocessing', 'false');

		return false;
	}
}
function updateChecked(user) {
	hitEndPoint('/api/update-checked-credentials', USER_ID, [], true);
	console.error('update-checked-credentials FileStates:', FileStates);
	AI_process_Data();
	setTimeout(function () {
		location.reload();
	}, 1000);
}
window.onload = async function init() {
	return;
};
//  Export  Date: 12:44:54 PM - 22:Feb:2025...
