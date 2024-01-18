from plotly.subplots import make_subplots

import plotly.express as px
import plotly.graph_objects as go

def show_comparison_graph(graph_title, lhs, rhs=None, x_range=None):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    _add_data_to_fig(fig, lhs, False)
    if rhs is not None:
        _add_data_to_fig(fig, rhs, True)

    fig.update_layout(title_text=graph_title)
    if x_range is not None:
        fig.update_xaxes(range=x_range)
    fig.show()

def _add_data_to_fig(fig, obj, secondary_y):
    obj_title = obj['description']
    if 'range' in obj:
        fig.update_yaxes(title_text=obj_title, secondary_y=secondary_y, range=obj['range'])
    else:
        fig.update_yaxes(title_text=obj_title, secondary_y=secondary_y)
    for entry in obj['data']:
        t = entry.get('type', 'trace')
        assert t in {'trace', 'bar'}

        n = entry['name']
        xs = entry['x']
        ys = entry['y']

        if t == 'trace':
            m = entry.get('mode', 'lines')
            assert m in {'lines', 'lines+markers', 'markers'}
            fig.add_trace(go.Scatter(x=xs, y=ys, mode=m, name=n), secondary_y=secondary_y)
        elif t == 'bar':
            fig.add_bar(x=xs, y=ys, name=n, secondary_y=secondary_y)

if __name__ == '__main__':
    # Sanity check
    import numpy as np

    x = np.linspace(0, 10, 100)
    f_x = np.sin(x)
    g_x = x + np.cos(x)

    show_comparison_graph('A graph of sin(x) vs x+cos(x)',
                          {
                            'description': 'Left hand side data',
                            'data': [{'name': 'sin(x)', 'x': x, 'y': f_x}]
                          },
                          {
                            'description': 'Right hand side data',
                            'data': [{'name': 'x+cos(x)', 'x': x, 'y': g_x}]
                          })

    show_comparison_graph('A graph of sin(x) alone',
                          {
                            'description': 'Left hand side data',
                            'data': [{'name': 'sin(x)', 'x': x, 'y': f_x}]
                          })

    show_comparison_graph('A graph of sin(x) and x+cos(x) on the same side',
                          {
                            'description': 'Left hand side data',
                            'data': [{'name': 'sin(x)', 'x': x, 'y': f_x},
                                     {'name': 'x+cos(x)', 'x': x, 'y': g_x}]
                          },
                          rhs=None,
                          x_range=[6, 9])

    show_comparison_graph('A graph of (trace+bar) sin(x) vs x+cos(x)',
                          {
                            'description': 'Left hand side data',
                            'data': [{'name': 'trace sin(x)', 'x': x, 'y': f_x},
                                     {'name': 'bar sin(x)', 'x': x, 'y': f_x, 'type': 'bar'}]
                          },
                          {
                            'description': 'Right hand side data',
                            'data': [{'name': 'x+cos(x)', 'x': x, 'y': g_x}]
                          })
    print('Done')
