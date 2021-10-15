import jinja_helper
import math

class PlotCollectionPair:
    def __init__(self, x, y, x_label, y_label, title):
        self.x = x
        self.y = y
        self.x_label = x_label
        self.y_label = y_label
        self.title = title

class SubplotCounter:
    def __init__(self, count):
        if count <= 0:
            self.use_subplot = False
            return
        else:
            self.use_subplot = True

        self.cols = int(math.sqrt(count)) + 1
        self.rows = int(count / self.cols)
        if count % self.cols != 0:
            self.rows += 1

class PlotCollection:
    def __init__(self):
        self.pair_collection = []

    def add_pair(self, x, y, x_axis_label, y_axis_label, title):
        self.pair_collection.append(PlotCollectionPair(x, y, x_axis_label, y_axis_label, title))
        print("Adding new curve to plot.")

    def render(self, m_path, subplot):
        if subplot:
            instance_subplot = SubplotCounter(len(self.pair_collection))
        else:
            instance_subplot = SubplotCounter(-1)

        jinja_helper.render("draw_plot.tmpl", m_path, {
            "collection": self.pair_collection,
            "subplot": instance_subplot
        })

        print("Plot file generated successfully")

