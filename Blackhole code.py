# ============================================================
# BLACK HOLE & ACCRETION DISK SIMULATION
# ============================================================
# This simulation visualizes a simplified black hole system.
# Particles orbit the black hole and gradually spiral inward
# due to gravitational attraction, forming an accretion disk.
#
# Scientific principles:
# - Newtonian gravitational motion
# - Orbital dynamics
# - Accretion disk behavior
# - Particle-based simulation
# - 3D visualization

# This is a visual approximation, not a full general-relativistic
# simulation of a real black hole.
# ============================================================

#now for one final
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# ============================================================
# BLACK HOLE SIMULATION
# ============================================================

# -----------------------------
# Simulation settings
# -----------------------------

N = 12000

BLACK_HOLE_RADIUS = 5.2

INNER_DISK = 6.5
OUTER_DISK = 18.0

STAR_COUNT = 500


# ============================================================
# CREATE FIGURE
# ============================================================

fig = plt.figure(
    figsize=(12, 8),
    facecolor="black"
)

ax = fig.add_subplot(
    111,
    projection="3d",
    facecolor="black"
)


# ============================================================
# MAKE 3D SPACE BLACK
# ============================================================

ax.set_facecolor("black")

ax.xaxis.pane.fill = True
ax.yaxis.pane.fill = True
ax.zaxis.pane.fill = True

ax.xaxis.pane.set_facecolor("black")
ax.yaxis.pane.set_facecolor("black")
ax.zaxis.pane.set_facecolor("black")

ax.xaxis.pane.set_edgecolor("black")
ax.yaxis.pane.set_edgecolor("black")
ax.zaxis.pane.set_edgecolor("black")

ax.set_axis_off()


# ============================================================
# BACKGROUND STARS
# ============================================================

star_x = np.random.uniform(-30, 30, STAR_COUNT)
star_y = np.random.uniform(-30, 30, STAR_COUNT)
star_z = np.random.uniform(-30, 30, STAR_COUNT)

star_size = np.random.uniform(
    0.3,
    1.8,
    STAR_COUNT
)

ax.scatter(
    star_x,
    star_y,
    star_z,
    s=star_size,
    c="white",
    alpha=0.75,
    depthshade=False
)


# ============================================================
# ACCRETION DISK PARTICLES
# ============================================================

r = np.random.uniform(
    INNER_DISK,
    OUTER_DISK,
    N
)

# Concentrate particles toward the inner disk

r = INNER_DISK + (
    (r - INNER_DISK) ** 1.15
)


# Initial angular position

theta = np.random.uniform(
    0,
    2 * np.pi,
    N
)


# Thin disk

z = np.random.normal(
    0,
    0.35,
    N
)


# Initial coordinates

x = r * np.cos(theta)
y = r * np.sin(theta)


# ============================================================
# PARTICLE BRIGHTNESS
# ============================================================

brightness = 1 / np.sqrt(r)

brightness = (
    brightness - brightness.min()
)

brightness = (
    brightness / brightness.max()
)


# ============================================================
# DRAW ACCRETION DISK
# ============================================================

disk = ax.scatter(
    x,
    y,
    z,

    s=brightness * 4 + 0.5,

    c=brightness,

    cmap="inferno",

    alpha=0.75,

    depthshade=False
)


# ============================================================
# 3D GOLDEN CENTRAL SPHERE
# ============================================================

u = np.linspace(
    0,
    2 * np.pi,
    160
)

v = np.linspace(
    0,
    np.pi,
    100
)


sphere_x = (
    BLACK_HOLE_RADIUS
    * np.outer(
        np.cos(u),
        np.sin(v)
    )
)

sphere_y = (
    BLACK_HOLE_RADIUS
    * np.outer(
        np.sin(u),
        np.sin(v)
    )
)

sphere_z = (
    BLACK_HOLE_RADIUS
    * np.outer(
        np.ones_like(u),
        np.cos(v)
    )
)


# ============================================================
# GOLDEN 3D LIGHTING
# ============================================================

# Create a light direction
light_direction = np.array(
    [-0.6, -0.4, 0.7]
)

light_direction = (
    light_direction
    / np.linalg.norm(light_direction)
)


# Surface normals of sphere

normal_x = (
    np.outer(
        np.cos(u),
        np.sin(v)
    )
)

normal_y = (
    np.outer(
        np.sin(u),
        np.sin(v)
    )
)

normal_z = (
    np.outer(
        np.ones_like(u),
        np.cos(v)
    )
)


# Calculate lighting

lighting = (
    normal_x * light_direction[0]
    +
    normal_y * light_direction[1]
    +
    normal_z * light_direction[2]
)


lighting = np.clip(
    lighting,
    0,
    1
)


# Add a small amount of ambient light

lighting = (
    0.18
    +
    0.82 * lighting
)


# ============================================================
# GOLD MATERIAL
# ============================================================

gold = np.zeros(
    (
        lighting.shape[0],
        lighting.shape[1],
        4
    )
)


gold[:, :, 0] = (
    1.0 * lighting
)

gold[:, :, 1] = (
    0.55 * lighting
)

gold[:, :, 2] = (
    0.05 * lighting
)

gold[:, :, 3] = 1.0


# ============================================================
# DRAW GOLDEN SPHERE
# ============================================================

ax.plot_surface(
    sphere_x,
    sphere_y,
    sphere_z,

    facecolors=gold,

    linewidth=0,

    antialiased=True,

    shade=False,

    alpha=1.0
)


# ============================================================
# PHOTON RING
# ============================================================

ring_radius = (
    BLACK_HOLE_RADIUS * 1.12
)

ring_theta = np.linspace(
    0,
    2 * np.pi,
    800
)

ring_x = (
    ring_radius
    * np.cos(ring_theta)
)

ring_y = (
    ring_radius
    * np.sin(ring_theta)
)

ring_z = np.zeros_like(
    ring_theta
)


photon_ring = ax.scatter(
    ring_x,
    ring_y,
    ring_z,

    s=3,

    c="gold",

    alpha=0.95,

    depthshade=False
)


# ============================================================
# INNER GLOW RINGS
# ============================================================

for radius, size, alpha in [

    (4.6, 2.5, 0.35),

    (4.9, 1.8, 0.25),

    (5.2, 1.2, 0.18)

]:

    glow_theta = np.linspace(
        0,
        2 * np.pi,
        500
    )

    glow_x = (
        radius
        * np.cos(glow_theta)
    )

    glow_y = (
        radius
        * np.sin(glow_theta)
    )

    glow_z = np.zeros_like(
        glow_theta
    )

    ax.scatter(
        glow_x,
        glow_y,
        glow_z,

        s=size,

        c="orange",

        alpha=alpha,

        depthshade=False
    )


# ============================================================
# CAMERA / SPACE LIMITS
# ============================================================

ax.set_xlim(
    -25,
    25
)

ax.set_ylim(
    -25,
    25
)

ax.set_zlim(
    -15,
    15
)

ax.set_box_aspect(
    (1, 1, 0.65)
)


# ============================================================
# ANIMATION
# ============================================================

def update(frame):

    # --------------------------------------------------------
    # DIFFERENTIAL ROTATION
    # --------------------------------------------------------

    angular_speed = (
        0.035
        / np.sqrt(
            np.maximum(r, 1)
        )
    )

    new_theta = (
        theta
        + frame * angular_speed
    )


    # --------------------------------------------------------
    # SPIRAL INFALL
    # --------------------------------------------------------

    inward = (
        0.00025
        * frame
        / np.maximum(r, 1)
    )

    current_r = (
        r - inward
    )


    # Keep particles outside the inner disk

    current_r = np.maximum(
        current_r,
        INNER_DISK
    )


    # --------------------------------------------------------
    # NEW PARTICLE POSITIONS
    # --------------------------------------------------------

    new_x = (
        current_r
        * np.cos(new_theta)
    )

    new_y = (
        current_r
        * np.sin(new_theta)
    )


    # --------------------------------------------------------
    # VERTICAL MOTION
    # --------------------------------------------------------

    new_z = (
        z
        + 0.05
        * np.sin(
            new_theta * 3
            + frame * 0.02
        )
    )


    # --------------------------------------------------------
    # UPDATE DISK
    # --------------------------------------------------------

    disk._offsets3d = (
        new_x,
        new_y,
        new_z
    )


    # --------------------------------------------------------
    # ROTATE PHOTON RING
    # --------------------------------------------------------

    ring_angle = (
        frame * 0.025
    )

    rotated_x = (
        ring_radius
        * np.cos(
            ring_theta
            + ring_angle
        )
    )

    rotated_y = (
        ring_radius
        * np.sin(
            ring_theta
            + ring_angle
        )
    )


    photon_ring._offsets3d = (
        rotated_x,
        rotated_y,
        ring_z
    )


    # --------------------------------------------------------
    # ROTATING CAMERA
    # --------------------------------------------------------

    azimuth = (
        frame * 0.15
    )

    elevation = (
        22
        + 5
        * np.sin(
            frame * 0.01
        )
    )


    ax.view_init(
        elev=elevation,
        azim=azimuth
    )


    return (
        disk,
        photon_ring
    )


# ============================================================
# START ANIMATION
# ============================================================

animation = FuncAnimation(
    fig,
    update,

    frames=None,

    interval=30,

    blit=False
)


# ============================================================
# DISPLAY
# ============================================================

plt.show()


