import os
import numpy as np
import open3d as o3d
from tqdm import tqdm
import time

# Folder paths
input_folder = "dataset/semantic_raw"
output_folder = "dataset/semantic_raw_label_removed"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# File prefixes
train_file_prefixes = [

    "bildstein_station1_xyz_intensity_rgb",
    "bildstein_station3_xyz_intensity_rgb",
    "bildstein_station5_xyz_intensity_rgb",
    "sg27_station4_intensity_rgb",
    "domfountain_station1_xyz_intensity_rgb",
    "domfountain_station2_xyz_intensity_rgb",
    "domfountain_station3_xyz_intensity_rgb",
    "neugasse_station1_xyz_intensity_rgb",
    "sg27_station1_intensity_rgb",
    "sg27_station2_intensity_rgb",
    "sg27_station5_intensity_rgb",
    "sg27_station9_intensity_rgb",
    "sg28_station4_intensity_rgb",
    "untermaederbrunnen_station1_xyz_intensity_rgb",
    "untermaederbrunnen_station3_xyz_intensity_rgb",
]
# Outer progress bar for the total number of files
with tqdm(total=len(train_file_prefixes), desc="Processing files", unit="file") as pbar:
    for prefix in train_file_prefixes:
        # Output file paths
        output_pcd_file_path = os.path.join(output_folder, prefix + ".pcd")
        output_label_file_path = os.path.join(output_folder, prefix + ".labels")
        
        # Check if the output files already exist
        if os.path.exists(output_pcd_file_path) and os.path.exists(output_label_file_path):
            tqdm.write(f"Skipping {prefix}: filtered files already exist.")
            pbar.update(1)
            continue
        
        start_time = time.time()
        
        # File paths
        pcd_file_path = os.path.join(input_folder, prefix + ".pcd")
        label_file_path = os.path.join(input_folder, prefix + ".labels")
        
        # Read the point cloud and labels
        pcd = o3d.io.read_point_cloud(pcd_file_path)
        labels = np.loadtxt(label_file_path, dtype=np.int32)
        
        # Count the number of points in the input data
        input_point_count = len(pcd.points)
        
        # Filter out points with label 0
        valid_indices = labels != 0
        pcd_filtered = pcd.select_by_index(np.where(valid_indices)[0])
        labels_filtered = labels[valid_indices]
        
        # Count the number of points in the filtered data
        filtered_point_count = len(pcd_filtered.points)
        
        # Save the filtered point cloud and labels
        o3d.io.write_point_cloud(output_pcd_file_path, pcd_filtered)
        np.savetxt(output_label_file_path, labels_filtered, fmt='%d')
        
        # Calculate time taken for the current file
        time_taken = time.time() - start_time
        
        # Print metrics
        print(f"Processed {prefix}:")
        print(f"  - Input points: {input_point_count}")
        print(f"  - Saved points: {filtered_point_count}")
        print(f"  - Time taken: {time_taken:.2f} seconds")
        print(f"  - Filtered point cloud saved to: {output_pcd_file_path}")
        print(f"  - Filtered labels saved to: {output_label_file_path}\n")
        
        # Update the progress bar
        pbar.update(1)
