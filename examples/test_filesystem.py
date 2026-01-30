"""
Filesystem API Test

Test love.filesystem module with read, write, and exists functions.
Run with: ./bin/love examples/test_filesystem.py
"""

import love

def love_load():
    print("=== Filesystem API Test ===")
    
    # Test 1: Write a file
    print("\nTest 1: Writing to test file...")
    test_content = "Hello from LOVE2D Python!\nThis is a test file."
    success = love.filesystem.write("test_output.txt", test_content)
    if success:
        print("✓ Write successful")
    else:
        print("✗ Write failed")
    
    # Test 2: Check if file exists
    print("\nTest 2: Checking if file exists...")
    exists = love.filesystem.exists("test_output.txt")
    if exists:
        print("✓ File exists")
    else:
        print("✗ File does not exist")
    
    # Test 3: Read the file back
    print("\nTest 3: Reading file contents...")
    try:
        content = love.filesystem.read("test_output.txt")
        print("✓ Read successful")
        print("Content:", repr(content))
        
        if content == test_content:
            print("✓ Content matches!")
        else:
            print("✗ Content doesn't match")
            print("Expected:", repr(test_content))
            print("Got:", repr(content))
    except Exception as e:
        print("✗ Read failed:", e)
    
    # Test 4: Check non-existent file
    print("\nTest 4: Checking non-existent file...")
    exists = love.filesystem.exists("nonexistent_file.txt")
    if not exists:
        print("✓ Correctly reports file doesn't exist")
    else:
        print("✗ Should not exist")
    
    print("\n=== All tests completed ===")
    
    # Quit after tests
    love.event.quit()

def love_update(dt):
    pass

def love_draw():
    love.graphics.clear(0.1, 0.1, 0.15)
    love.graphics.setColor(0, 1, 0)
    love.graphics.rectangle('fill', 350, 250, 100, 100)

def love_quit():
    print("\nFilesystem test ended!")
