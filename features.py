import numpy as np
from scipy.spatial import ConvexHull

def count_corners(shape):
    corners = 0
    for path in shape:
        for i in range(len(path)):
            prev = path[i-1]
            curr = path[i]
            next = path[(i+1) % len(path)]
            v1 = prev - curr
            v2 = next - curr
            angle = np.arctan2(np.cross(v1, v2), np.dot(v1, v2))
            if abs(angle) < np.pi/4:  # 45 degree threshold
                corners += 1
    return corners

def aspect_ratio(shape):
    all_points = np.concatenate(shape)
    x_min, y_min = np.min(all_points, axis=0)
    x_max, y_max = np.max(all_points, axis=0)
    return (x_max - x_min) / (y_max - y_min)

def convexity(shape):
    all_points = np.concatenate(shape)
    hull = ConvexHull(all_points)
    return hull.area / hull.volume

def circularity(shape):
    all_points = np.concatenate(shape)
    perimeter = np.sum([np.sum(np.sqrt(np.sum(np.diff(path, axis=0)**2, axis=1))) for path in shape])
    area = ConvexHull(all_points).area
    return 4 * np.pi * area / (perimeter ** 2)

def extract_features(shape):
    return {
        'corners': count_corners(shape),
        'aspect_ratio': aspect_ratio(shape),
        'convexity': convexity(shape),
        'circularity': circularity(shape)
    }

def detect_shape(features):
    if features['circularity'] > 0.85:
        return 'circle'
    elif features['corners'] == 4 and 0.8 < features['aspect_ratio'] < 1.2:
        return 'square'
    elif features['corners'] == 4:
        return 'rectangle'
    elif features['corners'] == 3:
        return 'triangle'
    else:
        return 'unknown'