import plotly.graph_objects as go
import plotly.express as px

def create_match_gauge(match_percentage):
    try:
        value = float(match_percentage.strip('%'))
    except:
        value = 0
        
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "JD Match", 'font': {'color': 'teal', 'size': 24}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "teal"},
            'bar': {'color': "teal"},
            'steps': [
                {'range': [0, 30], 'color': "#FFE5E5"},
                {'range': [30, 70], 'color': "#E6E6FA"},
                {'range': [70, 100], 'color': "#E6F3EF"}
            ],
            'threshold': {
                'line': {'color': "teal", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=300
    )
    return fig

def create_skills_pie(required_skills, present_skills):
    if not required_skills or not present_skills:
        return None
    
    # Create data for pie chart
    present_count = len([skill for skill in required_skills if skill in present_skills])
    missing_count = len(required_skills) - present_count
    
    labels = ['Present Skills', 'Missing Skills']
    values = [present_count, missing_count]
    colors = ['teal', '#FFE5E5']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.4,
        marker_colors=colors
    )])
    
    fig.update_layout(
        title={
            'text': "Skills Match Analysis",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'color': 'teal', 'size': 20}
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Add percentage annotations
    total = sum(values)
    percentages = [f"{(val/total)*100:.1f}%" for val in values]
    
    annotations = []
    for i, percent in enumerate(percentages):
        annotations.append(dict(
            text=percent,
            x=0.5,
            y=0.5,
            font=dict(size=20, color='white' if i == 0 else 'black'),
            showarrow=False
        ))
    
    fig.update_traces(textposition='inside', textinfo='label+percent')
    return fig

def create_improvement_radar(improvement_areas):
    if not improvement_areas:
        return None
    
    # Create scores for each improvement area
    scores = []
    areas = []
    
    for i, area in enumerate(improvement_areas):
        areas.append(area)
        score = 100 - (i * (100 / (len(improvement_areas) or 1)))
        scores.append(score)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=areas,
        fill='toself',
        name='Priority Areas',
        line_color='#FF4B4B',
        fillcolor='rgba(255, 75, 75, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont={"size": 10},
                showline=True,
                linewidth=1,
                gridcolor='rgba(255, 75, 75, 0.1)'
            ),
            angularaxis=dict(
                tickfont={"size": 10},
                rotation=90,
                direction="clockwise",
                gridcolor='rgba(255, 75, 75, 0.1)'
            )
        ),
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        title={
            'text': "Areas for Improvement",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'color': '#FF4B4B', 'size': 20}
        }
    )
    return fig