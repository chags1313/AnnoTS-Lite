import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from plotly_resampler import FigureResampler, FigureWidgetResampler
import time

st.set_page_config(
    page_title="PHIRE Pipe👩‍🦽",
    page_icon="👩‍🦽",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/hvrlxy/sciJitaiScript',
        'Report a bug': "https://github.com/hvrlxy/sciJitaiScript",
        'About': "# This app makes it possible to compare multiple pariticipant plots at the same time. Ask Cole if you need any help."
    }
)

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def check_autosaved(f):
    try:
        d = pd.read_csv("autosaved_" + f)
        return d
    except:
        return None
# Define function to add rectangle to plot
@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def processing_annotation(start, end, label, color, df, mn, mx):
    # Create figure for plot
    # Create layout for plot
    layout = go.Layout(
        xaxis=dict(title="Timestamps"),
        yaxis=dict(title="Signals"),
        shapes=[]
    )
    fig = FigureWidgetResampler(go.Figure(layout=layout), default_n_shown_samples=st.session_state.n_samples)

    # Add line plot to figure
    fig.add_trace(go.Scatter(x=data.index, y=data["Accelerometer X"], mode="lines", name = "Accx", text = data['Timestamp']))
    # Add line plot to figure
    fig.add_trace(go.Scatter(x=data.index, y=data["Accelerometer Y"], mode="lines", name = "Accy"))
    # Add line plot to figure
    fig.add_trace(go.Scatter(x=data.index, y=data["Accelerometer Z"], mode="lines", name = "Accz"))
    d = pd.DataFrame({'Start': [start], 'End': [end], 'Class': [label], 'Color': [color]})
    df = pd.concat([d, df])
    for i in range(0, len(data), quart):
        fig.add_annotation(text = data['Timestamp'].iloc[i][11:-11], x = i, y = mn, showarrow = False)
    for i in range(len(df)):
        fig.add_shape(
            type="rect",
            x0=df['Start'].iloc[i],
            y0=mn,
            x1=df['End'].iloc[i],
            y1=mx,
            fillcolor=df['Color'].iloc[i],
            line=dict(color="rgba(0, 0, 0, 0.2)", width=0),
            opacity=0.3,
            layer="below"
        )
        fig.add_annotation(x=df['End'].iloc[i], y=mx,
            text=df['Class'].iloc[i],
            showarrow=False,
            yshift=10, textangle=90)
    fig.update_layout(xaxis={"rangeslider":{"visible":True}}, height = 550)
    fig.update_layout(hovermode='x unified', yaxis_range = [mn, mx], showlegend = False)
    fig.update_layout(
        hoverlabel=dict(
            font_size=16,
            font_family="Rockwell"
        )
    )
    return fig, df

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def update_plot(df, data):
    # Create layout for plot
    layout = go.Layout(
        xaxis=dict(title="Timestamps"),
        yaxis=dict(title="Signals"),
        shapes=[]
    )
    # Create figure for plot
    fig = FigureWidgetResampler(go.Figure(layout=layout), default_n_shown_samples=st.session_state.n_samples)

    # Add line plot to figure
    fig.add_trace(go.Scatter(x=data.index, y=data["Accelerometer X"], mode="lines", name = "Accx", text = data['Timestamp']))
    # Add line plot to figure
    fig.add_trace(go.Scatter(x=data.index, y=data["Accelerometer Y"], mode="lines", name = "Accy"))
    # Add line plot to figure
    fig.add_trace(go.Scatter(x=data.index, y=data["Accelerometer Z"], mode="lines", name = "Accz"))
    df = st.session_state.df
    for i in range(0, len(data), quart):
        fig.add_annotation(text = data['Timestamp'].iloc[i][11:-11], x = i, y = mn, showarrow = False)
    for i in range(len(df)):
        fig.add_shape(
            type="rect",
            x0=df['Start'].iloc[i],
            y0=mn,
            x1=df['End'].iloc[i],
            y1=mx,
            fillcolor=df['Color'].iloc[i],
            line=dict(color="rgba(0, 0, 0, 0.2)", width=0),
            opacity=0.3,
            layer="below"
        )
        fig.add_annotation(x=df['End'].iloc[i], y=mx,
            text=df['Class'].iloc[i],
            showarrow=False,
            yshift=10, textangle=90)
    fig.update_layout(xaxis={"rangeslider":{"visible":True}}, height = 550)
    fig.update_layout(hovermode='x unified', yaxis_range = [mn, mx], showlegend = False)
    fig.update_layout(
        hoverlabel=dict(
            font_size=16,
            font_family="Rockwell"
        )
    )
    return fig

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def get_data_download(data, stamps):
    if 'anno_key' not in data:
        data['anno_key'] = 'NAN'
    for i in range(len(stamps)):
        data['anno_key'].iloc[int(stamps['Start'].iloc[i]):int(stamps['End'].iloc[i])] = stamps['Class'].iloc[i]
    return data

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def create_annotation_plot():
    if 'df' in st.session_state:
        # Create figure for plot
        # Create layout for plot
        layout = go.Layout(
            xaxis=dict(title="Timestamps"),
            yaxis=dict(title="Signals"),
            shapes=[]
        )
        fig = FigureWidgetResampler(go.Figure(layout=layout), default_n_shown_samples=st.session_state.n_samples)
        # Add line plot to figure
        fig.add_trace(go.Scatter(x=data.index, y=data["Accelerometer X"], mode="lines", name = "Accx", text = data['Timestamp']))
        # Add line plot to figure
        fig.add_trace(go.Scatter(x=data.index, y=data["Accelerometer Y"], mode="lines", name = "Accy"))
        # Add line plot to figure
        fig.add_trace(go.Scatter(x=data.index, y=data["Accelerometer Z"], mode="lines", name = "Accz"))
        for i in range(0, len(data), quart):
            fig.add_annotation(text =  data['Timestamp'].iloc[i][11:-11], x = i, y = mn, showarrow = False)
        for i in range(len(st.session_state.df)):
            fig.add_shape(
                type="rect",
                x0=st.session_state.df['Start'].iloc[i],
                y0=mn,
                x1=st.session_state.df['End'].iloc[i],
                y1=mx,
                fillcolor="rgba(0, 0, 0, 0.2)",
                line=dict(color="rgba(0, 0, 0, 0.2)", width=0),
                opacity=0.3,
                layer="below"
            )
            fig.add_annotation(x=st.session_state.df['End'].iloc[i], y=mx,
                text=st.session_state.df['Class'].iloc[i],
                showarrow=False,
                yshift=10, textangle=90)
            fig.update_layout(hovermode='x unified', yaxis_range = [mn, mx])
        # Add range slider
        fig.update_layout(xaxis={"rangeslider":{"visible":True}}, height = 550)
        fig.update_layout(hovermode='x unified', yaxis_range = [mn, mx], showlegend = False)
        fig.update_layout(
        hoverlabel=dict(
            font_size=16,
            font_family="Rockwell"
        )
        )
    return fig

def modify_annotations():
    if st.session_state.df['Remove'].any():
        for i in range(len(st.session_state.df)):
            try:
                try:
                    if st.session_state.df['Remove'].iloc[i] == True:
                        st.session_state.df = st.session_state.df.drop([i])
                        fig = update_plot(df = st.session_state.df, data =data)
                        container.plotly_chart(fig, use_container_width=True, config= {'displaylogo': False})
                except:
                    if st.session_state.df['Remove'][i] == True:
                        st.session_state.df = st.session_state.df.drop([i])
                        fig = update_plot(df = st.session_state.df, data =data)
                        container.plotly_chart(fig, use_container_width=True, config= {'displaylogo': False})
            except:
                continue
#################################################
#################################################
#################################################
# UI Starts Here#################################
if 'n_samples' not in st.session_state:
    st.session_state.n_samples = 100000

#Title Format Columns
titleleft, titleright, s, r = st.columns([1,8, 3, 3])

#Header Image
titleleft.image('https://th.bing.com/th/id/OIG.TPqe_ZlXqnmRqYOeK3jr?w=270&h=270&c=6&r=0&o=5&dpr=1.3&pid=ImgGn', width = 100)

#Title
titleright.title("AnnoTS")

#Slogan
st.markdown("AnnoTS Web is designed make the annotation process easy")

#Tabs
settings, annotation, datashow = st.tabs(['Settings', 'Annotation Canvas', 'Data'])

#Classes that are used for annotation
classes = [
    'RchFwd',
    'RchUp',
    'RchDown',
    'LftUp',
    'PshDown',
    'WrstUp',
    'GrspAcqRel',
    'GrspDyn',
    'LtPnch',
    'PshPull',
    'ContainerAcqRel',
    'Container',
    'PnchDie',
    'Pencil',
    'Manipulate',
    'PshIndx',
    'PshThmb']

# SETTINGS TAB
with settings:
    #Upload file
    file = st.file_uploader("Select Data", type = ['.csv'], label_visibility='collapsed')
    #Check if df variable is in session state
    if file is not None:
        if 'df' not in st.session_state:
            #Check if data was previously stored
            d = check_autosaved(f = file.name)
            #If there is data
            if d is not None:
                #Use that data
                st.session_state['df'] = d
            #If there is no data
            else:
                #Create an empty dataframe
                st.session_state['df'] = pd.DataFrame()

#Check if file was uploaded
if file is not None:
    # ANNOTATION TAB
    with annotation:
        form_container = st.empty()
        container = st.empty()
        #Read the csv file
        data = pd.read_csv(file)
        #Get an aribitrary fraction of the data for plotting
        quart = int(len(data) / 15)
        mn, mx = data[["Accelerometer X", "Accelerometer Y", "Accelerometer Z"]].min(axis = 1).min(), data[["Accelerometer X", "Accelerometer Y", "Accelerometer Z"]].max(axis = 1).max()
        # Create annotation figure
        fig = create_annotation_plot()
        # Add plot to app
        container.plotly_chart(fig, use_container_width=True, config= {'displaylogo': False})
        # Add input fields for start and end timestamps, and label
        with st.form("form"):
            left, middle, right, farright = st.columns([4, 4, 4, 1])
            start = left.number_input("Start", step = 1)
            end = middle.number_input("End", step = 1)
            label = right.selectbox("Label", options = classes)
            color = farright.color_picker('Color', '#C8CBC8')
            submit = st.form_submit_button("Add ➕", use_container_width=True)
            # Add button to add rectangle to plot
            if submit:
                fig, st.session_state['df'] = processing_annotation(start, end, label, color, st.session_state['df'], mn = mn, mx = mx)
                container.plotly_chart(fig, use_container_width=True)
                #autosave = st.session_state.df[['Start', 'End', 'Class', 'Color', 'Remove']].to_csv("autosaved_" + file.name, index=False)
        # Add input fields for start and end timestamps, and label
        st.session_state.df['Remove'] = False
        st.session_state.df = st.experimental_data_editor(st.session_state.df.reset_index(drop = True),
                                                            use_container_width = True, on_change = modify_annotations)
        #fig = update_plot(df = st.session_state.df, data =data)
        #container.plotly_chart(fig, use_container_width=True, config= {'displaylogo': False})

        with st.expander("Plot Settings"):
            # Slider for downsampling plot
            st.session_state.n_samples = st.slider("Downsample Plot", 
                                                min_value = 0, 
                                                max_value = len(data), 
                                                value = st.session_state.n_samples, 
                                                help = "This data was downsampled to decrease a buggy experience. You can increase the number of samples to plot by sliding the slider to the right. However, you should note that the performance of the application may decrease.")

        download = s.download_button("💾Save", 
                                     data = get_data_download(data = data, stamps = st.session_state.df).to_csv(index=False).encode('utf-8'), 
                                     file_name = 'ANNOTS.csv',
                                     help = 'Save your file', 
                                     use_container_width=True)
        recover = r.button("📂Recover", use_container_width=True, help = 'Recover from previous checkpoint')
        if recover:
            recovered = pd.read_csv("autosaved_" + file.name)
            st.session_state.df = recovered
            time.sleep(10)
            st.session_state.df = recovered
            fig = create_annotation_plot()
            container.plotly_chart(fig, use_container_width=True, config= {'displaylogo': False})

    with datashow:
        st.dataframe(data.describe(include = 'all'), use_container_width=True)


else:
    with annotation: 
        st.info("Upload Data", icon = '📁')
    with datashow:
        st.info("Upload Data", icon = '📁')

