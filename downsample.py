import open3d as o3d
import os
import numpy as np
from util.point_cloud_util import load_labels, write_labels
# from dataset.semantic_dataset import all_file_prefixes
from tqdm import tqdm
import cupy as cp

all_file_prefixes = [
    "bildstein_station1_xyz_intensity_rgb",
    "bildstein_station3_xyz_intensity_rgb",
    "bildstein_station5_xyz_intensity_rgb",
    "domfountain_station1_xyz_intensity_rgb",
    "domfountain_station2_xyz_intensity_rgb",
    "domfountain_station3_xyz_intensity_rgb",
    "neugasse_station1_xyz_intensity_rgb",
    "sg27_station1_intensity_rgb",
    "sg27_station2_intensity_rgb",
    "sg27_station4_intensity_rgb",
    "sg27_station5_intensity_rgb",
    "sg27_station9_intensity_rgb",
    "sg28_station4_intensity_rgb",
    "untermaederbrunnen_station1_xyz_intensity_rgb",
    "untermaederbrunnen_station3_xyz_intensity_rgb",
]

def down_sample(
    dense_pcd_path, dense_label_path, sparse_pcd_path, sparse_label_path, voxel_size
):
    # Skip if done
    if os.path.isfile(sparse_pcd_path) and (
        not os.path.isfile(dense_label_path) or os.path.isfile(sparse_label_path)
    ):
        print("Skipped:", file_prefix)
        return
    else:
        print("Processing:", file_prefix)

    # Inputs
    dense_pcd = o3d.io.read_point_cloud(dense_pcd_path)
    try:
        dense_labels = load_labels(dense_label_path)
    except:
        print("No labels-- exception")
        dense_labels = None

    # Skip label 0, we use explicit frees to reduce memory usage
    print("Num points:", np.asarray(dense_pcd.points).shape[0])
    if dense_labels is not None:
        non_zero_indexes = dense_labels != 0

        dense_points = np.asarray(dense_pcd.points)[non_zero_indexes]
        # dense_pcd.points = o3d.utility.Vector3dVector()
        dense_pcd.points = o3d.utility.Vector3dVector(dense_points)
        del dense_points

        dense_colors = np.asarray(dense_pcd.colors)[non_zero_indexes]
        # dense_pcd.colors = o3d.utility.Vector3dVector()
        dense_pcd.colors = o3d.utility.Vector3dVector(dense_colors)
        del dense_colors

        dense_labels = dense_labels[non_zero_indexes]
        print("Num points after 0-skip:", np.asarray(dense_pcd.points).shape[0])

    with cp.cuda.Device(0):
        # Downsample points
        min_bound = dense_pcd.get_min_bound() - voxel_size * 0.5
        max_bound = dense_pcd.get_max_bound() + voxel_size * 0.5

        sparse_pcd, cubics_ids = o3d.geometry.voxel_down_sample_and_trace(
            dense_pcd, voxel_size, min_bound, max_bound, False
        )
        print("Num points after down sampling:", cp.asarray(sparse_pcd.points).shape[0])

        o3d.io.write_point_cloud(sparse_pcd_path, sparse_pcd)
        print("Point cloud written to:", sparse_pcd_path)

        # Downsample labels
        if dense_labels is not None:
            # sparse_labels = []
            # for cubic_ids in cubics_ids:
            #     cubic_ids = cubic_ids[cubic_ids != -1]
            #     cubic_labels = dense_labels[cubic_ids]
            #     sparse_labels.append(np.bincount(cubic_labels).argmax())
            # sparse_labels = np.array(sparse_labels)


            #Using tqdm for progress bar and cupy instead of numpy
            sparse_labels = []
            dense_labels_cp = cp.array(dense_labels)
            for cubic_ids in tqdm(cubics_ids, desc="Downsampling labels"):
                cubic_ids = cubic_ids[cubic_ids != -1]
                cubic_labels = dense_labels_cp[cubic_ids]
                sparse_labels.append(cp.bincount(cubic_labels).argmax())
            # sparse_labels = cp.array(sparse_labels)
            sparse_labels = cp.asnumpy(sparse_labels)

            write_labels(sparse_label_path, sparse_labels)
            print("Labels written to:", sparse_label_path)


if __name__ == "__main__":
    voxel_size = 0.1

    # By default
    # raw data: "dataset/semantic_raw"
    # downsampled data: "dataset/semantic_downsampled"
    current_dir = os.path.dirname(os.path.realpath(__file__))
    dataset_dir = os.path.join(current_dir, "dataset")
    raw_dir = os.path.join(dataset_dir, "semantic_raw")
    downsampled_dir = os.path.join(dataset_dir, "no_label_0.1")

    # Create downsampled_dir
    os.makedirs(downsampled_dir, exist_ok=True)

    # for file_prefix in all_file_prefixes:
    for file_prefix in all_file_prefixes:
        # Paths
        dense_pcd_path = os.path.join(raw_dir, file_prefix + ".pcd")
        dense_label_path = os.path.join(raw_dir, file_prefix + ".labels")
        sparse_pcd_path = os.path.join(downsampled_dir, file_prefix + ".pcd")
        sparse_label_path = os.path.join(downsampled_dir, file_prefix + ".labels")

        # Put down_sample in a function for garbage collection
        down_sample(
            dense_pcd_path,
            dense_label_path,
            sparse_pcd_path,
            sparse_label_path,
            voxel_size,
        )
