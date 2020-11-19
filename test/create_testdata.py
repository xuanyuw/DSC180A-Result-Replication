
import gzip

def create_dummy_data(input, output, num_lines):
    with gzip.open(input, 'r') as dummy:
        dummy_short_list = [next(dummy)for x in range(num_lines)]
    
    dummy_short = gzip.compress(b''.join(dummy_short_list))
    
    with open(output, 'wb') as out:
        out.write(dummy_short)
