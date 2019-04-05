# gtfs-route-lengths
Calculates lengths of routes from GTFS source, prints sorted longest to shortest.

## Instructions
Run from CLI and specify directory of extracted, plain-text GTFS data (or run in same directory as data). Requires shapes.txt, routes.txt, and trips.txt to be present.

## Dependencies
GeoPY: `pip install geopy` or download here https://geopy.readthedocs.io/en/stable

## Known issue
When a used value is located at the end of a line in a file, the newline character is included, which results in the script failing. Temp workaround is to open the affected files in a table editor (e.g. Microsoft Excel) and move the column away from the end.

Used values from `routes.txt`:
`route_id`
`route_short_name`

Used values from `trips.txt`:
`route_id`
`shape_id`

Used values from `shapes.txt`:
`shape_id`
`shape_pt_lat`
`shape_pt_lon`
