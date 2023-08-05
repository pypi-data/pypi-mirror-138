
# Seminal root angle extraction

Used for high-throughput phenotyping of rhizobox images.

### Install

The latest version is available via PyPI (https://pypi.org/project/seminal-root-angle) for convenient installation with pip

> pip install seminal-root-angle

### Example usage

Assuming the following folder structure:

    output
    data
    ├── photos
    │   ├── photo1.JPG
    │   ├── photo2.JPG
    │   └── ....
    ├── root_segmentations
    │   ├── photo1.png
    │   ├── photo2.png
    │   └── ....
    └── seed_segmentations
        ├── photo1.png
        └── photo2.png
        └── ....

Then the angles can be extracted to the output/angles.csv with the following python code:

```python
from seminal_root_angle.extract import extract_all_angles
extract_all_angles(root_seg_dir='data/root_segmentations',
                   im_dataset_dir='data/photos',
                   seed_seg_dir='data/seed_segmentations',
                   max_seed_points_per_im=2,
                   debug_image_dir='output/debug_images',
                   output_csv_path='output/angles.csv',
                   error_csv_path='output/errors.csv')
```
