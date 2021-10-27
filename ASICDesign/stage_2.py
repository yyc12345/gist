import jinja_helper
import input_helper
import hspice_helper
import measure_helper
import matlab_helper
import sys

print("Format stage_2.py [nw]")

processor = input_helper.HspiceInputIterator({
    "nw": sys.argv[1]
})

percent = []
vmin = []
trise = []
tfall = []
tphl = []
tplh = []
for dict_val in processor.give():
    jinja_helper.render("stage_2.tmpl", "stage_2.sp", dict_val)
    file_collection = hspice_helper.run("stage_2.sp")
    data = measure_helper.get_measure_data(file_collection.measure)

    percent.append(dict_val['nw'])
    vmin.append(data['vmin'])
    trise.append(data['trise'])
    tfall.append(data['tfall'])
    tphl.append(data['tphl'])
    tplh.append(data['tplh'])

plot = matlab_helper.PlotCollection()
plot.add_pair(percent, vmin, "Wn / Wp", "Voltage (V)", "Vmin")
plot.add_pair(percent, trise, "Wn / Wp", "Time (s)", "Trise")
plot.add_pair(percent, tfall, "Wn / Wp", "Time (s)", "Tfall")
plot.add_pair(percent, tphl, "Wn / Wp", "Time (s)", "TPHL")
plot.add_pair(percent, tplh, "Wn / Wp", "Time (s)", "TPLH")
plot.render("stage_2_split.m", True)

plot = matlab_helper.PlotCollection()
plot.add_pair(percent, trise, "Wn / Wp", "Time (s)", "Merged Time Graph")
plot.add_pair(percent, tfall, "Wn / Wp", "Time (s)", "Merged Time Graph")
plot.add_pair(percent, tphl, "Wn / Wp", "Time (s)", "Merged Time Graph")
plot.add_pair(percent, tplh, "Wn / Wp", "Time (s)", "Merged Time Graph")
plot.render("stage_2_merge.m", False)