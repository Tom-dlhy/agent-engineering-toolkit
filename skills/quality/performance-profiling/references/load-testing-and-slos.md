# k6 load testing — realistic workload and verifiable SLOs

**Read when:** measuring request capacity, error under bursts, latency tails
or implementing performance pass/fail checks.

## Plan before traffic

Establish endpoint/task mix, traffic arrival pattern, input size, tenant
distribution, cache and warmup state, data volume and downstream token/rate
budgets. Test disposable localhost/staging only unless explicit authority
covers a bounded production test.

~~~js
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 3,
  duration: '15s',
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<800'],
    checks: ['rate>0.99'],
  },
};
export default function () {
  const response = http.get('http://127.0.0.1:8000/health');
  check(response, {
    'health returns 200': r => r.status === 200,
  });
}
~~~

Example values are **illustrative**, not recommendations without a business SLO.
k6 checks alone do **not** cause a failed run; a threshold on the checks
metric is included to enforce content/status assertion outcome.
Ensure load-generator CPU isn't bottlenecking before trusting measurements.

## Read results honestly

Track completed successful operations/sec and offered traffic, 429/5xx
rates, p50/p95/p99 latency and queue age. Averages disguise tail.
Rapid failures can artificially reduce mean latency. Compare matched
infrastructure, dataset, version, steady-state window and repetitions.
At high concurrency, monitor DB/HTTP pools, CPU/RSS, event-loop delay
and provider limits; don't assume users → fixed replica threshold.

## CI gate
Use stable microbenchmarks for cheap PR warnings; full load tests are
separate controlled stages. Avoid strict microsecond thresholds on noisy
shared CI runners. Record methodology and confidence rather than
claiming "100k users supported" after a 30-second synthetic run.

Official: https://grafana.com/docs/k6/latest/using-k6/thresholds/ ,
https://grafana.com/docs/k6/latest/using-k6/checks/ ,
https://grafana.com/docs/k6/latest/examples/get-started-with-k6/test-for-performance/ .
