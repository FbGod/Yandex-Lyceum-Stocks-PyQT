import os
from datetime import datetime
from datetime import timedelta

import pandas as pd
import pandas_datareader as data_reader
from PyQt5.QtCore import *
from pyecharts import options as opts
from pyecharts.charts import Line

stock_name = ['GOOGL']


class ActionStock:

    def get_stock_data(stocktickers, days):
        start = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        end = (datetime.now()).strftime('%Y-%m-%d')
        stock = []
        for stockticker in stocktickers:
            data = data_reader.DataReader(stockticker, 'yahoo', start, end)
            data['stock_ticker'] = stockticker
            stock.append(data)

        return pd.concat(stock)

    """ Line chart """

    def create_line_chart(self, name):
        stock_name = name
        data = ActionStock.get_stock_data(stock_name, 30)
        stockDate = data.index.tolist()
        open = data['Open'].tolist()
        close = data['Close'].tolist()

        line = (
            Line()
                .add_xaxis(xaxis_data=stockDate)
                .add_yaxis(series_name="Открытие", y_axis=open, symbol="circle", is_symbol_show=True, is_smooth=True,
                           is_selected=True)
                .add_yaxis(series_name="Закрытие", y_axis=close, symbol="circle", is_symbol_show=True, is_smooth=True,
                           is_selected=True)
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title=stock_name[0]))
        )

        html_file = (os.getcwd() + "\\stockchart.html")
        line.render(path=html_file)
        self.view.load(QUrl.fromLocalFile(html_file))

