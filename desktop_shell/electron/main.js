const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const crypto = require("crypto");
const { spawn } = require("child_process");

const API_HOST = process.env.NEXUS_DESKTOP_HOST || "127.0.0.1";
const API_PORT = Number(process.env.NEXUS_DESKTOP_PORT || "8765");
const API_URL = `http://${API_HOST}:${API_PORT}`;
const API_TOKEN = process.env.NEXUS_DESKTOP_API_TOKEN || crypto.randomBytes(24).toString("hex");

let apiProcess = null;

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function waitForApi(maxAttempts = 80) {
  for (let i = 0; i < maxAttempts; i += 1) {
    try {
      const response = await fetch(`${API_URL}/api/health`);
      if (response.ok) {
        return;
      }
    } catch (_) {
      // Continue polling until the Python service is ready.
    }
    await wait(150);
  }
  throw new Error("Nexus desktop API did not start in time");
}

function pythonCommand() {
  if (process.env.NEXUS_PYTHON) {
    return process.env.NEXUS_PYTHON;
  }
  return process.platform === "win32" ? "python" : "python3";
}

function startApi() {
  if (apiProcess) {
    return;
  }

  const repoRoot = path.resolve(__dirname, "..", "..");
  const py = pythonCommand();
  const args = ["-m", "nexus_os.product.api_server", "--host", API_HOST, "--port", String(API_PORT)];
  args.push("--api-token", API_TOKEN);

  apiProcess = spawn(py, args, {
    cwd: repoRoot,
    stdio: ["ignore", "pipe", "pipe"],
    env: {
      ...process.env,
      PYTHONUNBUFFERED: "1",
    },
  });

  apiProcess.stdout.on("data", (chunk) => {
    process.stdout.write(`[nexus-api] ${chunk}`);
  });
  apiProcess.stderr.on("data", (chunk) => {
    process.stderr.write(`[nexus-api] ${chunk}`);
  });
  apiProcess.on("exit", () => {
    apiProcess = null;
  });
}

function stopApi() {
  if (apiProcess) {
    apiProcess.kill();
    apiProcess = null;
  }
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1500,
    height: 980,
    minWidth: 1200,
    minHeight: 760,
    titleBarStyle: "hiddenInset",
    backgroundColor: "#070A14",
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      sandbox: false,
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  win.loadURL(API_URL);
}

ipcMain.handle("app-info", () => ({
  apiUrl: API_URL,
  apiToken: API_TOKEN,
  name: "Nexus Desktop",
}));

ipcMain.handle("open-textual-fallback", () => {
  const repoRoot = path.resolve(__dirname, "..", "..");
  const py = pythonCommand();
  spawn(py, ["-m", "nexus_os.ui", "--developer"], {
    cwd: repoRoot,
    stdio: "inherit",
    detached: true,
  });
  return { ok: true };
});

app.whenReady().then(async () => {
  startApi();
  await waitForApi();
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("before-quit", () => {
  stopApi();
});
