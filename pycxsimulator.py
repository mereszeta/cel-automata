from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets


class GUI:

    def __init__(self, parameterSetters=[]):
        self.parameterSetters = parameterSetters

    def start(self, func=[]):
        self.modelInitFunc = func[0]
        self.modelDrawFunc = func[1]
        self.modelStepFunc = func[2]

        def run_step_and_draw():
            self.modelStepFunc()
            self.modelDrawFunc()

        inter = interactive(run_step_and_draw)
        steps_num = widgets.IntSlider(min=1, max=30, step=1, value=1, description="Steps")

        variablesWidgets = []
        variablesText = []
        for variableSetter in self.parameterSetters:
            hWidgets = []
            hWidgets.append(widgets.FloatText(
                value=variableSetter(),
                description=variableSetter.__name__,
                disabled=False
            ))
            variablesText.append(hWidgets[0])
            if variableSetter.__doc__ != None and len(variableSetter.__doc__) > 0:
                hWidgets.append(widgets.Label(value=variableSetter.__doc__.strip()))
            variablesWidgets.append(widgets.HBox(hWidgets))

        def stepf(_):
            for i, variableSetter in enumerate(self.parameterSetters):
                variableSetter(variablesText[i].value)
            for i in range(steps_num.value):
                inter.update()

        def resf(_):
            for i, variableSetter in enumerate(self.parameterSetters):
                variableSetter(variablesText[i].value)
            self.modelInitFunc()
            inter.update()

        run = widgets.Button(description="Run")
        run.on_click(stepf)

        res = widgets.Button(description="Reset")
        res.on_click(resf)
        self.modelInitFunc()

        return widgets.VBox(variablesWidgets + [widgets.HBox([run, steps_num]), res, inter])
