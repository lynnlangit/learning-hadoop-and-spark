SELECT sample_07.description, sample_07.salary
FROM
  sample_07
WHERE
( sample_07.salary > 100000)
ORDER BY sample_07.salary DESC
LIMIT 1000