from datetime import timedelta

import pandas as pd
from bokeh.plotting import figure, Figure


def get_candlestick_plot(
    df: pd.DataFrame,
    window_seconds: int    
) -> Figure:
    """Generates a candlestick plot using the provided data in `df_` and the
    Bokeh library

    Args:
        df_ (pd.DataFrame): columns
            - upper_band
            - lower_band
            - open
            - high
            - low
            - close

    Returns:
        figure.Figure: Bokeh figure with candlestick and Bollinger bands
    """
    
    df["date"] = pd.to_datetime(df["time"], unit="s")

    inc = df.close > df.open
    dec = df.open > df.close
    w = 1000 * window_seconds / 2 # band width in ms

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    x_max = df['date'].max() + timedelta(minutes=2)
    x_min = df['date'].max() - timedelta(minutes=4)
    p = figure(x_axis_type="datetime", tools=TOOLS, width=1000,
               title = "ETH/USD", x_range=(x_min, x_max))
    p.grid.grid_line_alpha=0.3

    p.segment(df.date, df.high, df.date, df.low, color="black")
    p.vbar(df.date[inc], w, df.open[inc], df.close[inc], fill_color="#70bd40", line_color="black")
    p.vbar(df.date[dec], w, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")

    return p