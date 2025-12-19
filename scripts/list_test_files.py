import os

TEST_DIR = "/mnt/d/Ai/WslProject/coffee_bean_receiving_Specification"

def list_files():
    if not os.path.exists(TEST_DIR):
        print(f"Directory not found: {TEST_DIR}")
        return

    print(f"Files in {TEST_DIR}:")
    for f in os.listdir(TEST_DIR):
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf')):
            print(f)

if __name__ == "__main__":
    list_files()
