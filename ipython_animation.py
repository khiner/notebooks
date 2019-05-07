import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import HTML

MILLIS_PER_SECOND = 1_000
DEFAULT_FPS = 24

def create_animation(fig, plt, animate, length_seconds=4, frames_per_second=DEFAULT_FPS, frames=None):
    anim = animation.FuncAnimation(fig, animate, frames=frames if frames else int(length_seconds * frames_per_second), interval=MILLIS_PER_SECOND/frames_per_second)
    video = HTML(anim.to_html5_video())
    plt.close()
    return video
