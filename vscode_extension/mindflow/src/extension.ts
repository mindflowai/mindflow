// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "mindflow" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	let disposable = vscode.commands.registerCommand('mindflow.query', () => {
		// The code you place here will be executed every time your command is executed
		// Display a message box to the user
		vscode.window.showInformationMessage('Hello World from mindflow!');
			
		// If there is no active terminal, create a new one
		if (!vscode.window.activeTerminal) {
			vscode.window.createTerminal();
		}


		// Open a search bar that is overlaying the current editor
		vscode.window.showInputBox({
			placeHolder: "Search for a note",
			prompt: "Search for a note",
			ignoreFocusOut: true
		}).then((value) => {
			// treat the value as a command and execute it in the terminal

			if (!value) {
				return;
			}

			let terminal = vscode.window.activeTerminal;

			// If there is no active terminal, create a new one
			if (!terminal) {
				terminal = vscode.window.createTerminal();
			}

			terminal.sendText(value);
			// console.log(value);

			
		});
	});

	context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
export function deactivate() {}
