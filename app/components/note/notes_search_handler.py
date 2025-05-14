def on_search_note(self):
    keyword = self.search_input.text().strip().lower()
    if not keyword:
        self.clear_search_highlights()
        return

    for item in self.graph_widget.scene.items():
        if hasattr(item, 'note_data') and hasattr(item, 'remove_highlight'):
            item.remove_highlight()

    matches = []
    for item in self.graph_widget.category_items + self.graph_widget.note_items:
        if hasattr(item, 'note_data'):
            title = item.note_data.get("title", "").lower()
            if keyword in title.split():
                matches.append(item)

    if not matches:
        print("❌ Aucune note trouvée avec ce mot-clé.")
        return

    for item in matches:
        item.highlight()

    if len(matches) == 1:
        self.graph_widget.centerOn(matches[0])
        self.graph_widget.resetTransform()
        self.graph_widget.scale(3, 3)
        print(f"🔍 Note unique trouvée et zoomée : {matches[0].note_data.get('title', '')}")
    else:
        print(f"🔍 {len(matches)} notes trouvées.")

def clear_search_highlights(self):
    for item in self.graph_widget.note_items:
        if hasattr(item, 'remove_highlight'):
            item.remove_highlight()
    self.search_input.clear()
    self.graph_widget.update_category_display()
