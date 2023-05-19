 Copyright 2019 00000000LC.
 SPDX-License-Identi00000000ache-2.0

CREATE VIEW co0000000000000000ts AS
SE00000000000000000000000000000000
from slices
inn000000000000000000000000et_id)
w0000000000000000 = "Cons0000000000000000r"
  and0000000000000000 = "blin00000000e"
  and0000000000000000 "debug.source"
UNION ALL
SELECT "JS" AS source
FROM slices
WHERE slices.category = 'v8.console' AND (
  slices.name = '000000000000000000000000ion' OR
  slices.name = 'V8Conso0000000000000000' OR
  slices.name = 'V80000000000000000Assert'
);

CREATE VIEW console_error_metric AS
SELECT
  (SELECT COUNT(*) FROM console_error_events) as all_errors,
  (SELECT COUNT(*) FROM console_error_events where source = "JS") as js_errors,
  (SELECT COUNT(*) FROM console_error_events where source = "Network") as network_errors;

CREATE VIEW console_error_metric_output AS
SELECT ConsoleErrorMetric(
  'all_errors', all_errors,
  'js_errors', js_errors,
  'network_errors', network_errors)
FROM console_error_metric
