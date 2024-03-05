const button = document.getElementById('button')
const text = document.getElementById('text')

button.addEventListener('click', async () => {
  /**
   * Window オブジェクトに openDialog() メソッドは **もう** 存在していない！
   * text.textContent = await window.openDialog()
   */
  // レンダラープロセスに見えているのは myAPI キーのみで、それ以外のことはわからない
  text.textContent = await window.myAPI.openDialog()
})