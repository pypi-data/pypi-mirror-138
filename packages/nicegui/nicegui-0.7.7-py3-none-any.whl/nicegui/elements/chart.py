import justpy as jp
from typing import Dict
from .element import Element


class Chart(Element):
    def __init__(self, options: Dict):
        """Chart

        An element to create a chart using `Highcharts <https://www.highcharts.com/>`_.

        :param options: dictionary of highcharts options
        """
        view = jp.HighCharts(classes='m-2 p-2 border', style='width: 600px')
        view.options = self.options = jp.Dict(**options)
        super().__init__(view)
