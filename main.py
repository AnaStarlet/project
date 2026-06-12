def maxArea(height):
    left = 0
    right = len(height) - 1
    max_val = 0
    while left < right:
        width = right - left
        if height[left] < height[right]:
            current_height = height[left]
        else:
            current_height = height[right]
        current_area = width * current_height
        if current_area > max_val:
            max_val = current_area
        if height[left] < height[right]:
            left = left + 1
        else:
            right = right - 1

    return max_val
if __name__ == "__main__":
    array = input("Input: height = ")
    height = [int(x) for x in array.split()]

    result = maxArea(height)
    print("Output:", result)