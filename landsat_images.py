import rasterio
import numpy as np
from PIL import Image
import io
import os

folder_path = 'images'
output_path = 'output'

# Reads an image and returns its data
def read_band(band):

    for filename in os.listdir(folder_path):
        file = os.path.join(folder_path, filename)
        
        # Checking if it is a TIF file
        if os.path.isfile(file):
            if file.endswith(f'{band}.TIF'):
                band_file = rasterio.open(file)
                band_data = band_file.read(1).astype(np.float64)
                band_file.close()

                return band_data


def calculate_min_max(band, low=2, high=98):
    non_zero_band = band[band > 0]  # Exclude No-Data values
    band_min = np.nanpercentile(non_zero_band, low)
    band_max = np.nanpercentile(non_zero_band, high)
    return band_min, band_max

# Function to normalize the band using the calculated min and max values
def normalize_band(band):
    min_val, max_val = calculate_min_max(band, 2, 98)
    band = np.clip(band, min_val, max_val)  # Clip values
    return (band - min_val) / (max_val - min_val)


def create_fcc(red_color, green_color, blue_color):

    red_rescale = normalize_band(read_band(red_color))
    green_rescale = normalize_band(read_band(green_color))
    blue_rescale = normalize_band(read_band(blue_color))

    # Create an alpha channel: 1 where data is present, 0 where no-data values (zeroes) are present
    alpha_channel = np.where((read_band(red_color) > 0) & (read_band(green_color) > 0) & (read_band(blue_color) > 0), 1, 0)

    # Stack the RGB bands
    rgba_image = np.dstack((red_rescale, green_rescale, blue_rescale, alpha_channel))

    return rgba_image


def export_composite_file(composite_name, bands):

    composite_data = []
    for band in bands:
        for filename in os.listdir(folder_path):
            file = os.path.join(folder_path, filename)
            
            # Checking if it is a TIF file
            if os.path.isfile(file):
                if file.endswith(f'{band}.TIF'):
                    band_file = rasterio.open(file)
                    band_data = band_file.read(1).astype(np.float64)
                    band_meta = band_file.meta
                    composite_data.append(band_data)
                    band_file.close()

    composite_file = np.stack(composite_data)
    band_meta.update(count=len(bands))

    # Write the composite image to a new file
    with rasterio.open(os.path.join(f'{output_path}/{composite_name}.TIF'), 'w', **band_meta) as output:
        output.write(composite_file)


# Function to downsample the image by selecting every nth pixel
def downsample_image(rgba_image, factor):
    return rgba_image[::factor, ::factor]


def create_thumbnail(rgba_image, max_size_kb, thumbnail_name):

    downsampled_image = downsample_image(rgba_image, 5)

    rgba_downsampled_8bit = (downsampled_image * 255).astype(np.uint8)

    pil_image = Image.fromarray(rgba_downsampled_8bit, mode='RGBA')
    quality = 100

    while True:
        print(quality)
        buffer = io.BytesIO()
        pil_image.save(buffer, format='webp', optimize=True, quality=quality)
        size_kb = buffer.tell() / 1024
        print(size_kb)
        if size_kb <= max_size_kb:
            break
        quality -= 5

        with open(os.path.join(f'{output_path}/{thumbnail_name}.webp'), 'wb') as f:
            f.write(buffer.getvalue())


def calculate_ndi(band_1, band_2):
    np.seterr(invalid='ignore')
    ndi = (band_1 - band_2) / (band_1 + band_2)
    return ndi


def pan_sharpening(pan_band, blue_band, green_band, red_band):

    pan_norm = normalize_band(pan_band)
    blue_norm = normalize_band(blue_band)
    green_norm = normalize_band(green_band)
    red_norm = normalize_band(red_band)

    # Apply the Brovey transform for pan-sharpening
    sum_bands = blue_norm + green_norm + red_norm
    sum_bands[sum_bands == 0] = 1  # To avoid division by zero

    blue_sharpened = (blue_norm * pan_norm) / sum_bands
    green_sharpened = (green_norm * pan_norm) / sum_bands
    red_sharpened = (red_norm * pan_norm) / sum_bands

    # Stack the sharpened bands
    pan_sharpened_image = np.dstack((red_sharpened, green_sharpened, blue_sharpened))

    return pan_sharpened_image