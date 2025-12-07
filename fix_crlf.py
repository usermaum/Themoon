
import os

file_path = 'dev.sh'

with open(file_path, 'rb') as f:
    content = f.read()

# Replace CRLF with LF
content = content.replace(b'\r\n', b'\n')

# Also handle rogue CRs if any (though usually it's CRLF)
# content = content.replace(b'\r', b'')

with open(file_path, 'wb') as f:
    f.write(content)

print(f"Converted {file_path} to LF line endings.")
