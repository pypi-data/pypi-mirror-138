"""Dash app for using software"""

from distutils.log import debug
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
import base64
import pandas as pd
import io
import zipfile
import mopa.analysis as analysis
import mopa.viz as viz


def create_dashboard():
    """
    Create dash app
    """
    # Initialize app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    # Create app layout
    app.layout = dbc.Container([
        dbc.Row(dbc.Col(html.H1('Multi-Objective Transistor Performance'))),
        dbc.Row(
            dcc.Tabs([  # First Tab
                dcc.Tab(
                    label='Upload AWR Files',
                    children=[
                        dbc.Row(dbc.Col(html.H2('1. Upload Files'))),
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },
                            # Allow multiple files to be uploaded
                            multiple=True
                        ),
                        dbc.Row(dbc.Col(
                            html.Button('Upload', id='upload', n_clicks=0)
                        )),
                        dbc.Row(dbc.Col(html.H2('2. Initial Visualization'))),
                        dbc.Row(html.Div(html.Iframe(
                            id='initial-parallel',
                            style={'width': '100%', 'height': '1080px'}
                        )))
                    ]
                ),
                dcc.Tab(  # Second Tab
                    label='Robustness',
                    children=[
                        dbc.Row(dbc.Col(html.H1('3. Robustness'))),
                        dbc.Row(dbc.Col(
                            html.Button(
                                'Compute Robustness',
                                id='robust',
                                n_clicks=0
                            )
                        )),
                        dbc.Row(html.Div(html.Iframe(
                            id='robust-parallel',
                            style={'width': '100%', 'height': '1080px'}
                        )))
                    ]
                ),
                dcc.Tab(  # Third Tab
                    label='Non-Domination',
                    children=[
                        dbc.Row(dbc.Col(html.H1('4. Non-Domination'))),
                        dbc.Row(dbc.Col(html.Button(
                            'Non-Dominated Sort',
                            id='nondom',
                            n_clicks=0
                        ))),
                        dbc.Row(html.Div(html.Iframe(
                            id='nondom-parallel',
                            style={'width': '100%', 'height': '1080px'}
                        )))
                    ]
                ),
                dcc.Tab(  # Fourth Tab
                    label='Export',
                    children=[
                        dbc.Row(dbc.Col(html.H1('5. Export Plots'))),
                        dbc.Row(dbc.Col(html.Button(
                            'Export',
                            id='export',
                            n_clicks=0
                        ))),
                        dcc.Download(id='download'),
                    ]
                )
            ])
        ),
        dcc.Store(id='initial-store'),
        dcc.Store(id='robust-store'),
        dcc.Store(id='nondom-store')
    ])

    @app.callback(
        Output('initial-store', 'data'),
        Output('initial-parallel', 'srcDoc'),
        Input('upload', 'n_clicks'),
        State('upload-data', 'contents'),
        State('upload-data', 'filename')
    )
    def upload_to_memory(n_clicks, contents, filenames):
        """
        Upload awr files and store in memory. These files get processed along
        the way and visualized

        Parameters
        ----------
        n_clicks : int
            Number of clicks
        contents : list
            List of strings of file contents
        filenames : list
            List of strings of filenames

        Returns
        -------
        data : dict
            Dictionary of data to store in memory
        srcdoc : str
            String of html output
        """
        if n_clicks == 0:
            data = ''
            srcdoc = ''
        else:
            # Parse Files
            df_awr_ls = [
                parse_contents(c, n) for c, n in zip(contents, filenames)
            ]

            # Convert to standard format
            df_ls = [analysis.awr_to_dataframe(df=i) for i in df_awr_ls]

            # Combine into single device DataFrame
            df_device = analysis.combine_output_single_device(df_ls)

            # Extract labels
            obj_labs = df_device.columns[[1, -1]].tolist()
            freq_lab = 'Frequency'
            dec_labs = df_device.columns.difference(obj_labs+[freq_lab])

            # Render Output
            exp = viz.parallel(
                df_device,
                invert_cols=obj_labs
            )
            srcdoc = exp.to_html()

            # Store in memory
            data = {
                'obj_labs': obj_labs,
                'freq_labs': freq_lab,
                'dec_labs': dec_labs,
                'df_device': df_device.to_json(),
                'srcdoc': srcdoc
            }
        return data, srcdoc

    @app.callback(
        Output('robust-store', 'data'),
        Output('robust-parallel', 'srcDoc'),
        Input('robust', 'n_clicks'),
        Input('initial-store', 'data'),
    )
    def compute_robustness(n_clicks, data):
        """
        Compute robustness. Includes adding to memory and visualization

        Parameters
        ----------
        n_clicks : int
            Number of times 'robust' button clicked.
        data : dict
            Data stored in memory from 'upload_to_memory' tab

        Returns
        -------
        robust_data : dict
            Dictionary of data to store in memory
        srcdoc : str
            String of html output
        """
        if n_clicks == 0:
            robust_data = ''
            srcdoc = ''
        else:
            # Local vars
            obj_labs = data['obj_labs']
            robust_types = ['min', 'max', 'mean']
            robust_labs = []
            for robust_type in robust_types:
                for obj in data['obj_labs']:
                    robust_labs.append(robust_type + '_' + obj)

            # Compute robustness metrics
            df_device_robust = analysis.get_native_robust_metrics(
                df=pd.read_json(data['df_device']),
                dec_labs=data['dec_labs'],
                obj_labs=obj_labs,
                robust_types=robust_types
            )

            # Create visualization
            exp = viz.parallel(
                df_device_robust,
                invert_cols=obj_labs + robust_labs
            )
            srcdoc = exp.to_html()

            # Store in memory
            robust_data = {
                'df_device_robust': df_device_robust.to_json(),
                'robust_labs': robust_labs,
                'srcdoc': srcdoc
            }

        return robust_data, srcdoc

    @app.callback(
        Output('nondom-store', 'data'),
        Output('nondom-parallel', 'srcDoc'),
        Input('nondom', 'n_clicks'),
        Input('robust-store', 'data'),
        Input('initial-store', 'data'),
    )
    def nondom(n_clicks, robust_data, initial_data):
        """Get Nond-dominated solutions

        Parameters
        ----------
        n_clicks : int
            Number of clicks of nondom button
        robust_data : dict
            Dictionary of data to store in memory
        initial_data : dict
            Dictionary of data to store in memory

        Returns
        -------
        nondom_data : dict
            Dictionary of data to store in memory
        srcdoc : str
            String of html rendering
        """
        if n_clicks == 0:
            nondom_data = ''
            srcdoc = ''
        else:
            # Local Vars
            robust_labs = robust_data['robust_labs']
            dec_labs = initial_data['dec_labs']
            obj_labs = initial_data['obj_labs']

            # Nondominated sorting
            df_nondom = analysis.get_nondomintated(
                pd.read_json(robust_data['df_device_robust']),
                objs=robust_labs,
                max_objs=robust_labs
            )
            df_nondom = analysis.get_states(
                df_nondom,
                pd.read_json(initial_data['df_device']),
                dec_labs=dec_labs,
            )

            # Create plot for non-dominated solutions
            exp = viz.parallel(
                df_nondom,
                invert_cols=obj_labs + robust_labs
            )
            srcdoc = exp.to_html()

            # Store in memory
            nondom_data = {
                'df_nondom': df_nondom.to_json(),
                'srcdoc': srcdoc
            }

        return nondom_data, srcdoc

    @app.callback(
        Output('download', 'data'),
        Input('export', 'n_clicks'),
        Input('robust-store', 'data'),
        Input('initial-store', 'data'),
        Input('nondom-store', 'data')
    )
    def download(n_clicks, robust_data, initial_data, nondom_data):
        """Download plots

        Parameters
        ----------
        n_clicks : int
            Number of clicks of export button
        robust_data : dict
            Dictionary of data to store in memory
        initial_data : dict
            Dictionary of data to store in memory
        nondom_data : dict
            Dictionary of data to store in memory
        """
        if n_clicks == 0:
            return 0
        else:
            zip_file_name = "plots.zip"
            with zipfile.ZipFile(zip_file_name, mode="w") as zf:
                zf.writestr('Initial.html', initial_data['srcdoc'])
                zf.writestr('Robust.html', robust_data['srcdoc'])
                zf.writestr('Nondom.html', nondom_data['srcdoc'])
            return dcc.send_file(zip_file_name)

    return app


def parse_contents(contents, filename):
    """Parse contents of supplied file

    Parameters
    ----------
    contents : str
        String of file contents
    filename : str
        String of file name

    Returns
    -------
    df : DataFrame
        Parsed dataframe
    """
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        df = pd.read_csv(
            io.StringIO(decoded.decode('utf-8'))
        )
    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        df = pd.read_excel(io.BytesIO(decoded))
    elif 'txt' in filename:
        # Assume that the user uploaded a text file
        df = pd.read_table(io.BytesIO(decoded))
    return df


def main():
    # Create dashboard
    app = create_dashboard()

    # Run dashboard
    app.run_server()


if __name__ == '__main__':
    main()
