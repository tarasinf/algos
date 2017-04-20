class TarasHash:
    def __init__(self, hash_size=100000):
        self.size = hash_size
        self.slots = [None] * self.size
        self.data = [None] * self.size
    

    def __getitem__(self,key):
        return self.get(key)

    
    def __setitem__(self,key,data):
        self.put(key,data)
    
    def pprint(self):
        print '-- SIZE: %d --' % self.size
        for i in xrange(self.size):
            if self.slots[i] is not None:
                print ' - ', self.slots[i], self.data[i]

    def hash(self, key):
        # for string
        ans = 0
        for i in xrange(len(key)):
            ans += (i + 1) * ord(key[i])

        return ans % self.size
        
    def hashfunction(self, key):
        return key % self.size
    
    def hf(self, key):
        return self.hashfunction(key)
    
    def rehash(self, old_hash):
        return (old_hash + 1) % self.size
    
    
    def get(self, key):
        key_hash = self.hashfunction(key)
        start_key = key_hash
        found = False
        stop = False
        data = None
        
        while self.slots[key_hash] != None and  \
                       not found and not stop:
            if self.slots[key_hash] == key:
                found = True
                data = self.data[key_hash]
            else:
                position=self.rehash(key_hash)
                if key_hash == start_key:
                    stop = True
        return data
    
    
    def put(self, key, data):
        key_hash = self.hashfunction(key)
        
        if self.slots[key_hash] is None:
            self.slots[key_hash] = key
            self.data[key_hash] = data
        else:
            if self.slots[key_hash] == key:
                self.data[key_hash] = data
            else:
                next_key_hash = self.rehash(key_hash)
                while self.slots[next_key_hash] is not None and self.slots[next_key_hash] != key:
                    next_key_hash = self.rehash(next_key_hash)
                    

                self.slots[next_key_hash] = key
                self.data[next_key_hash] = data
        
        
    def delete(self, key):
        key_hash = self.hashfunction(key)
        start_key = key_hash
        
        while self.slots[key_hash] != key and self.slots[key_hash] != None:
            key_hash = self.rehash(key_hash)
            if key_hash == start_key:
                return
            
        self.slots[key_hash] = None
        self.data[key_hash] = None


def ransom_note_taras(magazine, ransom):
    h = TarasHash()

    for word in magazine:
        h[h.hash(word)] = (h[h.hash(word)] + 1) if h[h.hash(word)] is not None else 1
    
    for word in ransom:
        if h[h.hash(word)] is not None:
            if h[h.hash(word)] == 1:
                h.delete(h.hash(word))
            else:
                h[h.hash(word)] -= 1 
        else:
            return False
    return True


        
def ransom_note_python(magazine, ransom):
    h = {}
    for word in magazine:
        h[word] = (h[word] + 1) if word in h else 1
    
    for word in ransom:
        if word in h:
            if h[word] == 1:
                del h[word]
            else:
                h[word] -= 1 
        else:
            return False
    return True
    
def ransom_note(magazine, ransom):
    return ransom_note_taras(magazine, ransom)
    

magazine = 'give me one grand today night'.strip().split(' ')
ransom = 'give one grand today'.strip().split(' ')


if ransom_note(magazine, ransom):
    print "Yes"
else:
    print "No"
