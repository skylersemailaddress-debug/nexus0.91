const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("nexusDesktop", {
  appInfo: () => ipcRenderer.invoke("app-info"),
  openTextualFallback: () => ipcRenderer.invoke("open-textual-fallback"),
});
