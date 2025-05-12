import json
from pathlib import Path
from collections import defaultdict, deque


class TreeStructureGenerator:
    def __init__(self, notes_dir="data/notes", cat_dir="data/categories", output_file="data/categories/category_tree.json"):
        self.notes_dir = Path(notes_dir)
        self.cat_dir = Path(cat_dir)
        self.output_file = Path(output_file)
        self.notes = []
        self.category_tree = {}
        self.category_links = {}
        self.category_notes = defaultdict(list)

    def load_notes(self):
        for file in self.notes_dir.glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                note = json.load(f)
                note_id = note.get("id")
                for keyword in note.get("keywords", []):
                    self.category_notes[keyword].append(note_id)

    def load_category_links(self):
        link_file = self.cat_dir / "link_categories.json"
        if not link_file.exists():
            raise FileNotFoundError("Fichier link_categories.json non trouvé.")
        with open(link_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        graph = defaultdict(set)
        for key, linked in data.items():
            if key.startswith("catégories connectées à "):
                cat = key.replace("catégories connectées à ", "")
                for other in linked:
                    graph[cat].add(other)
                    graph[other].add(cat)  # graphe non orienté
        self.category_links = graph

    def build_category_tree(self):
        visited = set()
        notes_used = set()  # 🆕 Ensemble des notes déjà insérées
        tree = {
            "name": "Cerveau du Designer",
            "type": "root",
            "notes": [],
            "children": []
        }

        def build_subtree(current):
            visited.add(current)
            all_notes = self.category_notes.get(current, [])
            new_notes = [n for n in all_notes if n not in notes_used]
            notes_used.update(new_notes)

            node = {
                "name": current,
                "type": "category",
                "notes": new_notes,
                "children": []
            }
            for neighbor in sorted(self.category_links[current]):
                if neighbor not in visited:
                    child = build_subtree(neighbor)
                    node["children"].append(child)
            return node

        # Étape 1 : détecter les groupes de catégories connectées (composantes connexes)
        components = []
        unvisited = set(self.category_links.keys())

        while unvisited:
            queue = deque()
            start = unvisited.pop()
            queue.append(start)
            group = {start}

            while queue:
                current = queue.popleft()
                for neighbor in self.category_links[current]:
                    if neighbor in unvisited:
                        unvisited.remove(neighbor)
                        group.add(neighbor)
                        queue.append(neighbor)

            components.append(group)

        # Étape 2 : pour chaque groupe, rattacher plusieurs ancres au cerveau
        for group in components:
            sorted_group = sorted(group, key=lambda cat: len(self.category_notes.get(cat, [])), reverse=True)
            anchors = sorted_group[:min(3, len(sorted_group))]  # jusqu'à 3 racines par groupe
            visited.clear()
            for anchor in anchors:
                if anchor not in visited:
                    subtree = build_subtree(anchor)
                    tree["children"].append(subtree)


        return tree


    def save_tree(self, tree):
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(tree, f, indent=4, ensure_ascii=False)
        print(f"✅ Fichier hiérarchique sauvegardé : {self.output_file}")

    def generate(self):
        self.load_notes()
        self.load_category_links()
        tree = self.build_category_tree()
        self.save_tree(tree)


if __name__ == "__main__":
    generator = TreeStructureGenerator()
    generator.generate()
