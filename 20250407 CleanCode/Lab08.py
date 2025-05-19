import time

names = ["john doe", "jane smith", "bob johnson"]

two_part_name_count = 0
for name in names:
    name_parts = name.split()
    if len(name_parts) == 2:
        first_name, last_name = name_parts
        print(f"{first_name} {last_name}")
        two_part_name_count += 1
    time.sleep(1)

print(f"總共有 {two_part_name_count} 個名字包含兩個部分。")