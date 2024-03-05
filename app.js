const button = document.getElementById('button')
const filepath = document.getElementById('filepath')
const situation = document.getElementById('situation')
const execute = document.getElementById('execute')

button.addEventListener('click', async () => {
  /**
   * Window オブジェクトに openDialog() メソッドは **もう** 存在していない！
   * text.textContent = await window.openDialog()
   */
  // レンダラープロセスに見えているのは myAPI キーのみで、それ以外のことはわからない
  filepath.textContent = await window.myAPI.openDialog()
  situation.textContent = 'File Selected'
})



execute.addEventListener('click', async () => {
  console.log('[LOG] execute start!')
  const stim = document.getElementById('stim').value
  const frames = document.getElementById('frames').value
  const file = filepath.textContent
  message = await window.myAPI.sendData({'file': file, 'stim': stim, 'frames': frames})
  console.log('[LOG] execute done!')
})

