# Copyright 2012 Ben Morris; do what you want with it, but how about giving
# me some credit, huh?
from pylab import *
import csv
import scipy.stats as s
import sys
# 1 for absolute numbers, 2 for rates
if len(sys.argv) > 1: PLOT = int(sys.argv[1])
else: PLOT = 1


reader = csv.reader(open('guns.csv'))

reader.next()
xs = []
ys = []
zs = []
countries = {}
for row in reader:
    try:
        (country, code, source, percent_firearm_homicides, num_firearm_homicides, 
         firearm_homicide_rate, firearm_ownership_rank, firearm_ownership_rate, total_firearms) = row
        if PLOT == 1:
            y = float(num_firearm_homicides)
            x = float(total_firearms)
        elif PLOT == 2:
            y = float(firearm_homicide_rate)
            x = float(firearm_ownership_rate)
        z = float(total_firearms) * 100 / float(firearm_ownership_rate)
        if x > 0 and y > 0:
            xs.append(x)
            ys.append(y)
            zs.append(z)
            countries[country] = (x, y)
    except: pass

if PLOT == 1:
    xlabel('firearms owned')
    ylabel('total firearm homicides')
elif PLOT == 2:
    xlabel('firearms owned per 100 people')
    ylabel('firearm homicides per 100,000 people')
xscale('log')
yscale('log')

size = array(zs) ** 0.5 / 50
scatter(xs, ys, s=size)
m, b, r, p, se = s.linregress(log(xs), log(ys))
print m, b, r, p, se
plot(sorted(xs), [e**b * x**m for x in sorted(xs)],
     label='log(y) = %slog(x) + %s\nr^2 = %s\np = %.2g' % (round(m, 2), round(b, 2), round(r**2, 2), p))


for label, country in [
                       ('USA', 'United States'),
                       #('Denmark', 'Denmark'),
                       #('Japan', 'Japan'),
                       #('Canada', 'Canada'),
                       #('France', 'France'),
                       #('Italy', 'Italy'),
                       #('S. Korea', 'Korea, South'),
                       ]:
    try: annotate(label, xy = countries[country])
    except KeyError: pass

legend(loc='lower right')
savefig('figure%s.png' % PLOT)
show()