#!/usr/bin/env gnuplot
set title "Temperature"
set xlabel "Datetime"
set ylabel "Celcius"

set terminal png
set output "~/www/daily.png"
set datafile separator "|"
set style data lines
set grid
set xdata time
set timefmt x "%Y-%m-%d %H:%M"
set format x "%H:%M"
plot "< sqlite3 sensors.db \"SELECT date || ' ' || time, value from sensors where date > datetime('now','-1 days', 'localtime') and name = 'outdoor';\"" using 1:2 title "outdoor", "< sqlite3 sensors.db \"SELECT date || ' ' || time, value from sensors where date > datetime('now','-1 days', 'localtime') and name = 'indoor';\"" using 1:2 title "indoor
