from colordescriptor import color_descriptor
from config import get_postgres_connection
import argparse
import glob
import cv2

path_dataset = "./dataset"

connection = get_postgres_connection()
cursor = connection.cursor()

cd = color_descriptor((8, 12, 3))

# accept extension file of image
ext = ['png', 'jpg', 'jpeg']

for e in ext:
    for imagePath in glob.glob(path_dataset + "/**/*." + e, recursive=True):
        try:
            image = cv2.imread(imagePath)

            features = cd.describe(image)

            features = [str(f) for f in features]
            features = ",".join(features)

            # insert features to database
            cursor.execute(f"""
                    INSERT INTO image_descriptor (path, color_descriptor)
                    VALUES ($${imagePath}$$, $${features}$$)
                    ON CONFLICT DO NOTHING;
                """)
            connection.commit()
        except:
            print(imagePath)
