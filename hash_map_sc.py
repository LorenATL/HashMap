# Name: Loren Starnes
# OSU Email: starnesl@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap Implementation
# Due Date: August 9, 2022
# Description: This program implements the HashMap class using chaining
# for collision resolution. It includes the following methods:
# is_prime, next_prime, get_size, get_capacity, put, get, remove,
# contains_key, clear, empty_buckets, resize_table, table_load,
# and get_keys_and_values.  The program also includes a standalone
# function, find_mode.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map.
        """
        # find array index
        hash = self._hash_function(key)
        index = hash % self._buckets.length()

        # if key already in hash map, remove
        list = self._buckets.get_at_index(index)
        if list.contains(key):
            list.remove(key)
            self._size -= 1

        # insert key/value pair
        list.insert(key, value)
        self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        capacity = self.get_capacity()
        empty = 0
        for i in range(capacity):
            list = self._buckets.get_at_index(i)
            if list.length() == 0:
                empty += 1

        return empty

    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        size = self.get_size()
        capacity = self.get_capacity()
        load_factor = size/capacity
        return load_factor

    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing the underlying table capacity.
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.
        """
        # if new capacity is less than 1, do nothing
        if new_capacity < 1:
            return

        # check that new capacity is prime; if it isn't, change to next highest prime
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        # store existing key/value pairs, update capacity, and clear hash table
        elements = self.get_keys_and_values()
        self._capacity = new_capacity
        self.clear()

        # rehash existing key/value pairs into newly cleared table
        size = elements.length()
        for i in range(size):
            key, value = elements.get_at_index(i)
            self.put(key, value)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.
        """
        # if key isn't in hash table, do nothing
        if self.contains_key(key) is False:
            return None

        # find linked list stored at the array index
        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        list = self._buckets.get_at_index(index)

        # find the node in the linked list with the matching key and return its value
        node = list.contains(key)
        node_value = node.value

        return node_value

    def contains_key(self, key: str) -> bool:
        """
        Returns true if the given key is in the hash map; otherwise, returns false.
        """
        # if the hash table is empty, return False
        if self._size == 0:
            return False

        # find array index where key would be stored
        hash = self._hash_function(key)
        index = hash % self._buckets.length()

        # if key is in the linked list, return True; else return False
        list = self._buckets.get_at_index(index)
        if list.contains(key):
            return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        """
        # if key is in the hash table, find the array index
        if self.contains_key(key) is True:
            hash = self._hash_function(key)
            index = hash % self._buckets.length()
            list = self._buckets.get_at_index(index)

            # remove the key from the linked list and decrement hash table size
            list.remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array containing tuples of key/value pairs in hash map.
        """
        # create array to store key/value pairs
        new_arr = DynamicArray()

        # iterate over each index in array
        capacity = self.get_capacity()
        for i in range(capacity):
            list = self._buckets.get_at_index(i)
            # iterate over each element in linked list and append key/value pairs to new array
            for element in list:
                key = element.key
                value = element.value
                new_arr.append((key, value))

        return new_arr

def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Receives a dynamic array as input and returns a tuple containing a
    dynamic array comprising the mode value(s) of the array and an integer
    representing how many times the mode value(s) appear.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()

    #create mode array
    mode_arr = DynamicArray()

    # length of input array
    length = da.length()

    max_freq = 0

    for i in range(length):
        # if hash map contains key
        key = da.get_at_index(i)
        if map.contains_key(key):
            # get value and increment frequency of that key
            value = map.get(key)
            key_freq = value + 1
            # put key and its frequency in hash table
            map.put(key, key_freq)
        # else, add key to hash map with value of 1
        else:
            map.put(key, 1)
            key_freq = 1

        if key_freq > max_freq:
            max_freq = key_freq

    # build return array with the most occurring value(s) in array and the highest frequency
    map_pairs = map.get_keys_and_values()
    size = map.get_size()
    for i in range(size):
        key, value = map_pairs.get_at_index(i)
        if value == max_freq:
            mode_arr.append(key)

    return mode_arr, max_freq


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(1)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
