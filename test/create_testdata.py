import gzip
import os
def create_dummy_data(input, output,output_path, num_lines):
    with gzip.open(input, 'r') as dummy:
        dummy_short_list = [next(dummy)for x in range(num_lines)]
    
    dummy_short = gzip.compress(b''.join(dummy_short_list))
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with open(output, 'wb') as out:
        out.write(dummy_short)
