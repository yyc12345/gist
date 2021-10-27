import jinja_helper
import hspice_helper
import waves_helper
import matlab_helper

print("Format stage_4.py")

plot = matlab_helper.PlotCollection()
file_collection = hspice_helper.run("stage_4.sp")
data = waves_helper.convert_hspice_waves(file_collection.dc)

voltage = data.pick_column("5")
current = data.pick_column("I(vdd")
power = [abs(a * 5) for a in current]

plot.add_pair(data.pick_column("VOLTS"), voltage, "Vin (V)", "Vout (V)", "Vin - Vout Curve")
plot.add_pair(data.pick_column("VOLTS"), current, "Vin (V)", "I VDD (A)", "Vin - Ivdd Curve")
plot.add_pair(data.pick_column("VOLTS"), power, "Vin (V)", "Power (W)", "Vin - Power Curve")

plot.render("stage_4.m", True)
