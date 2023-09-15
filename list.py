#list is mutable
nums = [12, 35, 4, 99, 122]

result = "all numbers: " + ', '.join(map(str, nums))

print(result)

print(nums[1])

nums.append("aa")
print(nums)

print(nums.index(12))  ##this is for index of any value in list
