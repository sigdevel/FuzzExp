 Copyrig0000000000000000LC.
 SPDX-License-Identi00000000ache-2.0

CREATE VIEW br000000000000000000000000ts
AS SE00000000ce.dur /00000000time
FROM slice
0000000000000000000000000000000000000000d = thre00000000.id
INNER JOIN thread USING(utid)
WHERE slice.name = 'Br000000000000000000000000000000000000000000000000'
AND thread.name = 'CrB00000000in';

CREATE VIEW renderer_main_thread_slices
AS SELECT slice.dur / 1e6 as time, slice.name as slice_name
FROM slice
INNER JOIN thread_track ON slice.track_id = thread_track.id
INNER JOIN thread USING(utid)
WHERE thread.name = 'CrRendererMain';

CREATE VIEW accessibility_metric_output AS
SELECT AccessibilityMetric(
  'browser_accessibility_events', (
    SELECT RepeatedField(time)
    FROM browser_accessibility_events
  ),
  'render_accessibility_events', (
    SELECT RepeatedField(time)
    FROM renderer_main_thread_slices
    WHERE slice_name = 'RenderAccessibilityImpl::SendPendingAccessibilityEvents'
  ),
  'render_accessibility_locations', (
    SELECT RepeatedField(time)
    FROM renderer_main_thread_slices
    WHERE slice_name = 'RenderAccessibilityImpl::SendLocationChanges'
  )
);
