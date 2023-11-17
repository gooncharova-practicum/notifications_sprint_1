NOTIFICATIONS_LATEST = """
SELECT
  n.id,
  n.is_instant,
  n.schedule_at,
  t.layot,
  m.subject,
  m.body,
  array_length(users_ids, 1) as users_count
FROM
  notify.notifications n
JOIN notify.templates t ON n.template_id = t.id
JOIN notify.messages m ON n.message_id = m.id
WHERE GREATEST(n.created_at, n.modified_at) > %s
OFFSET %s;
"""

USERS_DETAILED = """
SELECT
  u.id,
  u.username,
  u.email,
  ui.first_name,
  ui.last_name,
  ui.timezone
FROM
  notify.users u
  JOIN notify.users_info ui ON ui.user_id = u.id
WHERE
  u.id = ANY(
    select
      unnest(users_ids)
    from
      notify.notifications
    where
      id = %s
  )
GROUP BY
  u.id,
  ui.id
OFFSET %s
"""
