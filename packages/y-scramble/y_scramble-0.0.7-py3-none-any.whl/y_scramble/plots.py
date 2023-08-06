import plotly.figure_factory as ff

def plot_score_histogram(df):

    colors = ['red', 'blue']
    group_labels = ['base_model', 'randomized']

    fig = ff.create_distplot([df['score'][0:1], df['score'][1::]], 
                            group_labels, bin_size=0.75,
                            curve_type='normal',
                            colors=colors)

    fig.update_layout(title_text='Histogram of scores for scrambled models vs base model')
    fig.show()

    return fig

def plot_zscore_histogram(df):

    colors = ['red', 'blue']
    group_labels = ['base_model', 'randomized']

    fig = ff.create_distplot([df['zscore'][0:1], df['zscore'][1::]], 
                            group_labels, bin_size=0.75,
                            curve_type='normal',
                            colors=colors)

    fig.update_layout(title_text='Histogram of scores for scrambled models vs base model')
    fig.show()

    return fig