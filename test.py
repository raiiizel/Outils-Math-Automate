class CustomFrozenSet(frozenset):
    def __str__(self):
        # Convert the elements to a string representation and join them with commas
        elements_str = ", ".join(str(ele) for ele in self)
        return "{" + elements_str + "}"

# Example usage:
custom_set = CustomFrozenSet({1, 2, 3})
print(custom_set)  # Output: {1, 2, 3}

print([[j for j in i]for i in [1,2,3]])