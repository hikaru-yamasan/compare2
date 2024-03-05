const { app, BrowserWindow, ipcMain, dialog } = require('electron')
const path = require('path')

const createWindow = () => {
  const mainWindow = new BrowserWindow({
    width: 600,
    height: 400,
    title: 'Compare',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    },
  })

  // 同時にデベロッパーツールを起動する
  // mainWindow.webContents.openDevTools({ mode: 'detach' })
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
