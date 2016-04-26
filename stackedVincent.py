# -*- coding: utf-8 -*-
"""
Vincent Stacked Area Examples
"""

#Build a Stacked Area Chart from scratch

from vincent import *
import pandas as pd
import pandas.io.data as web
all_data = {}
for ticker in ['AAPL', 'GOOG', 'IBM', 'YHOO', 'MSFT']:
    all_data[ticker] = web.get_data_yahoo(ticker, '1/1/2010', '1/1/2013')
price = pd.DataFrame({tic: data['Adj Close']
                      for tic, data in all_data.items()})

vis = Visualization(width=800, height=500)
vis.padding = {'top': 10, 'left': 50, 'bottom': 50, 'right': 100}


data = Data.from_pandas(price)
vis.data['table'] = data
facets = Transform(type='facet', keys=['data.idx'])
stats = Transform(type='stats', value='data.val')
stat_dat = Data(name='stats', source='table', transform=[facets, stats])
vis.data['stats'] = stat_dat


vis.scales['x'] = Scale(name='x', type='time', range='width',
                        domain=DataRef(data='table', field="data.idx"))
vis.scales['y'] = Scale(name='y', range='height', type='linear', nice=True,
                        domain=DataRef(data='stats', field="sum"))
vis.scales['color'] = Scale(name='color', type='ordinal',
                            domain=DataRef(data='table', field='data.col'),
                            range='category20')
vis.axes.extend([Axis(type='x', scale='x'),
                 Axis(type='y', scale='y')])


facet = Transform(type='facet', keys=['data.col'])
stack = Transform(type='stack', point='data.idx', height='data.val')
transform = MarkRef(data='table',transform=[facet, stack])
enter_props = PropertySet(x=ValueRef(scale='x', field="data.idx"),
                          y=ValueRef(scale='y', field="y"),
                          interpolate=ValueRef(value='monotone'),
                          y2=ValueRef(field='y2', scale='y'),
                          fill=ValueRef(scale='color', field='data.col'))
mark = Mark(type='group', from_=transform,
            marks=[Mark(type='area',
            properties=MarkProperties(enter=enter_props,update=update_props,hover=hover_props))])
vis.marks.append(mark)

vis.axis_titles(x='Date', y='Price')
vis.legend(title='Tech Stocks')
vis.to_json('StackedCHart.json')

#Convenience method

# vis = StackedArea(price)
# vis.axis_titles(x='Date', y='Price')
# vis.legend(title='Tech Stocks')
# vis.colors(brew='Paired')
# vis.to_json('StackedChart.json')
