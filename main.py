import landsat_images as li
import matplotlib.pyplot as plt
import numpy as np


# NOTE: Uncomment the part of code needed to run the examples

# TODO: Pan-Sharpening (under-construction)
# TODO: PCA
# TODO: Classifications (supervised non-supervised)
# TODO: Download with API
# TODO: INSERT INTO postgreSQL db
# TODO: Reproject image with proj4
# TODO: 5x5, 9x9 Filters
# TODO: Vegetation Suppression
# TODO: Spectral Signatures
# TODO: Apply Masks
# TODO: Unit-Testing

# TODO: SENTINEL-2

# ------------------------------------------------------------------------
# Visualize FCC
# ------------------------------------------------------------------------

fcc = li.create_fcc('B4', 'B3', 'B2')

plt.figure(figsize=(12, 12))
plt.imshow(fcc)
plt.title('True Color Image')
plt.axis('off')
plt.show()

# ------------------------------------------------------------------------
# Export Composite 
# ------------------------------------------------------------------------

# li.export_composite_file('full_composite_123', ['B1', 'B2', 'B3'])

# ------------------------------------------------------------------------
# Create thumbnail
# ------------------------------------------------------------------------

# fcc = li.create_fcc('B4', 'B3', 'B2')
# li.create_thumbnail(fcc, 500, 'thumbnail_true_color')

# ------------------------------------------------------------------------
# Plot Histogram
# ------------------------------------------------------------------------

# band = li.read_band('B3')[li.read_band('B3') > 0]

# plt.figure(figsize=(10, 6))
# plt.hist(band.ravel(), bins=256, color='red', alpha=0.7)
# plt.title('Histogram of Red Band')
# plt.xlabel('Pixel Value')
# plt.ylabel('Frequency')
# plt.show()

# ------------------------------------------------------------------------
# Plot Histogram (Normalized - Rescaled)
# ------------------------------------------------------------------------

# normalized_band = li.normalize_band(li.read_band('B3')[li.read_band('B3') > 0]) * 255

# plt.figure(figsize=(10, 6))
# plt.hist(normalized_band.ravel(), bins=256, color='red', alpha=0.7)
# plt.title('Histogram of Normalized Red Band')
# plt.xlabel('Pixel Value')
# plt.ylabel('Frequency')
# plt.show()

# ------------------------------------------------------------------------
# Plot histogram for the true color composite
# ------------------------------------------------------------------------

# fcc = li.create_fcc('B4', 'B3', 'B2')

# plt.figure(figsize=(10, 6))
# colors = ('red', 'green', 'blue')
# labels = ('Red Band', 'Green Band', 'Blue Band')

# for i, color in enumerate(colors):
#     band_data = fcc[:, :, i].ravel()
#     plt.hist(band_data, bins=256, color=color, alpha=0.5, label=labels[i])

# plt.title('Histogram of True Color Composite')
# plt.xlabel('Normalized Pixel Value')
# plt.ylabel('Frequency')
# plt.legend()
# plt.show()

# ------------------------------------------------------------------------
# Visualize NDVI
# ------------------------------------------------------------------------

# nir_band = np.where(li.read_band('B5') == 0, np.NAN, li.read_band('B5'))
# red_band = np.where(li.read_band('B4') == 0, np.NAN, li.read_band('B4'))
# ndvi = np.clip(li.calculate_ndi(nir_band, red_band), -1, 1)

# plt.figure(figsize=(12, 12))
# plt.imshow(li.calculate_ndi(li.read_band('B5'), li.read_band('B4')))
# plt.colorbar(label='NDVI')
# plt.set_cmap('Greens_r')
# plt.title('NDVI')
# plt.axis('off')
# plt.show()

# ------------------------------------------------------------------------
# Clip image
# ------------------------------------------------------------------------

# red_band = li.read_band('B4')

# clipped_band = li.clip_image(red_band, (3000, 3000), (3500, 3500))

# plt.figure(figsize=(12, 12))
# plt.imshow(clipped_band)
# plt.title('Clipped red band')
# plt.axis('off')
# plt.show()

# ------------------------------------------------------------------------
# Pan-Sharpening (NOTE: under-construction)
# ------------------------------------------------------------------------

# panchromatic_band = li.read_band('B8')
# red_band = li.read_band('B4')
# green_band = li.read_band('B3')
# blue_band = li.read_band('B2')


