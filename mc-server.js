const http = require('http');
const fs = require('fs');
const path = require('path');
const net = require('net');

const PORT = 8899;
const DATA_PATH = path.join(__dirname, 'mc-backup.json');
const ACTIVITY_PATH = path.join(__dirname, 'mc-activity.log');

function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', c => (data += c));
    req.on('end', () => resolve(data));
    req.on('error', reject);
  });
}

function send(res, status, payload, contentType = 'application/json') {
  res.writeHead(status, {
    'Content-Type': contentType,
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  });
  res.end(typeof payload === 'string' ? payload : JSON.stringify(payload));
}

function loadData() {
  try {
    if (!fs.existsSync(DATA_PATH)) return {};
    return JSON.parse(fs.readFileSync(DATA_PATH, 'utf8'));
  } catch {
    return {};
  }
}

function saveData(obj) {
  fs.writeFileSync(DATA_PATH, JSON.stringify(obj, null, 2));
}

async function getDubaiWeather() {
  try {
    const r = await fetch('https://wttr.in/Dubai?format=j1');
    const j = await r.json();
    const cur = j.current_condition?.[0] || {};
    return {
      temp: Number(cur.temp_C || 0),
      condition: cur.weatherDesc?.[0]?.value || 'Unknown',
      city: 'Dubai',
    };
  } catch {
    return { temp: '--', condition: 'Unavailable', city: 'Dubai' };
  }
}

function tcpProbe(host, port, timeoutMs = 1200) {
  return new Promise(resolve => {
    const socket = new net.Socket();
    let done = false;

    const finish = ok => {
      if (done) return;
      done = true;
      socket.destroy();
      resolve(ok);
    };

    socket.setTimeout(timeoutMs);
    socket.once('connect', () => finish(true));
    socket.once('timeout', () => finish(false));
    socket.once('error', () => finish(false));
    socket.connect(port, host);
  });
}

async function getBotHealth() {
  const [h1Up, etchUp] = await Promise.all([
    tcpProbe('127.0.0.1', 18789),
    tcpProbe('127.0.0.1', 47033),
  ]);

  return {
    checkedAt: Date.now(),
    bots: {
      malawany: {
        status: 'unknown',
        detail: 'Laptop-local bot; not directly probeable from this VPS',
      },
      h1: {
        status: h1Up ? 'online' : 'offline',
        detail: h1Up ? 'Gateway port 18789 reachable' : 'Gateway port 18789 unreachable',
      },
      etchclaw: {
        status: etchUp ? 'online' : 'offline',
        detail: etchUp ? 'Container port 47033 reachable' : 'Container port 47033 unreachable',
      },
    },
  };
}

const server = http.createServer(async (req, res) => {
  if (req.method === 'OPTIONS') return send(res, 204, '');

  const url = new URL(req.url, `http://${req.headers.host}`);

  if (url.pathname === '/mc/data' && req.method === 'GET') {
    return send(res, 200, loadData());
  }

  if (url.pathname === '/mc/data' && req.method === 'POST') {
    try {
      const body = await readBody(req);
      const data = body ? JSON.parse(body) : {};
      saveData(data);
      return send(res, 200, { ok: true, savedAt: Date.now() });
    } catch {
      return send(res, 400, { ok: false, error: 'Invalid JSON' });
    }
  }

  if (url.pathname === '/mc/activity' && req.method === 'POST') {
    try {
      const body = await readBody(req);
      const data = body ? JSON.parse(body) : {};
      const line = `${new Date().toISOString()} | ${data.description || 'activity'}\n`;
      fs.appendFileSync(ACTIVITY_PATH, line);
      return send(res, 200, { ok: true });
    } catch {
      return send(res, 400, { ok: false, error: 'Invalid JSON' });
    }
  }

  if (url.pathname === '/mc/weather' && req.method === 'GET') {
    const weather = await getDubaiWeather();
    return send(res, 200, weather);
  }

  if (url.pathname === '/mc/bots' && req.method === 'GET') {
    const health = await getBotHealth();
    return send(res, 200, health);
  }

  return send(res, 404, { ok: false, error: 'Not found' });
});

server.listen(PORT, () => {
  console.log(`Mission Control backup server running on http://localhost:${PORT}`);
});