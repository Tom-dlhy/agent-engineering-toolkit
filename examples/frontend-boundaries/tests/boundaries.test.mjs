import test from 'node:test';
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { renderAccount, createBoundaryServer } from '../server.mjs';

const a = {tenant:'A', scopes:new Set(['records:read','records:write'])};
const b = {tenant:'B', scopes:new Set(['records:read'])};

test('server rendering escapes HTML and applies tenant filter', () => {
  const rows=[{id:'a',tenant:'A',label:'<script>bad</script>'},
              {id:'b',tenant:'B',label:'Secret B'}];
  const page=renderAccount(a,rows);
  assert.ok(page.includes('&lt;script&gt;'));
  assert.ok(!page.includes('<script>'));
  assert.ok(!page.includes('Secret B'));
  assert.ok(renderAccount(b,rows).includes('Secret B'));
});

test('same input has deterministic initial HTML', () => {
  const rows=[{id:'a',tenant:'A',label:'Stable'}];
  assert.equal(renderAccount(a,rows),renderAccount(a,rows));
});

test('direct endpoint requires auth, origin, write scope and tenant', async () => {
  const rows=[{id:'a',tenant:'A',label:'A'}, {id:'b',tenant:'B',label:'B'}];
  let actor=null;
  const server=createBoundaryServer(async () => actor, rows,'https://example.test');
  server.listen(0,'127.0.0.1');
  await once(server,'listening');
  const address=server.address();
  if (!address || typeof address === 'string') throw new Error('missing address');
  const base='http://127.0.0.1:'+address.port;
  const update=(id,origin) => fetch(base+'/rpc/update',{
    method:'POST',
    headers:{'content-type':'application/json', ...(origin ? {origin}: {})},
    body:JSON.stringify({id,label:'updated'})
  });
  try {
    assert.equal((await fetch(base+'/account')).status,401);
    actor=a;
    let resp=await fetch(base+'/account');
    assert.equal(resp.status,200);
    assert.equal(resp.headers.get('cache-control'),'private, no-store');
    assert.equal((await update('a',null)).status,403);
    assert.equal((await update('a','https://evil.test')).status,403);
    assert.equal((await update('b','https://example.test')).status,404);
    assert.equal(rows[1].label,'B');
    actor=b;
    assert.equal((await update('b','https://example.test')).status,403);
    actor=a;
    assert.equal((await update('a','https://example.test')).status,200);
    assert.equal(rows[0].label,'updated');
  } finally {
    server.closeAllConnections();
    await new Promise((resolve,reject)=>server.close(e=>e?reject(e):resolve()));
  }
});

test('two SSR users cannot receive each others data', () => {
  const rows=[{id:'a',tenant:'A',label:'Visible to A'},
              {id:'b',tenant:'B',label:'Visible to B'}];
  assert.ok(!renderAccount(a,rows).includes('Visible to B'));
  assert.ok(!renderAccount(b,rows).includes('Visible to A'));
});
