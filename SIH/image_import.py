import rasterio
import numpy as np
from PIL import Image
import io
from pymongo import MongoClient
import gridfs

# Setup MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']
fs = gridfs.GridFS(db)


def import_multispectral(image_id):
    """
    Import a multispectral image from MongoDB using rasterio.
    """
    file = fs.get(image_id)
    with rasterio.open(io.BytesIO(file.read())) as src:
        image = src.read()
        metadata = src.meta
    return image, metadata


def import_rgb(image_id):
    """
    Import an RGB image from MongoDB using PIL.
    """
    file = fs.get(image_id)
    with Image.open(io.BytesIO(file.read())) as img:
        image = np.array(img)
    return image


def import_thermal(image_id):
    """
    Import a thermal image from MongoDB.
    """
    file = fs.get(image_id)
    with rasterio.open(io.BytesIO(file.read())) as src:
        image = src.read(1)  # Assuming thermal is single-band
        metadata = src.meta
    return image, metadata


def import_image(image_id, image_type):
    """
    General function to import images based on type from MongoDB.
    """
    if image_type == 'multispectral':
        return import_multispectral(image_id)
    elif image_type == 'rgb':
        return import_rgb(image_id)
    elif image_type == 'thermal':
        return import_thermal(image_id)
    else:
        raise ValueError(f"Unsupported image type: {image_type}")


# # Example usage
# try:
#     # Assuming you have the MongoDB ObjectId of the image
#     from bson.objectid import ObjectId
#
#     image_id = ObjectId('your_image_object_id_here')
#
#     rgb_image = import_image(image_id, 'rgb')
#     # Process or use the image as needed
#
# except Exception as e:
#     print(f"Error importing image: {e}")
# finally:
#     client.close()