#!/usr/bin/env gnuplot
set title "Temperature"
set xlabel "Datetime"
set ylabel "Celcius"

set terminal png
set output "~/www/monthlyAVG.png"
set datafile separator "|"
set style data lines
set grid
set yrange [0:*]
set autoscale ymin
set xdata time
set timefmt x "%Y-%m-%d %H:%M"
set format x "%m-%d"
plot "< sqlite3 sensors.db \"SELECT date, avg(value) from sensors where date > date('now','-1 months', 'localtime') and name = 'outdoor' group by date;\"" using 1:2 title "outdoor", "< sqlite3 sensors.db \"SELECT date, avg(value) from sensors where date > date('now','-1 months', 'localtime') and name = 'indoor' group by date;\"" using 1:2 title "indoor
