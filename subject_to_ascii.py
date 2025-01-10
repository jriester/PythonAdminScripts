allowed_chars = [":", ".", "-", "\n"]
# Path to your schema file, example:
  # :.888:prefix-{$subject}
  #:.111:prefix-{$subject}
  #:.999:prefix-{$subject}
  #{$subject123}
  #:.777:prefix-{$subject}
with open("./scratch", "r") as f:
    content = f.read()
    f.close()

output = set()
for l in content:
    if l not in allowed_chars and l.isalnum() is False:
        output.add(l)

for x in output:
    content = content.replace(x, "%" + x.encode("utf-8").hex())

# Outputs the schemas to a file called ascii_schemas.log
with open("ascii_schemas.log", "w") as f:
    f.write(content)
    f.close()
