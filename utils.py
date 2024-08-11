import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def read_csv(csv_path):
    np_path_XYs = np.genfromtxt(csv_path, delimiter=',')
    path_XYs = []
    for i in np.unique(np_path_XYs[:, 0]):
        npXYs = np_path_XYs[np_path_XYs[:, 0] == i][:, 1:]
        XYs = []
        for j in np.unique(npXYs[:, 0]):
            XY = npXYs[npXYs[:, 0] == j][:, 1:]
            XYs.append(XY)
        path_XYs.append(XYs)
    return path_XYs

def plot(path_XYs):
    colours = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    for i, XYs in enumerate(path_XYs):
        c = colours[i % len(colours)]
        for XY in XYs:
            ax.plot(XY[:, 0], XY[:, 1], c=c, linewidth=2)
    ax.set_aspect('equal')
    plt.show()

def preprocess(path_XYs):
    processed = []
    for shape in path_XYs:
        processed_shape = []
        for path in shape:
            # Remove duplicate points
            unique_path = np.unique(path, axis=0)
            processed_shape.append(unique_path)
        processed.append(processed_shape)
    return processed

def write_csv(shapes, output_path):
    with open(output_path, 'w') as f:
        for i, shape in enumerate(shapes):
            f.write(f"{i},{shape}\n")




def preprocess(path_XYs):
    processed = []
    for shape in path_XYs:
        processed_shape = []
        for path in shape:
            # Remove duplicate points
            unique_path = np.unique(path, axis=0)

            # Smooth the path using interpolation
            x = unique_path[:, 0]
            y = unique_path[:, 1]
            t = np.linspace(0, 1, len(x))
            f_x = interp1d(t, x, kind='linear')
            f_y = interp1d(t, y, kind='linear')
            t_new = np.linspace(0, 1, 100)
            x_new = f_x(t_new)
            y_new = f_y(t_new)
            smoothed_path = np.column_stack((x_new, y_new))
            processed_shape.append(smoothed_path)
        processed.append(processed_shape)
    return processed



# import numpy as np
# from scipy.interpolate import interp1d

# def read_csv(csv_path):
#     np_path_XYs = np.genfromtxt(csv_path, delimiter=',')
#     path_XYs = []
#     for i in np.unique(np_path_XYs[:, 0]):
#         npXYs = np_path_XYs[np_path_XYs[:, 0] == i][:, 1:]
#         XYs = []
#         for j in np.unique(npXYs[:, 0]):
#             XY = npXYs[npXYs[:, 0] == j][:, 1:]
#             XYs.append(XY)
#         path_XYs.append(XYs)
#     return path_XYs

# def preprocess(path_XYs):
#     processed = []
#     for shape in path_XYs:
#         processed_shape = []
#         for path in shape:
#             # Remove duplicate points
#             unique_path = np.unique(path, axis=0)

#             # Smooth the path using interpolation
#             x = unique_path[:, 0]
#             y = unique_path[:, 1]
#             t = np.linspace(0, 1, len(x))
#             f_x = interp1d(t, x, kind='linear')
#             f_y = interp1d(t, y, kind='linear')
#             t_new = np.linspace(0, 1, 100)
#             x_new = f_x(t_new)
#             y_new = f_y(t_new)
#             smoothed_path = np.column_stack((x_new, y_new))
#             processed_shape.append(smoothed_path)
#         processed.append(processed_shape)
#     return processed

# def write_csv(path_XYs, output_path):
#     with open(output_path, 'w') as f:
#         for shape in path_XYs:
#             for path in shape:
#                 for x, y in path:
#                     f.write(f"{x:.2E} {y:.2E}\n")