import jinja_helper
import input_helper
import hspice_helper
import measure_helper
import matlab_helper
import sys

print("Format stage_3.py [nw] [input_count]")

processor = input_helper.HspiceInputIterator({
    "nw": sys.argv[1],
    "input_count": sys.argv[2]
})

percent = []
trise = []
tfall = []
tphl = []
tplh = []

dict_val = tuple(processor.give())[0]
jinja_helper.render("stage_3.tmpl", "stage_3.sp", dict_val)
file_collection = hspice_helper.run("stage_3.sp")
data = measure_helper.get_measure_data(file_collection.measure)

for i in range(dict_val["input_count"]):
    percent.append(i + 1)
    trise.append(data['trise_' + str(i + 1)])
    tfall.append(data['tfall_' + str(i + 1)])
    tphl.append(data['tphl_' + str(i + 1)])
    tplh.append(data['tplh_' + str(i + 1)])

plot = matlab_helper.PlotCollection()
plot.add_pair(percent, trise, "Input Order", "Time (s)", "Trise")
plot.add_pair(percent, tfall, "Input Order", "Time (s)", "Tfall")
plot.add_pair(percent, tphl, "Input Order", "Time (s)", "TPHL")
plot.add_pair(percent, tplh, "Input Order", "Time (s)", "TPLH")
plot.render("stage_3_split.m", True)

plot = matlab_helper.PlotCollection()
plot.add_pair(percent, trise, "Input Order", "Time (s)", "Merged Time Graph")
plot.add_pair(percent, tfall, "Input Order", "Time (s)", "Merged Time Graph")
plot.add_pair(percent, tphl, "Input Order", "Time (s)", "Merged Time Graph")
plot.add_pair(percent, tplh, "Input Order", "Time (s)", "Merged Time Graph")
plot.render("stage_3_merge.m", False)
