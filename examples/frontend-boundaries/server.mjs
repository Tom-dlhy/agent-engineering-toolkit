import { createServer } from 'node:http';

export function escapeHtml(text) {
  return String(text).replaceAll('&', '&amp;').replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#39;');
}

export function renderAccount(actor, rows) {
  if (!actor.scopes.has('records:read')) throw new Error('forbidden');
  const visible = rows.filter(r => r.tenant === actor.tenant);
  const items = visible.map(r => '<li>' + escapeHtml(r.label) + '</li>').join('');
  return '<!doctype html><html><body><h1>Records</h1><ul>' + items + '</ul></body></html>';
}

export function createBoundaryServer(authenticate, rows, trustedOrigin) {
  return createServer(async (req, res) => {
    function send(status, body, contentType = 'application/json') {
      res.writeHead(status, {
        'content-type': contentType,
        'cache-control': 'private, no-store',
        'x-content-type-options': 'nosniff'
      });
      res.end(body);
    }
    try {
      const actor = await authenticate(req);
      if (!actor) return send(401, '{"code":"unauthorized"}');
      if (req.method === 'GET' && req.url === '/account') {
        if (!actor.scopes.has('records:read')) return send(403, '{"code":"forbidden"}');
        return send(200, renderAccount(actor, rows), 'text/html; charset=utf-8');
      }
      if (req.method === 'POST' && req.url === '/rpc/update') {
        // Illustrative Origin guard; real authentication and CSRF policy are outside this fixture.
        if (req.headers.origin !== trustedOrigin) return send(403, '{"code":"cross_origin"}');
        if (!actor.scopes.has('records:write')) return send(403, '{"code":"forbidden"}');
        const chunks = [];
        let bytes = 0;
        for await (const chunk of req) {
          bytes += chunk.length;
          if (bytes > 4096) return send(413, '{"code":"too_large"}');
          chunks.push(chunk);
        }
        let input;
        try { input = JSON.parse(Buffer.concat(chunks).toString('utf8')); }
        catch { return send(400, '{"code":"invalid_json"}'); }
        if (!input || typeof input !== 'object' || Array.isArray(input) ||
            Object.keys(input).some(k => !['id', 'label'].includes(k)) ||
            typeof input.id !== 'string' || typeof input.label !== 'string' ||
            input.label.length > 200) {
          return send(422, '{"code":"invalid_input"}');
        }
        const record = rows.find(r => r.id === input.id && r.tenant === actor.tenant);
        if (!record) return send(404, '{"code":"not_found"}');
        record.label = input.label;
        return send(200, '{"ok":true}');
      }
      return send(404, '{"code":"route_not_found"}');
    } catch {
      return send(500, '{"code":"internal_error"}');
    }
  });
}
