from colordescriptor import color_descriptor
from config import get_postgres_connection
import numpy
import faiss
import ast
import argparse
import cv2
import datetime
import forr


def get_total_dataset_dtb():
    connection = get_postgres_connection()
    cursor = connection.cursor()

    cursor.execute(f"""
        select count(*) from image_descriptor;
    """)
    connection.commit()
    rows = cursor.fetchall()
    return int(rows[0][0])


def get_dataset_vector(page, page_size=20000, offset=None):
    connection = get_postgres_connection()
    cursor = connection.cursor()

    if offset is None:
        limit = f" LIMIT {page_size} offset {(page - 1) * page_size}"
    else:
        limit = f" LIMIT {page_size} offset {offset + ((page - 1) * page_size)}"

    cursor.execute(f"""
        select color_descriptor from image_descriptor order by id {limit};
    """)
    connection.commit()
    rows = cursor.fetchall()
    list_vector = []
    for row in rows:
        features = [float(x) for x in row[2].split(',')]
        list_vector.append(features)

    return numpy.array(list_vector)


def get_feature_vector(path_image):
    # define color descriptor
    cd = color_descriptor((8, 12, 3))

    # create ndarray by vectors of image file
    query = cv2.imread(path_image)
    features = cd.describe(query)
    features_vector = [features]

    return numpy.array(features_vector).astype('float32')


def get_index_vector():
    dimension = 1440
    index = faiss.IndexFlatL2(dimension)
    index = faiss.read_index("train.index")
    print(index.ntotal)
    total_dataset_dtb = get_total_dataset_dtb()
    vector_total = index.ntotal
    if total_dataset_dtb > vector_total:
        for page in range(1, 100):
            page_size = 10000

            # find dimention vectors
            if vector_total > 0:
                data_vector = get_dataset_vector(page, page_size, vector_total)
            else:
                data_vector = get_dataset_vector(page, page_size)

            if len(data_vector) > 0:
                vector_total = vector_total + page_size
                # build the index by dimension and add vectors to the index
                data_vector = data_vector.reshape(data_vector.shape[0], -1).astype('float32')
                index.add(data_vector)
                # print(index.ntotal)
            else:
                break

        # write index file to disk
        faiss.write_index(index, 'train.index')
    print(index.ntotal)
    return index


def search_vector(path_image, total_results):
    index = get_index_vector()
    features_vector_search = get_feature_vector(path_image)

    # search image by the feature vector
    D, I = index.search(features_vector_search, total_results)  # actual search
    index.reset()
    return I


def get_image_similar(path_image):
    print(datetime.datetime.now())
    connection = get_postgres_connection()
    cursor = connection.cursor()

    total_results = 10
    result_vector = search_vector(path_image, total_results)
    query = ""
    for j in range(total_results):
        query += f"(select id, path from image_descriptor order by id LIMIT 1 offset {result_vector[0][j]}) union all "

    cursor.execute(query[:-11])
    connection.commit()
    rows = cursor.fetchall()
    print(datetime.datetime.now())
    return rows

if __name__ == '__main__':
    path_image = 'your_path'
    get_image_similar(path_image)
