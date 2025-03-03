
function showLineInfo( message = '' ) {
	const e = new Error();
	const stack = e.stack.split('\n');
	
	const lineInfo = stack[2].trim();
	console.log( `${message} LINE Executing at: ${lineInfo}` );
	}
async function getCredentials(  ) {
	
	try {
	
		const response = await fetch(addAPIKEY('/api/get-credentials'), { headers: { 'Cache-Control': 'no-cache' } });
		if (!response.ok){
			throw new Error('Network response was not ok');
		}
			
	const text = await response.text();
		let data = JSON.parse(text);
		let L = data.result.length;
		if( data.result[L-1].type === 'BLANK'  )
		{
			return JSON.parse(   '[]'   ) ;
		}else{
			return data.result;
			}
		
	} catch (error) {
		
		console.info('EMPTY WALLET ON SERVER :', error);
		
		return JSON.parse(   '[]'   ) ;
		}
	}


	

	
async function Confirmation ( prompt , callback ) {
	var result = confirm( prompt  );
	
	if( result  )
	{
		return callback() ;
	}else{
		ReLoad(  ) ;
		return;
		}
	}
async function SaveJSONdata(USER_ID, ITEMS) {
	const payload = { userId: USER_ID,  files: ITEMS };
	
	
	
	const saveResponse = await fetch( addAPIKEY( '/api/save-credentials' )  , { method: 'POST',headers: {'Content-Type': 'application/json' },body: JSON.stringify(payload) });
	
	if (!saveResponse.ok) {
	throw new Error(`Save failed: ${saveResponse.status}`);
		}
	const result = await saveResponse.json();
	
	if (!result.success) {
	throw new Error(result.message || 'Save operation failed');
		}
	
	return result.result ;
}
async function sendEmailData( userID , subject='From AMW' , reload = false ) {
	var  URI =  addAPIKEY( '/api/send-checked-credentials' ) ;
	
	URI +=  `&subject=${ subject }` ;
	
	var prompt =  `Confirm emailing ${numChecked()} selected documents to ${userID}.` ;
	var result = confirm(  prompt  );
	if( result  )
	{
	}else{
		return;
		}
	try {
	
		const response = await fetch( URI, { method: 'GET'  });
		const result = await response.json();
		
		alert(  'Credentials email sent'   ) ;
		if( reload  )
		{
			ReLoad(  ) ;
			
			}
	} catch (error) {
		console.error('Error sending email :', error);
		}
	}
function extractNumberAsText(inputString) {
	if (!inputString) {
	
		return '';
		}
	
	const matches = inputString.match(/\d+(\.\d+)?/);
	if (matches) {
	
		return   Number(matches[0]).toString();
	} else {
		return '';
		}
	}
function popPage( page ) {
	url  = `${page}?userId=${USER_ID}&apikey=${ APIKEY }` ;
	
	window.open(url, '_blank');
	return false;
	}


function generateFolderName(email) {
	
	const invalidChars = /[<>:"/\\|?*\s]+/g;
	
	let sanitizedEmail = email.replace(invalidChars, "_");
	
	const timestamp = new Date().getTime();
	const uniqueFolderName = `${sanitizedEmail}`;
	
	return uniqueFolderName;
	}
function togglePopup( message ) {
	var popup = document.getElementById("myPopup");
	popup.classList.toggle("show");
	}
function toggleHelp( ID) {
	alert( 'help toggle ' +  ID   ) ;
	var popup = document.getElementById( ID );
	popup.classList.toggle("show");
	}
let userData;
async function getUserData( user = '' ) {
	
	var response;
	var url ;
	try {
	
		if( user!= ''   )
		{
			url = addAPIKEY( `/api/get-user?userId=${user}` )
		}else{
			url = addAPIKEY( `/api/get-user` ) ;
			}
		
		response = await fetch(  url  );
		const data = await response.json();
		userData = data.result;
		
		
	} catch (error) {
		console.error("Error getUser profile:", error);
		}
	
	return userData ;  }
function Load( url  ) {
	var start_page = addAPIKEY(  url ) ;
	console.error(  "START PAGE SET TO ", start_page   ) ;
	location.replace( start_page  ) ;
	}
function ReLoad( ) {
	
	var start_page = addAPIKEY(  location.href ) ;
	console.error(  "START PAGE SET TO ", start_page   ) ;
	
	}
async function deleteChecked( user ){
	hitEndPoint( addAPIKEY(  '/api/remove-checked-credentials' ) , USER_ID, [], true)
	
	console.error('remove-checked-credentials FileStates:'  ) ;
	
	
	}
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
function updateChecked( user ){
	hitEndPoint(  '/api/update-checked-credentials' , USER_ID, [], true)
	console.error('update-checked-credentials FileStates:' , FileStates) ;
	AI_process_Data();setTimeout(function(){location.reload();},1000);
	}
window.onload = async function init() {
	
	return;
}
//  Export  Date: 12:44:54 PM - 22:Feb:2025...

