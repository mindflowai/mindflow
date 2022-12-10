// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';


function openQuery() {
	// If there is no active terminal, create a new one
	if (!vscode.window.activeTerminal) {
		vscode.window.createTerminal();
	}
	
	// show open dialog and choose multiple files/folders
	vscode.window.showOpenDialog({
		canSelectMany: true,
		canSelectFolders: true,
		canSelectFiles: true,
		openLabel: "Select Files to use as Query Context",
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
