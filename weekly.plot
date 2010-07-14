#!/usr/bin/env gnuplot
set title "Temperature"
set xlabel "Datetime"
set ylabel "Celcius"

set terminal png
set output "~/www/weekly.png"
set datafile separator "|"
set style data lines
set grid
set yrange [0:*]
set autoscale ymin
set xdata time
set timefmt x "%Y-%m-%d %H:%M"
set format x "%m-%d"
plot "< sqlite3 sensors.db \"SELECT date || ' ' || time, value from sensors where date > date('now','-7 days', 'localtime') and name = 'outdoor';\"" using 1:2 title "outdoor", "< sqlite3 sensors.db \"SELECT date || ' ' || time, value from sensors where date > date('now','-7 days', 'localtime') and name = 'indoor';\"" using 1:2 title "indoor
