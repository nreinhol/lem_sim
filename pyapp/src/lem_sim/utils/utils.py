import numpy as np


def split_list_into_n_chunks(l, chunks):
        list_of_array_chunks = np.array_split(l, chunks)
        list_of_list_chunks = []

        # cast numpy arrays into list
        for chunk in list_of_array_chunks:
                list_chunk = chunk.tolist()

                # check for nested lists
                if(type(list_chunk[0]) is list):
                        list_of_list_chunks.append(list_chunk[0])
                else:
                        list_of_list_chunks.append(list_chunk)

        return list_of_list_chunks
