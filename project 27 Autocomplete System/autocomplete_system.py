class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.frequency = 0


class AutocompleteSystem:
    def __init__(self, k=3):
        self.root = TrieNode()
        self.k = k
        self.current_prefix = ""
    
    def insert(self, word, frequency):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.frequency += frequency
    
    def search(self, prefix, update_frequency=False):
        if not prefix:
            return []
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]
        suggestions = []
        self._collect(node, prefix.lower(), suggestions)
        suggestions.sort(key=lambda x: (-x[1], x[0]))
        
        # Update frequency of top result if search is performed
        if update_frequency and suggestions:
            top_word = suggestions[0][0]
            self.insert(top_word, 1)
        
        return [word for word, _ in suggestions[:self.k]]
    
    def _collect(self, node, prefix, suggestions):
        if node.is_end:
            suggestions.append((prefix, node.frequency))
        for char, child in node.children.items():
            self._collect(child, prefix + char, suggestions)
    
    def input(self, character):
        if character == '#':
            if self.current_prefix:
                self.insert(self.current_prefix, 1)
            self.current_prefix = ""
            return []
        self.current_prefix += character
        return self.search(self.current_prefix)
    
    def get_all_words(self):
        all_words = []
        self._collect(self.root, "", all_words)
        all_words.sort(key=lambda x: (-x[1], x[0]))
        return all_words


def main():
    print("\n" + "="*50)
    print("     AUTOCOMPLETE SYSTEM - SEARCH SUGGESTIONS")
    print("="*50 + "\n")
    
    system = AutocompleteSystem(k=3)
    
    # Preload sample data
    for word, freq in [("apple", 10), ("application", 8), ("app", 6), ("april", 4),
                       ("banana", 9), ("band", 5), ("cat", 7), ("car", 8), 
                       ("card", 6), ("dog", 6), ("door", 4)]:
        system.insert(word, freq)
    
    print("System Ready | 11 words loaded | Top-3 suggestions\n")
    
    while True:
        print("-"*50)
        print("[1] Insert  [2] Search  [3] Real-time  [4] View  [5] Exit")
        print("-"*50)
        choice = input("Option: ").strip()
        
        if choice == '1':
            word = input("\nWord: ").strip()
            if word:
                system.insert(word, 1)
                print(f"✓ Added '{word}'\n")
        
        elif choice == '2':
            prefix = input("\nPrefix: ").strip()
            results = system.search(prefix, update_frequency=True)
            if results:
                print(f"→ {results}")
                print(f"✓ '{results[0]}' frequency increased\n")
            else:
                print("✗ No results\n")
        
        elif choice == '3':
            print("\nType one char at a time, '#' to finish:")
            while True:
                char = input("> ").strip()
                if not char or len(char) > 1:
                    continue
                if char == '#':
                    print("✓ Saved\n")
                    break
                print(f"  {system.input(char)}")
        
        elif choice == '4':
            print(f"\n{'WORD':<15} FREQUENCY")
            print("-"*30)
            for word, freq in system.get_all_words():
                print(f"{word:<15} {freq}")
            print()
        
        elif choice == '5':
            print("\n" + "="*50)
            print("     Thank you for using Autocomplete System!")
            print("="*50 + "\n")
            break


if __name__ == "__main__":
    main()
