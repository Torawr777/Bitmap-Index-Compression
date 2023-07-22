a4.py generates a bitmap index and can perform WAH (Word Aligned Hybrid) compression on bitmaps indices.
There are two main functions in a4.py:


create_index(input_file, output_path, sorted)

    This generates a bitmap index from the input_file.
    Where: ‘input_file’ is a file that you will use to create the bitmap index. ‘output_path’ is the
    destination directory for your output bitmap file. ‘sorted’ is a boolean value(True or False) that specifies whether your data will be sorted.


compress_index(bitmap_index, output_path, compression_method, word_size)

    This compresses the given bitmap_index.
    Where: ‘bitmap_index’ is the input file that will be used in the compression. ‘output_path’
    is the path to a directory where the compressed version will be written. ‘compression_method’ 
    is a String specifying which bitmap compression method you will be using (in this case; WAH). 
    ‘word_size’ is an integer specifying the word size to be used (8, 16, 32, 64, etc.)

Example runs:

    create_index('mine/animals', 'my_mine', True)
    compress_index('my_mine/animals_sorted', 'my_mine', 'WAH', 64)


If you want the file outputted into the current working directory, leave the output_path paramter empty like so:

    create_index('mine/animals', '', False)