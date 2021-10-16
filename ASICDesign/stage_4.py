import jinja_helper
import hspice_helper
import waves_helper
import matlab_helper

print("Format stage_4.py")

plot = matlab_helper.PlotCollection()
file_collection = hspice_helper.run("stage_4.sp")
data = waves_helper.convert_hspice_waves(file_collection.dc)

plot.add_pair(data.pick_column("VOLTS"), data.pick_column("5"), "Vin (V)", "Vout (V)", "Vin - Vout Curve")
plot.add_pair(data.pick_column("VOLTS"), data.pick_column("I(vdd"), "Vin (V)", "I VDD (A)", "Vin - Ivdd Curve")

plot.render("stage_4.m", True)
