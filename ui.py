import sys
import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from converter import read_markdown_file, preprocess_md, preprocess_md_fuwari

CHECK_ON      = "☑"
CHECK_OFF     = "☐"
CHECK_PARTIAL = "☒"   # folder: some children checked


# ── Persistence ────────────────────────────────────────────────────────────────

def _save_path():
    base = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) \
        else os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, 'tasklist.json')

def load_tasks():
    try:
        with open(_save_path(), 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(data):
    try:
        with open(_save_path(), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# ── File processing ────────────────────────────────────────────────────────────

def resolve_output_path(input_path, naming_rule):
    if not naming_rule:
        naming_rule = "Opensource_"
    dir_part = os.path.dirname(input_path)
    base     = os.path.basename(input_path)
    name, ext = os.path.splitext(base)
    if naming_rule.endswith('_'):
        out_name = naming_rule + base
    elif naming_rule.startswith('_'):
        out_name = name + naming_rule + ext
    else:
        out_name = naming_rule if '.' in naming_rule else naming_rule + ext
    return os.path.join(dir_part, out_name)

def process_file(input_path, naming_rule, fuwari_meta=None):
    content = read_markdown_file(input_path)
    if content is None:
        return None, f"File not found: {input_path}"
    if fuwari_meta:
        content = preprocess_md_fuwari(
            content,
            fuwari_meta.get('title', ''),
            fuwari_meta.get('description', ''),
            fuwari_meta.get('tags', '[]'),
            fuwari_meta.get('category', ''),
        )
    else:
        content = preprocess_md(content)
    out_path = resolve_output_path(input_path, naming_rule)
    try:
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return out_path, None
    except Exception as e:
        return None, str(e)


# ── UI ─────────────────────────────────────────────────────────────────────────

# Column layout (show='tree headings'):
#   #0  : Path / Name  (tree column, handles indentation)
#   #1  : enabled      (☑ / ☒ / ☐)
#   #2  : naming_rule
#   #3  : status

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Obsidian2OpenMD")
        self.geometry("900x580")
        self.minsize(700, 420)
        self._set_icon()
        self._build()
        self._load_tasks()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ── Icon ──────────────────────────────────────────────────────────────────

    def _set_icon(self):
        # Bundled resources live in sys._MEIPASS when frozen, else next to the script
        if getattr(sys, 'frozen', False):
            base = sys._MEIPASS
        else:
            base = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base, 'res', 'icon_app.ico')
        if os.path.exists(icon_path):
            self.iconbitmap(default=icon_path)

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build(self):
        top = tk.Frame(self, pady=6, padx=8)
        top.pack(fill=tk.X)

        tk.Label(top, text="Mode:").pack(side=tk.LEFT)
        self.mode_var = tk.StringVar(value="plain")
        tk.Radiobutton(top, text="Plain",  variable=self.mode_var, value="plain",
                       command=self._toggle_fuwari).pack(side=tk.LEFT, padx=4)
        tk.Radiobutton(top, text="Fuwari", variable=self.mode_var, value="fuwari",
                       command=self._toggle_fuwari).pack(side=tk.LEFT)

        tk.Button(top, text="Add Files",       command=self._add_files).pack(side=tk.LEFT, padx=(20, 2))
        tk.Button(top, text="Add Folder",      command=self._add_folder).pack(side=tk.LEFT, padx=2)
        tk.Button(top, text="Remove Selected", command=self._remove_selected).pack(side=tk.LEFT, padx=2)
        tk.Button(top, text="Clear All",       command=self._clear_all).pack(side=tk.LEFT, padx=2)
        tk.Button(top, text="Run Checked", bg="#4caf50", fg="white",
                  command=self._run_checked).pack(side=tk.RIGHT, padx=8)

        # Fuwari meta (hidden by default)
        self.fuwari_frame = tk.Frame(self, padx=8, pady=2)
        for label, attr in [("Title", "title"), ("Description", "desc"),
                             ("Tags (comma-separated)", "tags"), ("Category", "cat")]:
            row = tk.Frame(self.fuwari_frame)
            row.pack(fill=tk.X, pady=1)
            tk.Label(row, text=label, width=22, anchor='w').pack(side=tk.LEFT)
            var = tk.StringVar()
            setattr(self, f"_{attr}_var", var)
            tk.Entry(row, textvariable=var).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Task tree — show='tree headings' enables hierarchical indentation
        cols = ("enabled", "naming_rule", "status")
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        self.tree = ttk.Treeview(frame, columns=cols,
                                 show='tree headings', selectmode='extended')
        self.tree.heading('#0',          text='Path / Name')
        self.tree.heading('enabled',     text='')
        self.tree.heading('naming_rule', text='Output Naming Rule')
        self.tree.heading('status',      text='Status')

        self.tree.column('#0',          width=340, stretch=True)
        self.tree.column('enabled',     width=30,  stretch=False, anchor='center')
        self.tree.column('naming_rule', width=170, stretch=False)
        self.tree.column('status',      width=190, stretch=False)

        self.tree.tag_configure('folder', background='#dde8f0', font=('', 9, 'bold'))

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind('<Button-1>',  self._on_click)
        self.tree.bind('<Double-1>',  self._on_double_click)

        # Default naming rule bar
        bot = tk.Frame(self, padx=8, pady=4)
        bot.pack(fill=tk.X)
        tk.Label(bot, text="Default naming rule:").pack(side=tk.LEFT)
        self.default_rule_var = tk.StringVar(value="Opensource_")
        tk.Entry(bot, textvariable=self.default_rule_var, width=20).pack(side=tk.LEFT, padx=4)
        tk.Label(bot,
                 text="  Prefix ending '_'   |   Suffix starting '_'   |   Exact filename",
                 fg="gray").pack(side=tk.LEFT)

        self.status_var = tk.StringVar(value="Ready.")
        tk.Label(self, textvariable=self.status_var, anchor='w',
                 relief=tk.SUNKEN, bd=1).pack(fill=tk.X, side=tk.BOTTOM)

    def _toggle_fuwari(self):
        if self.mode_var.get() == "fuwari":
            self.fuwari_frame.pack(after=self.nametowidget(self.pack_slaves()[0]),
                                   fill=tk.X, padx=8, pady=2)
        else:
            self.fuwari_frame.pack_forget()

    # ── Path helpers ──────────────────────────────────────────────────────────

    def _default_rule(self):
        return self.default_rule_var.get() or "Opensource_"

    def _get_full_path(self, iid):
        """Reconstruct full path by joining from root down."""
        parts = []
        cur = iid
        while cur:
            parts.append(self.tree.item(cur, 'text'))
            cur = self.tree.parent(cur)
        parts.reverse()
        # parts[0] is always the full path of the top-level item;
        # deeper parts are basenames → os.path.join handles correctly.
        return os.path.join(*parts)

    # ── Folder depth check ────────────────────────────────────────────────────

    def _folder_depth(self, folder):
        """Return max subfolder nesting depth (0 = only files in root)."""
        max_d = 0
        for root, dirs, _ in os.walk(folder):
            rel = os.path.relpath(root, folder)
            d = 0 if rel == '.' else len(rel.split(os.sep))
            max_d = max(max_d, d)
        return max_d

    # ── Row insertion ─────────────────────────────────────────────────────────

    def _insert_folder_recursive(self, path, parent_iid, rule=None):
        """Insert a folder row and recursively add subfolders and .md files."""
        if rule is None:
            rule = self._default_rule()
        # Top-level: show full path; nested: show only folder name
        display = path if parent_iid == '' else os.path.basename(path)
        iid = self.tree.insert(parent_iid, tk.END, text=display,
                               values=(CHECK_ON, rule, ''),
                               tags=('folder',), open=True)
        try:
            entries = sorted(os.listdir(path))
        except PermissionError:
            return iid

        for entry in entries:
            entry_path = os.path.join(path, entry)
            if os.path.isdir(entry_path):
                self._insert_folder_recursive(entry_path, iid, rule)
            elif entry.endswith('.md'):
                self.tree.insert(iid, tk.END, text=entry,
                                 values=(CHECK_ON, rule, 'Pending'),
                                 tags=('file',))
        return iid

    def _insert_standalone_row(self, path, rule=None, enabled=True, status="Pending"):
        """Top-level file row (added via Add Files or loaded from session)."""
        if rule is None:
            rule = self._default_rule()
        check = CHECK_ON if enabled else CHECK_OFF
        self.tree.insert('', tk.END, text=path,
                         values=(check, rule, status),
                         tags=('file',))

    # ── Add / Remove ──────────────────────────────────────────────────────────

    def _add_files(self):
        paths = filedialog.askopenfilenames(
            title="Select Markdown files",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
        )
        for p in paths:
            self._insert_standalone_row(p)

    def _add_folder(self):
        folder = filedialog.askdirectory(title="Select folder")
        if not folder:
            return
        depth = self._folder_depth(folder)
        if depth > 2:
            messagebox.showwarning(
                "Folder nesting too deep",
                f"The selected folder has {depth} levels of subfolders.\n\n"
                "It is not recommended to process folders with more than 2 levels of nesting.\n"
                "Please reselect a folder whose subfolder depth does not exceed 2 levels."
            )
            return
        iid = self._insert_folder_recursive(folder, '')
        self._update_folder_state(iid)

    def _remove_selected(self):
        for item in list(self.tree.selection()):
            if not self.tree.exists(item):
                continue
            parent = self.tree.parent(item)
            self.tree.delete(item)
            if parent and self.tree.exists(parent):
                self._update_folder_state(parent)

    def _clear_all(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    # ── Checkbox logic ────────────────────────────────────────────────────────

    def _on_click(self, event):
        if self.tree.identify("region", event.x, event.y) != "cell":
            return
        if self.tree.identify_column(event.x) != "#1":   # enabled column
            return
        item = self.tree.identify_row(event.y)
        if not item:
            return
        if 'folder' in self.tree.item(item, 'tags'):
            self._toggle_folder(item)
        else:
            self._toggle_file(item)

    def _toggle_folder(self, folder_iid):
        current   = self.tree.set(folder_iid, "enabled")
        new_state = CHECK_OFF if current != CHECK_OFF else CHECK_ON
        self._set_subtree_state(folder_iid, new_state)
        parent = self.tree.parent(folder_iid)
        if parent:
            self._update_folder_state(parent)

    def _toggle_file(self, file_iid):
        current = self.tree.set(file_iid, "enabled")
        self.tree.set(file_iid, "enabled", CHECK_OFF if current == CHECK_ON else CHECK_ON)
        parent = self.tree.parent(file_iid)
        if parent:
            self._update_folder_state(parent)

    def _set_subtree_state(self, item, state):
        """Recursively set enabled state for item and all descendants."""
        self.tree.set(item, "enabled", state)
        for child in self.tree.get_children(item):
            self._set_subtree_state(child, state)

    def _update_folder_state(self, folder_iid):
        """
        Recalculate ☑ / ☒ / ☐ for a folder based on its direct children,
        then propagate upward to any grandparent folders.
        """
        children = self.tree.get_children(folder_iid)
        if not children:
            return
        states = [self.tree.set(c, "enabled") for c in children]
        if all(s == CHECK_ON for s in states):
            self.tree.set(folder_iid, "enabled", CHECK_ON)
        elif all(s == CHECK_OFF for s in states):
            self.tree.set(folder_iid, "enabled", CHECK_OFF)
        else:
            self.tree.set(folder_iid, "enabled", CHECK_PARTIAL)
        parent = self.tree.parent(folder_iid)
        if parent:
            self._update_folder_state(parent)

    # ── In-place edit (naming_rule, column #2) ────────────────────────────────

    def _on_double_click(self, event):
        if self.tree.identify("region", event.x, event.y) != "cell":
            return
        if self.tree.identify_column(event.x) != "#2":   # naming_rule column
            return
        item = self.tree.identify_row(event.y)
        if not item:
            return

        x, y, w, h = self.tree.bbox(item, "#2")
        entry_var = tk.StringVar(value=self.tree.set(item, "naming_rule"))
        entry = tk.Entry(self.tree, textvariable=entry_var)
        entry.place(x=x, y=y, width=w, height=h)
        entry.focus()

        def save(e=None):
            new_rule = entry_var.get()
            self.tree.set(item, "naming_rule", new_rule)
            # Folder: propagate to all descendants
            if 'folder' in self.tree.item(item, 'tags'):
                self._propagate_rule(item, new_rule)
            entry.destroy()

        entry.bind("<Return>",   save)
        entry.bind("<FocusOut>", save)

    def _propagate_rule(self, folder_iid, rule):
        for child in self.tree.get_children(folder_iid):
            self.tree.set(child, "naming_rule", rule)
            if 'folder' in self.tree.item(child, 'tags'):
                self._propagate_rule(child, rule)

    # ── Run ───────────────────────────────────────────────────────────────────

    def _all_file_items(self):
        """Collect all leaf file iids recursively."""
        result = []
        def collect(parent=''):
            for item in self.tree.get_children(parent):
                if 'folder' in self.tree.item(item, 'tags'):
                    collect(item)
                else:
                    result.append(item)
        collect()
        return result

    def _get_fuwari_meta(self):
        tags_list = list(set(
            t.strip() for t in self._tags_var.get().split(',') if t.strip()
        ))
        return {
            'title':       self._title_var.get(),
            'description': self._desc_var.get(),
            'tags':        str(tags_list).replace("'", '"'),
            'category':    self._cat_var.get(),
        }

    def _run_checked(self):
        all_files = self._all_file_items()
        checked   = [i for i in all_files if self.tree.set(i, "enabled") == CHECK_ON]
        if not checked:
            messagebox.showinfo("Nothing to do",
                                "No tasks are checked. Tick ☑ on the rows you want to run.")
            return

        fuwari_meta = self._get_fuwari_meta() if self.mode_var.get() == "fuwari" else None
        success, errors = 0, 0

        for item in checked:
            self.tree.set(item, "status", "Processing…")
            self.update_idletasks()
            input_path   = self._get_full_path(item)
            naming_rule  = self.tree.set(item, "naming_rule")
            out_path, err = process_file(input_path, naming_rule, fuwari_meta)
            if err:
                self.tree.set(item, "status", f"Error: {err}")
                errors += 1
            else:
                self.tree.set(item, "status", f"Done → {os.path.basename(out_path)}")
                success += 1

        skipped = len(all_files) - len(checked)
        self.status_var.set(
            f"Finished: {success} succeeded, {errors} failed, {skipped} skipped."
        )

    # ── Persistence ───────────────────────────────────────────────────────────

    def _serialise_item(self, item):
        """Recursively serialise a tree item to a dict."""
        path = self._get_full_path(item)
        if 'folder' in self.tree.item(item, 'tags'):
            return {
                'type':     'folder',
                'path':     path,
                'rule':     self.tree.set(item, "naming_rule"),
                'children': [self._serialise_item(c)
                             for c in self.tree.get_children(item)],
            }
        return {
            'type':    'file',
            'path':    path,
            'rule':    self.tree.set(item, "naming_rule"),
            'enabled': self.tree.set(item, "enabled") == CHECK_ON,
            'status':  self.tree.set(item, "status"),
        }

    def _load_item(self, task, parent_iid=''):
        """Recursively restore a tree item from a saved dict."""
        path    = task['path']
        display = path if parent_iid == '' else os.path.basename(path)
        rule    = task.get('rule', 'Opensource_')

        if task.get('type') == 'folder':
            iid = self.tree.insert(parent_iid, tk.END, text=display,
                                   values=(CHECK_ON, rule, ''),
                                   tags=('folder',), open=True)
            for child in task.get('children', []):
                self._load_item(child, iid)
            self._update_folder_state(iid)
        else:
            check = CHECK_ON if task.get('enabled', True) else CHECK_OFF
            self.tree.insert(parent_iid, tk.END, text=display,
                             values=(check, rule, task.get('status', 'Pending')),
                             tags=('file',))

    def _load_tasks(self):
        for task in load_tasks():
            self._load_item(task)

    def _save_current_tasks(self):
        save_tasks([self._serialise_item(i) for i in self.tree.get_children()])

    def _on_close(self):
        self._save_current_tasks()
        self.destroy()


# ── CLI entry ──────────────────────────────────────────────────────────────────

def cli_mode(file_path):
    print(f"Processing file: {file_path}")
    content = read_markdown_file(file_path)
    if content is None:
        print("Error: file not found.")
        input("Press Enter to exit...")
        return
    content  = preprocess_md(content)
    out_path = resolve_output_path(file_path, "Opensource_")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Done!")
    print(f"Processed markdown file saved to '{out_path}'")
    input("Press Enter to exit...")


if __name__ == "__main__":
    # Set AppUserModelID so Windows taskbar shows the correct icon
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "obsidian2openmd.app"
        )
    except Exception:
        pass

    if len(sys.argv) > 1:
        cli_mode(sys.argv[1])
    else:
        app = App()
        app.mainloop()
