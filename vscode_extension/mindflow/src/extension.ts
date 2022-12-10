// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import path = require('path');
import { TextEncoder } from 'util';


function openTextFileQuery() {

	// vscode.workspace.openTextDocument({
	// 	content: "Can you summarize this information as thoroughly as possible?",
	// 	language: "plaintext"
	// }).then((doc) => {
	// 	vscode.window.showTextDocument(doc).then((editor) => {
	// 		// editor
	// 	});
	// });

	let fileName = "_mf_query.mfq";
	let filePath = path.join(vscode.workspace.workspaceFolders?.[0].uri.path || "", fileName);
	let fileUri = vscode.Uri.file(filePath);
	let content = "Can you summarize this information as thoroughly as possible?";

	vscode.workspace.fs.writeFile(fileUri, new TextEncoder().encode(content)).then((value) => {
		vscode.window.showTextDocument(fileUri, { preview: false }).then((editor) => {
		});
	});

	vscode.workspace.onDidCloseTextDocument((doc) => {
		if (!doc) return;

		console.log("Closed a doc", doc.uri.path, filePath)

		const isDoc = doc.uri.path == filePath || doc.uri.path == filePath + ".git";  // i'm not sure why it adds the .git thing...
		if (isDoc) {
			console.log("closed THE doc!");
		}
	})	

}


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

			// terminal.sendText("mf query \"" + queryString + "\" " + paths?.join(" ") + " -s");
			const command = "mf q \"" + queryString + "\" " + paths?.join(" ");
			console.log('running command: ' + command);
			terminal.sendText(command);
		});

	});
  }

class MyCompletionItemProvider implements vscode.CompletionItemProvider {
	
	public provideCompletionItems(
		document: vscode.TextDocument,
		position: vscode.Position,
		token: vscode.CancellationToken,
		context: vscode.CompletionContext,
	): vscode.ProviderResult<vscode.CompletionItem[]> {
		const range = document.getWordRangeAtPosition(position);
		const variableName = document.getText(range);
		const files = vscode.workspace.findFiles(`**/${variableName}*/**`);
		return files.then((value) => {
			// add completion items for each file
			const completionItems = value.map(file => {
				const relPath = vscode.workspace.asRelativePath(file.path);
				const completionItem = new vscode.CompletionItem(relPath);
				completionItem.kind = vscode.CompletionItemKind.File;
				return completionItem;
			});
			return completionItems;
		});
	}
}

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	vscode.languages.registerCompletionItemProvider('mfq', new MyCompletionItemProvider(), '@');

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "mindflow" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	// let disposable = vscode.commands.registerCommand('mindflow.query', openQuery);
	let disposable = vscode.commands.registerCommand('mindflow.query', openTextFileQuery);

	context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
export function deactivate() {}
