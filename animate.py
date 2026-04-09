import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Plotly Animation Demo", layout="wide")

st.title("4 Plotly Animations in Streamlit")

animation_choice = st.selectbox(
    "Choose an animation",
    [
        "Rotating 3D Helix",
        "Moving Sine Wave",
        "Bouncing Ball",
        "✨ Lissajous Figure",
    ],
)

# --- Shared controls ---
col1, col2 = st.columns(2)

with col1:
    speed = st.slider("Animation Speed (ms per frame)", min_value=20, max_value=200, value=50, step=10)

with col2:
    color_theme = st.selectbox(
        "Color Theme",
        ["Electric Blue", "Neon Green", "Hot Pink", "Solar Orange", "Cyber Purple"],
    )

theme_colors = {
    "Electric Blue":  {"line": "#00cfff", "marker": "#0077ff", "bg": "#050d1a"},
    "Neon Green":     {"line": "#39ff14", "marker": "#00b300", "bg": "#030f03"},
    "Hot Pink":       {"line": "#ff2d78", "marker": "#ff85b3", "bg": "#1a0010"},
    "Solar Orange":   {"line": "#ff8c00", "marker": "#ffcc00", "bg": "#1a0d00"},
    "Cyber Purple":   {"line": "#bf00ff", "marker": "#e580ff", "bg": "#0d001a"},
}

colors = theme_colors[color_theme]
num_frames = 60

dark_layout = dict(
    paper_bgcolor=colors["bg"],
    plot_bgcolor=colors["bg"],
    font=dict(color="#cccccc"),
    margin=dict(l=0, r=0, t=50, b=0),
)

play_pause_buttons = [
    {
        "type": "buttons",
        "buttons": [
            {
                "label": "▶ Play",
                "method": "animate",
                "args": [
                    None,
                    {
                        "frame": {"duration": speed, "redraw": True},
                        "fromcurrent": True,
                    },
                ],
            },
            {
                "label": "⏸ Pause",
                "method": "animate",
                "args": [
                    [None],
                    {
                        "frame": {"duration": 0, "redraw": False},
                        "mode": "immediate",
                    },
                ],
            },
        ],
        "bgcolor": "#222",
        "font": {"color": "#fff"},
    }
]


def rotating_3d_helix():
    t = np.linspace(0, 8 * np.pi, 200)
    x = np.cos(t)
    y = np.sin(t)
    z = np.linspace(-2, 2, 200)

    frames = []
    for i in range(num_frames):
        angle = 2 * np.pi * i / num_frames
        x_rot = x * np.cos(angle) - y * np.sin(angle)
        y_rot = x * np.sin(angle) + y * np.cos(angle)
        frames.append(
            go.Frame(
                data=[go.Scatter3d(x=x_rot, y=y_rot, z=z, mode="lines",
                                   line=dict(color=colors["line"], width=4))],
                name=str(i),
            )
        )

    fig = go.Figure(
        data=[go.Scatter3d(x=x, y=y, z=z, mode="lines",
                           line=dict(color=colors["line"], width=4))],
        frames=frames,
    )
    fig.update_layout(
        title="Rotating 3D Helix",
        scene=dict(
            xaxis=dict(range=[-1.5, 1.5], backgroundcolor=colors["bg"], gridcolor="#222"),
            yaxis=dict(range=[-1.5, 1.5], backgroundcolor=colors["bg"], gridcolor="#222"),
            zaxis=dict(range=[-2.5, 2.5], backgroundcolor=colors["bg"], gridcolor="#222"),
            aspectmode="cube",
        ),
        updatemenus=play_pause_buttons,
        **dark_layout,
    )
    return fig


def moving_sine_wave():
    x = np.linspace(0, 4 * np.pi, 300)

    frames = []
    for i in range(num_frames):
        phase = 2 * np.pi * i / num_frames
        y = np.sin(x + phase)
        frames.append(
            go.Frame(
                data=[go.Scatter(x=x, y=y, mode="lines",
                                 line=dict(color=colors["line"], width=3))],
                name=str(i),
            )
        )

    fig = go.Figure(
        data=[go.Scatter(x=x, y=np.sin(x), mode="lines",
                         line=dict(color=colors["line"], width=3))],
        frames=frames,
    )
    fig.update_layout(
        title="Moving Sine Wave",
        xaxis=dict(range=[0, 4 * np.pi], gridcolor="#222", zerolinecolor="#444"),
        yaxis=dict(range=[-1.5, 1.5], gridcolor="#222", zerolinecolor="#444"),
        updatemenus=play_pause_buttons,
        **dark_layout,
    )
    return fig


def bouncing_ball():
    x_positions = np.linspace(0, 10, num_frames)
    y_positions = np.abs(np.sin(np.linspace(0, 3 * np.pi, num_frames))) * 5

    frames = []
    for i in range(num_frames):
        frames.append(
            go.Frame(
                data=[go.Scatter(
                    x=[x_positions[i]], y=[y_positions[i]],
                    mode="markers",
                    marker=dict(size=24, color=colors["marker"],
                                line=dict(color=colors["line"], width=2)),
                )],
                name=str(i),
            )
        )

    fig = go.Figure(
        data=[go.Scatter(
            x=[x_positions[0]], y=[y_positions[0]],
            mode="markers",
            marker=dict(size=24, color=colors["marker"],
                        line=dict(color=colors["line"], width=2)),
        )],
        frames=frames,
    )
    fig.update_layout(
        title="Bouncing Ball",
        xaxis=dict(range=[0, 10], gridcolor="#222", zerolinecolor="#444"),
        yaxis=dict(range=[0, 6], gridcolor="#222", zerolinecolor="#444"),
        updatemenus=play_pause_buttons,
        **dark_layout,
    )
    return fig


def lissajous_figure():
    """
    Morphs through different Lissajous figures by smoothly varying the
    frequency ratio (a:b) and phase delta over 60 frames.
    """
    t = np.linspace(0, 2 * np.pi, 1000)

    # We'll morph a from 1→3 and delta from 0→2π over the animation
    a_values = np.linspace(1, 3, num_frames)
    delta_values = np.linspace(0, 2 * np.pi, num_frames)

    # Build a color gradient along the curve for a rainbow trail effect
    colorscale = [
        [0.0,  colors["bg"]],
        [0.3,  colors["marker"]],
        [0.7,  colors["line"]],
        [1.0,  "#ffffff"],
    ]

    frames = []
    for i in range(num_frames):
        a = a_values[i]
        b = 2  # keep b fixed at 2 for classic shapes
        delta = delta_values[i]

        x = np.sin(a * t + delta)
        y = np.sin(b * t)

        frames.append(
            go.Frame(
                data=[
                    go.Scatter(
                        x=x, y=y,
                        mode="markers",
                        marker=dict(
                            color=np.linspace(0, 1, len(t)),
                            colorscale=colorscale,
                            size=2,
                        ),
                    )
                ],
                name=str(i),
                layout=go.Layout(
                    title_text=f"Lissajous Figure  |  a={a:.2f} : b={b}  |  δ={np.degrees(delta):.0f}°"
                ),
            )
        )

    x0 = np.sin(a_values[0] * t + delta_values[0])
    y0 = np.sin(2 * t)

    fig = go.Figure(
        data=[
            go.Scatter(
                x=x0, y=y0,
                mode="markers",
                marker=dict(
                    color=np.linspace(0, 1, len(t)),
                    colorscale=colorscale,
                    size=2,
                ),
            )
        ],
        frames=frames,
    )

    fig.update_layout(
        title=f"Lissajous Figure  |  a={a_values[0]:.2f} : b=2  |  δ=0°",
        xaxis=dict(range=[-1.2, 1.2], gridcolor="#1a1a1a", zerolinecolor="#333",
                   scaleanchor="y", scaleratio=1),
        yaxis=dict(range=[-1.2, 1.2], gridcolor="#1a1a1a", zerolinecolor="#333"),
        updatemenus=play_pause_buttons,
        **dark_layout,
    )
    return fig


# --- Render ---
if animation_choice == "Rotating 3D Helix":
    fig = rotating_3d_helix()
elif animation_choice == "Moving Sine Wave":
    fig = moving_sine_wave()
elif animation_choice == "Bouncing Ball":
    fig = bouncing_ball()
else:
    fig = lissajous_figure()

st.plotly_chart(fig, use_container_width=True)

# Info blurb for Lissajous
if animation_choice == "✨ Lissajous Figure":
    st.info(
        "**Lissajous figures** are the curves traced by two perpendicular sinusoidal oscillations. "
        "This animation morphs the frequency ratio **a:b** from 1:2 → 3:2 while sweeping the phase "
        "offset **δ** from 0° → 360°, producing a continuously shifting family of shapes."
    )