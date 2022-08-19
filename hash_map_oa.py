# Name: Loren Starnes
# OSU Email: starnesl@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap Implementation
# Due Date: August 9, 2022
# Description: This program implements the HashMap class using a
# dynamic array to store the hash table and implements
# open addressing with quadratic probing for collision resolution.
# It includes several methods, including the following:
# put, get, remove, contains_key, clear, empty_buckets,
# resize_table, table_load, and get_keys_and_values.


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        # if load factor > 0.5, resize to double current capacity
        load_factor = self.table_load()
        if load_factor >= 0.5:
            new_capacity = self.get_capacity() * 2
            self.resize_table(new_capacity)

        # create entry and get capacity of hash table
        entry = HashEntry(key, value)
        capacity = self._capacity

        # find array index and entry at that location
        hash = self._hash_function(key)
        initial_index = hash % self._buckets.length()
        index = initial_index
        bucket = self._buckets.get_at_index(index)
        capacity = self._capacity


        if self.contains_key(key) is True:
            j = 0  # quadratic probing value
            # probe until you find the key
            while bucket.key != key:
                j += 1
                index = (initial_index + j * j) % capacity
                bucket = self._buckets.get_at_index(index)
            self._buckets.set_at_index(index, entry)
        else:
            j = 0  # quadratic probing value
            # probe until you find the key
            while bucket is not None and bucket.is_tombstone is False:
                j += 1
                index = (initial_index + j * j) % capacity
                bucket = self._buckets.get_at_index(index)
            self._buckets.set_at_index(index, entry)
            self._size += 1


    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        size = self.get_size()
        capacity = self.get_capacity()
        load_factor = size/capacity
        return load_factor

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        capacity = self._capacity
        size = self._size
        empty = capacity - size
        return empty

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table and rehashes  all
        existing key/value pairs.
        """
        # if new capacity is less than 1, do nothing
        if new_capacity < self._size:
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

        # find array index and entry at that location
        hash = self._hash_function(key)
        initial_index = hash % self._buckets.length()
        index = initial_index
        bucket = self._buckets.get_at_index(index)
        capacity = self._capacity

        j = 0  # quadratic probing value
        # probe until you find the key and return associated value
        while bucket.key != key:
            j += 1
            index = (initial_index + j * j) % capacity
            bucket = self._buckets.get_at_index(index)

        return bucket.value

    def contains_key(self, key: str) -> bool:
        """
        Returns true if the given key is in the hash map; otherwise, returns false.
        """
        # if the hash table is empty, return False
        if self._size == 0:
            return False

        # find array index and entry at that location
        hash = self._hash_function(key)
        initial_index = hash % self._buckets.length()
        index = initial_index
        bucket = self._buckets.get_at_index(index)
        capacity = self._capacity

        j = 0  # quadratic probing value
        # probe until you find the key
        while bucket is not None and (bucket.is_tombstone is True or bucket.key != key):
            j += 1
            index = (initial_index + j * j) % capacity
            bucket = self._buckets.get_at_index(index)
        if bucket is not None and bucket.key == key:
            return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        """
        # if key is in hash table, find it
        if self.contains_key(key) is True:
            # find array index and entry at that location
            hash = self._hash_function(key)
            initial_index = hash % self._buckets.length()
            index = initial_index
            bucket = self._buckets.get_at_index(index)
            capacity = self._capacity

            j = 0  # quadratic probing value
            # probe until you find the key
            while bucket.key != key:
                j += 1
                index = (initial_index + j * j) % capacity
                bucket = self._buckets.get_at_index(index)
            # remove key by setting tombstone to True and decrement hash table size
            bucket.is_tombstone = True
            self._size -= 1

    def clear(self) -> None:
        """
        Clears the contents of the hash map.
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a
        key/value pair stored in the hash map.
        """
        # create array to store key/value pairs
        new_arr = DynamicArray()
        capacity = self.get_capacity()
        # iterate over each index in array
        for i in range(capacity):
            bucket = self._buckets.get_at_index(i)
            # if index isn't empty, append key/value pair to new array
            if bucket is not None and bucket.is_tombstone is False:
                key = bucket.key
                value = bucket.value
                new_arr.append((key, value))

        return new_arr


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

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())
