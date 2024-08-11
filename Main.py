import numpy as np
import matplotlib.pyplot as plt
from utils import read_csv, plot, preprocess, write_csv
from features import extract_features, detect_shape

###  .\env\Scripts\activate
### python shape_detector.py

def main():
    input_path = 'examples/frag2_sol.csv'
    output_path = 'outputsss/test2.csv'


    # input_path = 'outputsss/test2.csv'
    # output_path = 'outputsss/test2zzzz.csv'


    # Read and plot input data
    path_XYs = read_csv(input_path)
    plot(path_XYs)

    # Preprocess data
    preprocessed_data = preprocess(path_XYs)

    # Extract features and detect shapes
    features = [extract_features(shape) for shape in preprocessed_data]
    detected_shapes = [detect_shape(f) for f in features]

    # Write results
    

    write_csv(detected_shapes, output_path)
    
    # path_XYz = read_csv(output_path)
    # plot(path_XYz)

    print("Shape detection completed. Results written to", output_path)

if __name__ == "__main__":
    main()




# from utils import read_csv, preprocess, write_csv

# def main():
#     input_path = 'examples/frag2.csv'
#     output_path = 'examples/test24.csv'

#     path_XYs = read_csv(input_path)
#     smoothed_path_XYs = preprocess(path_XYs)
#     write_csv(smoothed_path_XYs, output_path)

#     print("Smoothing completed. Results written to", output_path)

# if __name__ == "__main__":
#     main()