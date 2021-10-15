import jinja_helper
import input_helper
import hspice_helper
import waves_helper
import matlab_helper
import sys

print("Format stage_1.py [pw]")

processor = input_helper.HspiceInputIterator({
    "pw": sys.argv[1]
})

plot = matlab_helper.PlotCollection()
for dict_val in processor.give():
    jinja_helper.render("stage_1.tmpl", "stage_1.sp", dict_val)
    file_collection = hspice_helper.run("stage_1.sp")
    data = waves_helper.convert_hspice_waves(file_collection.dc)

    plot.add_pair(data.pick_column("VOLTS"), data.pick_column("5"), "Vin (V)", "Vout (V)", "Voltage Transmission Curve")

plot.render("stage_1.m", False)
