import numpy as np
import open3d


def _label_to_colors(labels):
    map_label_to_color = {
        0: [255, 255, 255],  # white
        1: [0, 0, 255],  # blue
        2: [128, 0, 0],  # maroon
        3: [255, 0, 255],  # fuchisia
        4: [0, 128, 0],  # green
        5: [255, 0, 0],  # red
        6: [128, 0, 128],  # purple
        7: [0, 0, 128],  # navy
        8: [128, 128, 0],  # olive
    }
    return np.array([map_label_to_color[label] for label in labels]).astype(np.int32)


def _label_to_colors_one_hot(labels):
    map_label_to_color = np.array(
        [
            [255, 255, 255],
            [0, 0, 255],
            [128, 0, 0],
            [255, 0, 255],
            [0, 128, 0],
            [255, 0, 0],
            [128, 0, 128],
            [0, 0, 128],
            [128, 128, 0],
        ]
    )
    num_labels = len(labels)
    labels_one_hot = np.zeros((num_labels, 9))
    labels_one_hot[np.arange(num_labels), labels] = 1
    return np.dot(labels_one_hot, map_label_to_color).astype(np.int32)


def colorize_point_cloud(point_cloud, labels):
    if len(point_cloud.points) != len(labels):
        raise ValueError("len(point_cloud.points) != len(labels)")
    if len(labels) < 1e6:
        print("_label_to_colors_one_hot used")
        colors = _label_to_colors_one_hot(labels)
    else:
        colors = _label_to_colors(labels)
    # np.testing.assert_equal(colors, colors_v2)
    point_cloud.colors = open3d.utility.Vector3dVector()  # Clear it to save memory
    point_cloud.colors = open3d.utility.Vector3dVector(colors)


# def load_labels(label_path):
#     # Assuming each line is a valid int
#     with open(label_path, "r") as f:
#         labels = [int(line) for line in f]
#     return np.array(labels, dtype=np.int32)

def load_labels(labels_file):
    try:
        # Open the file and read the contents
        with open(labels_file, "r") as f:
            # Skip lines that start with 'Labels' or any other header line
            lines = f.readlines()
            labels = []
            for line in lines:
                stripped_line = line.strip()
                if stripped_line and not stripped_line.startswith('Labels'):  # Skip empty lines and headers
                    try:
                        labels.append(int(stripped_line))
                    except ValueError:
                        print(f"Skipping non-integer line: {stripped_line}")

            dense_labels = np.array(labels, dtype=np.int32)
            print(f"dense_labels shape: {dense_labels.shape}")
            return dense_labels
    except Exception as e:
        print(f"Error loading {labels_file}: {e}")
        return np.array([])  # Return an empty array on error


def write_labels(label_path, labels):
    with open(label_path, "w") as f:
        for label in labels:
            f.write("%d\n" % label)
