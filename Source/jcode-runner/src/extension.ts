import * as vscode from "vscode";
import { exec } from "child_process";

let outputChannel: vscode.OutputChannel | undefined;

export function activate(context: vscode.ExtensionContext) {
  outputChannel = vscode.window.createOutputChannel("JCode Output");

  let disposable = vscode.commands.registerCommand(
    "code-runner.run",
    async () => {
      const editor = vscode.window.activeTextEditor;
      if (
        !editor ||
        editor.document.isUntitled ||
        editor.document.uri.scheme !== "file" ||
        !editor.document.fileName.endsWith(".jcode")
      ) {
        vscode.window.showErrorMessage(
          "No active .jcode file - open a jcode (.jcode) file to run"
        );
        return;
      }
      const filePath = editor.document.uri.fsPath;
      const interpreterPath =
        vscode.workspace
          .getConfiguration("jcodeRunner")
          .get<string>("interpreterPath") || "";
      if (!interpreterPath) {
        vscode.window.showErrorMessage(
          "Interpreter path not set. Please configure 'jcodeRunner.interpreterPath' in your settings."
        );
        return;
      }

      outputChannel!.clear();
      outputChannel!.show(true);

      exec(
        `python3 "${interpreterPath}" "${filePath}"`,
        (error, stdout, stderr) => {
          if (error) {
            outputChannel!.appendLine(`Error: ${error.message}`);
          }
          if (stderr) {
            outputChannel!.appendLine(`Stderr: ${stderr}`);
          }
          if (stdout) {
            outputChannel!.appendLine(stdout);
          }
        }
      );
    }
  );
  context.subscriptions.push(disposable);
}

export function deactivate() {
  outputChannel?.dispose();
}
