# '''
# Linked List hash table key/value pair
# '''


class LinkedPair:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def __repr__(self):
        return f"<{self.key}, {self.value}>"


class HashTable:
    '''
    A hash table that with `capacity` buckets
    that accepts string keys
    '''

    def __init__(self, capacity):
        self.capacity = capacity  # Number of buckets in the hash table
        self.storage = [None] * capacity
        self.entries = 0

    def _hash(self, key):
        '''
        Hash an arbitrary key and return an integer.

        You may replace the Python hash with DJB2 as a stretch goal.
        '''
        return hash(key)

    def _hash_djb2(self, key):
        '''
        Hash an arbitrary key using DJB2 hash

        OPTIONAL STRETCH: Research and implement DJB2
        '''
        pass

    def _hash_mod(self, key):
        '''
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        '''
        return self._hash(key) % self.capacity

    def insert(self, key, value):
        '''
        Store the value with the given key.

        # Part 1: Hash collisions should be handled with an error warning. (Think about and
        # investigate the impact this will have on the tests)

        # Part 2: Change this so that hash collisions are handled with Linked List Chaining.

        Fill this in.
        '''
        # Create LinkedPair obj
        obj = LinkedPair(key, value)
        # Increment entries
        self.entries += 1
        # Linked List Chaining
        index = self._hash_mod(key)
        pair = self.storage[index]
        current_node = pair
        # MVP 2 - Hash Collisions Implemented
        # Check if a pair already exists in the bucket
        if pair is not None and pair.key == key:
            # Overwrite value
            pair.value = value
        # If so, check if it is the right key and if right key overwrite
        elif pair is not None and pair.key != key:
            # loop through until end
            while current_node:
                # If key is found, overwrite value
                if current_node.key == key:
                    current_node.value = value
                    break
                # If no key found, append to tail
                elif current_node.next == None:
                    current_node.next = obj
                    break
                current_node = current_node.next
        else:
            # If not, Create a new LinkedPair and place it in the bucket
            self.storage[index] = obj

    def remove(self, key):
        '''
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Fill this in.
        '''
        self.entries -= 1
        index = self._hash_mod(key)
        # check if pair exists in the bucket with matching keys
        # Linked List Traveral
        current_node = self.storage[index]
        # If the node to be deleted is the head
        if self.storage[index] is not None and self.storage[index].key == key:
            # If so remove that pair by setting it to the linked list next value
            self.storage[index] = self.storage[index].next
            return current_node
        elif self.storage[index] is not None and self.storage[index].key != key:
            while current_node.next:
                # If the next node is the node to be deleted
                if current_node.next.key == key:
                    # save deleted node
                    deleting = current_node.next
                    # Replace current nodes next to the one after deleted
                    current_node.next = deleting.next
                    return deleting
                current_node = current_node.next
        else:
            # Else print warning
            print("Warning: Key does not exist")

    def retrieve(self, key):
        '''
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Fill this in.
        '''
        # Get index from hashmode
        index = self._hash_mod(key)
        # Linked List Traveral
        current_node = self.storage[index]
        # Check if a pair exists in the bucket with matching keys
        if self.storage[index] is not None and self.storage[index].key == key:
            # if so, return the value
            return self.storage[index].value
        elif self.storage[index] is not None and self.storage[index].key != key:
            while current_node:
                if current_node.key == key:
                    return current_node.value
                current_node = current_node.next
        else:
            return None

    def resize(self):
        '''
        Doubles the capacity of the hash table and
        rehash all key/value pairs.

        Fill this in.
        '''
        load_factor = self.entries / self.capacity
        new_capacity = self.capacity * 2
        if load_factor >= 0.7:
            # Create new bigger table
            new_table = [None] * new_capacity
            # Loop through storage
            for pair in self.storage:
                if pair != None:
                    current_node = pair
                    # Traverse current node
                    while current_node:
                        # Save next node
                        next_node = current_node.next
                        # Save new hashing index
                        new_hash_index = self._hash(
                            current_node.key) % new_capacity
                        # Rehash and place current_node in new table
                        # If current index is filled traverse new_table linked list
                        if new_table[new_hash_index] is not None:
                            new_table_head = new_table[new_hash_index]
                            while new_table_head:
                                if new_table_head.next == None:
                                    new_table_head.next = current_node
                                    break
                                new_table_head = new_table_head.next
                        else:
                            new_table[new_hash_index] = current_node
                        # Remove current_nodes next value
                        current_node.next = None
                        # Set current_node -> next_node
                        current_node = next_node
            # Set new_table as the self.storage
            self.storage = new_table
            self.capacity = new_capacity


if __name__ == "__main__":
    ht = HashTable(2)

    ht.insert("line_1", "Tiny hash table")
    ht.insert("line_1", "Tiny hash")
    ht.insert("line_2", "Filled beyond capacity")
    ht.insert("line_3", "Linked list saves the day!")

    print("")
    print(ht.storage)

    # Test storing beyond capacity
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    # Test resizing
    old_capacity = len(ht.storage)
    ht.resize()
    new_capacity = len(ht.storage)

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))
    print(ht.storage)

    print("")
