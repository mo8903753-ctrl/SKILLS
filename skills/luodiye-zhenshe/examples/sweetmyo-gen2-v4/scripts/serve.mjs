// Tiny static server with HTTP Range support (needed for video scrubbing). Usage: node serve.mjs <root> <port>
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
const root = process.argv[2] || process.cwd();
const port = Number(process.argv[3] || 8796);
const types = { '.html': 'text/html; charset=utf-8', '.js': 'application/javascript; charset=utf-8', '.css': 'text/css', '.mp4': 'video/mp4', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.json': 'application/json' };
http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (p.endsWith('/')) p += 'index.html';
  const file = path.join(root, p);
  if (!file.startsWith(root) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); return res.end('404'); }
  const size = fs.statSync(file).size;
  const type = types[path.extname(file)] || 'application/octet-stream';
  const range = req.headers.range;
  res.setHeader('Cache-Control', 'no-cache');
  if (range) {
    const m = /bytes=(\d*)-(\d*)/.exec(range);
    const start = m[1] ? parseInt(m[1], 10) : 0;
    const end = m[2] ? parseInt(m[2], 10) : size - 1;
    res.writeHead(206, { 'Content-Type': type, 'Content-Range': `bytes ${start}-${end}/${size}`, 'Accept-Ranges': 'bytes', 'Content-Length': end - start + 1 });
    fs.createReadStream(file, { start, end }).pipe(res);
  } else {
    res.writeHead(200, { 'Content-Type': type, 'Content-Length': size, 'Accept-Ranges': 'bytes' });
    fs.createReadStream(file).pipe(res);
  }
}).listen(port, '127.0.0.1', () => console.log('serving', root, 'on', port));
