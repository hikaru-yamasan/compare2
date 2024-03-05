const { app, BrowserWindow, ipcMain, dialog } = require('electron')
const path = require('path')

// ここで pythonshell library を呼び出す
const { PythonShell } = require('python-shell')

const createWindow = () => {
  const mainWindow = new BrowserWindow({
    width: 900,
    height: 4600,
    title: 'Compare',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    },
  })

  // 同時にデベロッパーツールを起動する
  mainWindow.webContents.openDevTools({ mode: 'detach' })
  
  mainWindow.loadFile('index.html') // index.html を読み込ませている -> Chromium が対応



  ipcMain.handle('open-dialog', async (_e, _arg) => {
    return dialog
      .showOpenDialog(mainWindow, {
        properties: ['openFile'],
      })
      .then((result) => {
        if (result.canceled) return ''

        return result.filePaths[0]
      })
      .catch((err) => console.error(err))
  })

  

}

// app はアプリ全体のライフサイクルを制御するモジュール
app.once('ready', () => {
  createWindow()
})

// すべてのウィンドウが閉じられたというイベントに対応してアプリ自身を終了させる
app.once('window-all-closed', () => app.quit())

ipcMain.handle('analyze', async (event, data) => {
  console.log('[LOG] handler analyze called')
  console.log('[LOG] data: ', data)
  var options = [
    data['file'],
    data['stim'],
    data['frames'],
  ]
  console.log('[LOG] pyshell called')
  var pyshell = new PythonShell('analyze.py')
  pyshell.send(data['file'])
  pyshell.send(data['stim'])
  pyshell.send(data['frames'])
  pyshell.on('message', function (data) {
    console.log('[LOG] ', data)
  })
})