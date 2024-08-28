import open3d as o3d
import os
import cupy as cp
import numpy as np
from util.point_cloud_util import load_labels, write_labels
from dataset.semantic_dataset import all_file_prefixes
from dataset.semantic_dataset import building_file_prefixes
from tqdm import tqdm

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
        print("No labels -- exception")
        dense_labels = None

    # Print the number of points
    print("Num points:", np.asarray(dense_pcd.points).shape[0])

    # If labels are present, keep all points (including label 0)
    if dense_labels is not None:
        dense_points = np.asarray(dense_pcd.points)
        dense_colors = np.asarray(dense_pcd.colors)

        dense_pcd.points = o3d.utility.Vector3dVector(dense_points)
        dense_pcd.colors = o3d.utility.Vector3dVector(dense_colors)

        print("Num points after including all labels:", np.asarray(dense_pcd.points).shape[0])

    # Downsample points
    min_bound = dense_pcd.get_min_bound() - voxel_size * 0.5
    max_bound = dense_pcd.get_max_bound() + voxel_size * 0.5

    sparse_pcd, cubics_ids = o3d.geometry.voxel_down_sample_and_trace(
        dense_pcd, voxel_size, min_bound, max_bound, False
    )
    print("Num points after down sampling:", np.asarray(sparse_pcd.points).shape[0])

    o3d.io.write_point_cloud(sparse_pcd_path, sparse_pcd)
    print("Point cloud written to:", sparse_pcd_path)

    # Downsample labels using CuPy
    if dense_labels is not None:
        sparse_labels = []
        dense_labels_cp = cp.array(dense_labels)

        # Using tqdm for progress bar
        # for cubic_ids in tqdm(cubics_ids, desc="Downsampling labels"):
        #     cubic_ids = cubic_ids[cubic_ids != -1]
        #     cubic_labels = dense_labels_cp[cubic_ids]
        #     sparse_labels.append(cp.bincount(cubic_labels).argmax())

        # sparse_labels = cp.asnumpy(cp.array(sparse_labels))
        # Using tqdm for progress bar
        for cubic_ids in tqdm(cubics_ids, desc="Downsampling labels"):
            cubic_ids = cubic_ids[cubic_ids != -1]
            if len(cubic_ids) > 0:
                cubic_labels = dense_labels_cp[cubic_ids]
                sparse_labels.append(int(cp.bincount(cubic_labels).argmax()))
            else:
                print("wrong data")
                sparse_labels.append(0)  # Handle empty cubic_ids, defaulting to 0 or another appropriate label
        sparse_labels = cp.asnumpy(sparse_labels)
        write_labels(sparse_label_path, sparse_labels)
        print("Labels written to:", sparse_label_path)


if __name__ == "__main__":
    voxel_size = 0.05

    # By default
    # raw data: "dataset/semantic_raw"
    # downsampled data: "dataset/semantic_downsampled"
    current_dir = os.path.dirname(os.path.realpath(__file__))
    dataset_dir = os.path.join(current_dir, "dataset")
    raw_dir = os.path.join(dataset_dir, "semantic_raw")
    downsampled_dir = os.path.join(dataset_dir, "semantic_downsampled_0.05")

    # Create downsampled_dir
    os.makedirs(downsampled_dir, exist_ok=True)

    # for file_prefix in building_file_prefixes:
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
