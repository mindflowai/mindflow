// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';



// function openQuery() {
// 	const editor = vscode.window.activeTextEditor;

// 	if (!editor) {
// 		return;
// 	}

// 	const decorationType = vscode.window.createTextEditorDecorationType({
// 		backgroundColor: 'green',
// 		border: '2px solid white',
// 	});

// 	let sourceCode = editor.document.getText()
// 	// let regex = /(console\.log)/
  
// 	let decorationsArray: vscode.DecorationOptions[] = []

// 	let decoration = { range: new vscode.Range(0, 0, 0, 0) }

// 	decorationsArray.push(decoration)
  
// 	// const sourceCodeArr = sourceCode.split('\n')
  
// 	// for (let line = 0; line < sourceCodeArr.length; line++) {
// 	//   let match = sourceCodeArr[line].match(regex)
  
// 	//   if (match !== null && match.index !== undefined) {
// 	// 	let range = new vscode.Range(
// 	// 	  new vscode.Position(line, match.index),
// 	// 	  new vscode.Position(line, match.index + match[1].length)
// 	// 	)
  
// 	// 	let decoration = { range }
  
// 	// 	decorationsArray.push(decoration)
// 	//   }
// 	// }
  
// 	editor.setDecorations(decorationType, decorationsArray)
//   }

// function openQuery() {
// 	vscode.window.activeTextEditor?.setDecorations

// 	// If there is no active terminal, create a new one
// 	if (!vscode.window.activeTerminal) {
// 		vscode.window.createTerminal();
// 	}

// 	// Open a search bar that is overlaying the current editor
// 	vscode.window.showInputBox({
// 		placeHolder: "Search for a note",
// 		prompt: "Search for a note",
// 		ignoreFocusOut: true
// 	}).then((value) => {
// 		// treat the value as a command and execute it in the terminal

// 		if (!value) {
// 			return;
// 		}

// 		let terminal = vscode.window.activeTerminal;

// 		// If there is no active terminal, create a new one
// 		if (!terminal) {
// 			terminal = vscode.window.createTerminal();
// 		}

// 		terminal.sendText(value);
// 		// console.log(value);

		
// 	});
// }


function openQuery() {
	// If there is no active terminal, create a new one
	if (!vscode.window.activeTerminal) {
		vscode.window.createTerminal();
	}
	
	// Create a new webview panel that overlays the current editor
	// const panel = vscode.window.createWebviewPanel(
	// 	'myWebview', // Identifies the type of the webview. Used internally
	// 	"My Webview", // Title of the panel displayed to the user
	// 	vscode.ViewColumn.One, // Editor column to show the new webview panel in.
	// 	{
	// 		enableScripts: true, // Allow scripts in the webview
	// 		// preserveFocus: true, // Do not take focus when the webview is shown
	// 		// preserveFocus: true
	// 	},
	// );
  
	// // Set the HTML content of the webview panel
	// panel.webview.html = `
	
	// <html>
	// <body>
	
	// <!-- This is a large input text box -->
	// <input type="text" style="width: 100%; height: 50px;">
	
	// </body>
	// </html>

	// `;
  
	// // Show the webview panel
	// panel.reveal();

	// let uri = new vscode.Uri

	// vscode.window.openTextDocument({
	// content: 'This is some pre-populated text.'
	// }).then(doc => {
	// vscode.window.showTextDocument(doc).then(editor => {
	// 	// Open the editor in Vim mode
	// 	vscode.commands.executeCommand('setEditorMode', {
	// 	editor,
	// 	mode: 'vim'
	// 	});
	// });
	// });

	// Open a new text editor window and pre-populate it with some text and give it a filename

	// create a new file

	// vscode.workspace.fs.writeFile(vscode.Uri.file('test.md'), new Uint8Array([1, 2, 3])).then(() => {

	// 	// open the file in the editor
	// 	vscode.window.showTextDocument(vscode.Uri.file('test.md'));
	// });
	
	// show open dialog and choose multiple files
	vscode.window.showOpenDialog({
		canSelectMany: true,
		canSelectFolders: false,
		canSelectFiles: true,
		openLabel: "Select",
		// filters: {
			// 'Images': ['png', 'jpg'],
			// 'TypeScript': ['ts', 'tsx'],
			// 'JavaScript': ['js', 'jsx']
	}).then((value) => {
		// console.log(value);

		// get the paths of the selected files
		let paths = value?.map((uri) => {
			return uri.path;
		});

		// console.log(paths);

		// Open an input text box that is overlaying the current editor
		vscode.window.showInputBox({
			placeHolder: "Can you summarize this information as thoroughly as possible?",
			prompt: "What would you like to know about these files?",
			ignoreFocusOut: true,
		}).then((queryString) => {
			let terminal = vscode.window.activeTerminal;

			// If there is no active terminal, create a new one
			if (!terminal) {
				terminal = vscode.window.createTerminal();
			}

			terminal.sendText("mf query \"" + queryString + "\" " + paths?.join(" ") + " -s");
		});

		// console.log(value);
	});
  }

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "mindflow" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	let disposable = vscode.commands.registerCommand('mindflow.query', openQuery);

	context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
export function deactivate() {}
