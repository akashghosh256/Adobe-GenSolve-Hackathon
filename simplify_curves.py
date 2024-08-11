# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.linear_model import LinearRegression
# from sklearn.preprocessing import PolynomialFeatures

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

# def fit_line(X, y):
#     model = LinearRegression()
#     model.fit(X, y)
#     return model.coef_[0], model.intercept_

# def fit_polynomial(X, y, degree):
#     poly = PolynomialFeatures(degree=degree)
#     X_poly = poly.fit_transform(X)
#     model = LinearRegression()
#     model.fit(X_poly, y)
#     return model.coef_, model.intercept_

# def process_shape(XYs):
#     new_XYs = []
#     for path in XYs:
#         X = path[:, 0]
#         y = path[:, 1]
#         if len(X) <= 2:
#             new_XYs.append(path)
#             continue
        
#         # Fit a line to the path
#         a, b = fit_line(X[:, np.newaxis], y)
#         new_X = np.linspace(min(X), max(X), 100)
#         new_y = a * new_X + b
#         new_path = np.column_stack((new_X, new_y))
#         new_XYs.append(new_path)
#     return new_XYs

# def write_csv(paths_XYs, output_path):
#     with open(output_path, 'w') as f:
#         for i, XYs in enumerate(paths_XYs):
#             for j, XY in enumerate(XYs):
#                 for x, y in XY:
#                     f.write(f"{i},{j},{x},{y}\n")

# # Example usage
# input_path = 'examples/frag2.csv'
# output_path = 'outputsss/test2.csv'

# path_XYs = read_csv(input_path)
# new_path_XYs = [process_shape(XYs) for XYs in path_XYs]
# write_csv(new_path_XYs, output_path)















# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.linear_model import LinearRegression
# from sklearn.preprocessing import PolynomialFeatures

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

# def fit_polynomial(X, y, degree):
#     poly = PolynomialFeatures(degree=degree)
#     X_poly = poly.fit_transform(X)
#     model = LinearRegression()
#     model.fit(X_poly, y)
#     return model, poly

# def process_shape(XYs, degree=3):
#     new_XYs = []
#     for path in XYs:
#         X = path[:, 0]
#         y = path[:, 1]
#         if len(X) <= 2:
#             new_XYs.append(path)
#             continue
        
#         # Fit a polynomial to the path
#         model, poly = fit_polynomial(X[:, np.newaxis], y, degree)
#         new_X = np.linspace(min(X), max(X), len(X))  # Keep the number of points the same
#         new_y = model.predict(poly.transform(new_X[:, np.newaxis]))
#         new_path = np.column_stack((new_X, new_y))
#         new_XYs.append(new_path)
#     return new_XYs

# def write_csv(paths_XYs, output_path):
#     with open(output_path, 'w') as f:
#         for i, XYs in enumerate(paths_XYs):
#             for j, XY in enumerate(XYs):
#                 for x, y in XY:
#                     f.write(f"{i},{j},{x},{y}\n")

# # Example usage
# input_path = 'examples/frag1.csv'
# output_path = 'outputsss/test2.csv'

# path_XYs = read_csv(input_path)
# new_path_XYs = [process_shape(XYs) for XYs in path_XYs]
# write_csv(new_path_XYs, output_path)





import numpy as np
import matplotlib.pyplot as plt
import cv2

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

def fit_and_correct_shapes(XYs):
    new_XYs = []
    for path in XYs:
        if len(path) < 5:  # Skip paths with fewer than 5 points
            new_XYs.append(path)
            continue

        path = np.array(path, dtype=np.float32)
        contours = path.reshape(-1, 1, 2)

        if len(contours) >= 5:  # Fit ellipse if possible
            ellipse = cv2.fitEllipse(contours)
            new_path = cv2.ellipse2Poly((int(ellipse[0][0]), int(ellipse[0][1])),
                                        (int(ellipse[1][0] // 2), int(ellipse[1][1] // 2)),
                                        int(ellipse[2]), 0, 360, 5)
        else:
            new_path = contours[:, 0, :]  # Retain the original path if insufficient points
        
        new_XYs.append(new_path)
    return new_XYs

def write_csv(paths_XYs, output_path):
    with open(output_path, 'w') as f:
        for i, XYs in enumerate(paths_XYs):
            for j, XY in enumerate(XYs):
                for x, y in XY:
                    f.write(f"{i},{j},{x},{y}\n")

def plot(paths_XYs):
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    for i, XYs in enumerate(paths_XYs):
        c = colors[i % len(colors)]
        for XY in XYs:
            if len(XY) > 0:
                ax.plot(XY[:, 0], XY[:, 1], c=c, linewidth=2)
    ax.set_aspect('equal')
    plt.show()

# Example usage
input_path = 'examples/frag0.csv'
output_path = 'outputsss/test2.csv'

path_XYs = read_csv(input_path)
new_path_XYs = [fit_and_correct_shapes(XYs) for XYs in path_XYs]
write_csv(new_path_XYs, output_path)
plot(new_path_XYs)
