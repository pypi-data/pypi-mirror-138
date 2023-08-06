"""
Create a GUI to allow an easy control for any user :D
"""
import os.path
import tkinter as tk
from glob import glob
from pathlib import Path
from tkinter import ttk, filedialog
from tkinter.messagebox import showerror, showinfo
from urllib.parse import urlparse

import yaml
from PIL import Image
from PIL import ImageTk
from ttkthemes import ThemedTk

import Obsidian_Snippeter as manager
from Obsidian_Snippeter.src import environment as envi
from Obsidian_Snippeter.src import github_action as gt


def git_pull(repo_path):
    """
    Pull the repository to get the lasts updates.
    :param repo_path: The repo to update
    :return: /
    """
    exc = gt.git_pull(repo_path)
    if exc != "0":
        showerror(title="WARNING", message=f"Git returns an error : {exc}")


def git_clone(repo_url):
    """
    Clone repository
    :param repo_url: Github URL to repository
    :return: Cloned directory path / info message if fail
    """
    dir, message = gt.git_clone(repo_url)
    return dir


def get_environment():
    """
    Get environment value from files
    :return: vault : Path / Basedir : Path
    """
    VAULT, BASEDIR = envi.get_environments()
    if len(str(VAULT)) == 0 or len(str(BASEDIR)) == 0:
        return "", ""
    return VAULT, BASEDIR


def browsefunc(entry, config):
    """
    Browse function to select folder path and insert in entry
    :param entry: entry to insert the path
    :param config: Configuration frame
    :return: /
    """
    entry.delete(0, "end")
    filename = filedialog.askdirectory(parent=config)
    filename = str(Path(filename))
    entry.insert("end", filename)


def save_env(vault, folder_snippet):
    """
    Save vault environment in configuration file
    create .snippets if not exists
    create exclude.yml if not exists
    :param vault: Vault path
    :param folder_snippet: Folder snippet path
    :return: /
    """
    basedir = manager.__path__[0]
    env_path = Path(f"{basedir}/.obsidian-snippet-manager")
    if (
        vault == ""
        or not os.path.isdir(Path(vault))
        or not os.path.isdir(os.path.join(vault, ".obsidian"))
    ):
        showerror(title="❌❌❌❌❌❌", message="Invalid vault path !")
    elif folder_snippet == "" or not os.path.isdir(Path(folder_snippet)):
        showerror(title="❌❌❌❌❌❌", message="Invalid Manager Snippet path !")
    elif (
        vault == ""
        or not os.path.isdir(Path(vault))
        or folder_snippet == ""
        or not os.path.isdir(Path(folder_snippet))
    ):
        showerror(title="❌❌❌❌❌❌", message="Invalid path for both !")
    else:
        with open(env_path, "w", encoding="utf-8") as env:
            env.write(f"vault={vault}\n")
            env.write(f"folder_snippet={folder_snippet}\n")
        excluded = os.path.join(folder_snippet, "exclude.yml")
        if not os.path.isfile(Path(excluded)):
            f = open(excluded, "w", encoding="utf-8")
            f.close()
        snippets = os.path.join(vault, ".obsidian", "snippets")
        Path(snippets).mkdir(exist_ok=True)  # Create snippets folder if not exists


def download(url, tree, exclude_tree, clone_exclude):
    """
    Clone a repository
    Move CSS to obsidian
    :param url: URL to repo
    :param tree: Update treeview
    :param exclude_tree: Exclude treeview
    :param clone_exclude: Checkbox value
    :return: /
    """
    repo_path = git_clone(url)
    repo_name = urlparse(url).path[1:].split("/")[1]
    if repo_path == "Already exists":
        showerror(title="❌❌❌❌❌❌", message=f"{repo_name} already exists.")
    elif repo_path == "0":
        showerror(title="❌❌❌❌❌❌", message=f"{repo_name} doesn't exists.")
    else:
        css_file = gt.move_to_obsidian(repo_path)
        if len(css_file) > 0:
            showinfo(
                title="🎉🎉🎉🎉🎉",
                message=f"{repo_name} successfully added to Obsidian !",
            )
            reload(tree)
            reload(exclude_tree)
            if clone_exclude.instate(["selected"]):
                gt.exclude_folder(repo_path)
        else:
            showerror(title="❌❌❌❌❌❌", message=f"There is no CSS file in {repo_name}.")


def reload(tree):
    """
    Reload treeview with new contents
    Select all contents by default
    Update the select button
    :param tree: Treeview to reload
    :return: /
    """
    BASEDIR, VAULT = get_environment()
    tree.delete(*tree.get_children())
    all_repo = [x for x in glob(os.path.join(str(BASEDIR), "**")) if os.path.isdir(x)]
    for i, name in enumerate(all_repo):
        tupled = (str(name),)
        repo_name = os.path.basename(name)
        tree.insert("", i, text=repo_name, values=tupled)
    if len(all_repo) > 0:
        selection_all(tree)
    tree.heading("#0", text="Unselect all Snippets")


def selection_all(tree):
    """
    Select all files
    :param tree: Treeview to select files
    :return: /
    """
    tree.selection_set(tree.get_children())


def unselect_all(tree):
    """
    Unselect all files
    :param tree: Treeview to deselect contents
    :return: /
    """
    for item in tree.selection():
        tree.selection_remove(item)


def switch(tree):
    """
    Switch between select/deselect
    :param tree: Treeview
    :return:
    """
    if len(tree.get_children()) > 1:
        if len(tree.selection()) < len(tree.get_children()) - 1:
            tree.heading("#0", text="Unselect all Snippets")
            selection_all(tree)
        else:
            tree.heading("#0", text="Select all Snippets")
            unselect_all(tree)


def message_info(info):
    """
    Create a message based on the length of provided info
    :param info: list of repo
    :return:
    """
    if len(info) > 1:
        info = "\n- ".join(info)
        info = "\n- " + info
    elif len(info) == 1:
        info = "".join(info)
    else:
        info = ""
    return info


def update_selected(tree):
    """
    Update the selected snippets
    :param tree: Snippet treeview
    :return: /
    """
    BASEDIR, VAULT = get_environment()
    data = tree.selection()
    exclude_file = os.path.join(BASEDIR, "exclude.yml")
    if os.path.isfile(exclude_file):
        with open(exclude_file, "r", encoding="utf-8") as f:
            exclude = yaml.safe_load(f)
    else:
        f = open(exclude_file, "w", encoding="utf-8")
        f.close()
        exclude = []
    info = []
    no_css = []
    git_repo = []
    for i in data:
        if len(tree.item(i)["values"]) > 0:
            repo_path = tree.item(i)["values"][0]
            repo_name = tree.item(i)["text"]
            if (
                os.path.isdir(os.path.join(repo_path, ".git"))
                and not repo_name in exclude
            ):
                git_pull(repo_path)
                css_file = gt.move_to_obsidian(repo_path)
                if len(css_file) > 0:
                    info.append(f"{repo_name}")
                else:
                    no_css.append(repo_name)
            else:
                git_repo.append(repo_name)
    info = message_info(info)
    no_css = message_info(no_css)
    git_repo = message_info(git_repo)
    if info != "":
        showinfo(title="🎉🎉🎉🎉🎉", message=f"Successfully updated {info} !")
    if no_css != "":
        showerror(title="❌❌❌❌❌❌", message=f"There is no CSS in {no_css}")
    if git_repo != "":
        showerror(title="❌❌❌❌❌❌", message=f"There is nothing to update in: {git_repo} ")


def exclude_selected(exclude_tree):
    """
    Add to exclude.yml selected snippet
    :param exclude_tree: Exclude treeview
    :return:
    """
    data = exclude_tree.selection()
    info = []
    for i in data:
        if len(exclude_tree.item(i)["values"]) > 0:
            repo_path = exclude_tree.item(i)["values"][0]
            repo_name = exclude_tree.item(i)["text"]
            gt.exclude_folder(repo_path)
            info.append(repo_name)
    if len(info) == 1:
        showinfo(
            title="🎉🎉🎉🎉🎉",
            message=f"{info[0]} successfully excluded from future update !",
        )
    elif len(info) > 1:
        info = "\n-" + "\n- ".join(info)
        showinfo(title="🎉🎉🎉🎉🎉", message=f"Excluded from future update:{info}")


def configuration_menu(config):
    """
    Create the configuration frame
    :param config: Frame
    :return: /
    """
    browse_path = os.path.join(manager.__path__[0], "src", "gui_bin", "folder.png")
    browse_icon = Image.open(browse_path).resize((18, 18), Image.ANTIALIAS)
    browse_png = ImageTk.PhotoImage(browse_icon)

    config1 = ttk.Label(
        config,
        text="Vault Path",
        font=("Ubuntu", 10, "bold"),
        justify=tk.LEFT,
        anchor="w",
    )
    config1.grid(row=0, column=1, ipadx=5, sticky=tk.W)
    vault_ui = ttk.Entry(config, font=40)
    BASEDIR, VAULT = get_environment()
    vault_ui.grid(row=0, column=2, ipadx=100)
    vault_ui.insert("end", str(VAULT))
    b1 = ttk.Button(
        config,
        text="browse",
        command=lambda: browsefunc(vault_ui, config),
        image=browse_png,
        padding=3,
    )
    b1.grid(row=0, column=3)

    config2 = ttk.Label(
        config,
        text="Folder Manager",
        font=("Ubuntu", 10, "bold"),
        justify=tk.LEFT,
        anchor="w",
    )
    config2.grid(row=1, column=1, ipadx=5, sticky=tk.W)
    manager_ui = ttk.Entry(config, font=40)
    manager_ui.grid(row=1, column=2, ipadx=100)
    manager_ui.insert("end", BASEDIR)

    b2 = ttk.Button(
        config,
        text="browse",
        command=lambda: browsefunc(manager_ui, config),
        image=browse_png,
        padding=3,
    )
    b2.grid(row=1, column=3)

    b3 = ttk.Button(
        config, text="Save", command=lambda: save_env(vault_ui.get(), manager_ui.get())
    )
    b3.grid(row=2, column=2)


def clone_menu(clone, tree, exclude_tree):
    """
    Create the clone menu
    :param clone: Frame
    :param tree: Clone treeview
    :param exclude_tree: exclude treeview
    :return:
    """
    clone_url = ttk.Label(
        clone,
        text="URL",
        font=("Ubuntu", 10, "bold"),
        justify=tk.CENTER,
        anchor="center",
    )
    clone_url.grid(row=0, column=0, ipadx=10)
    clone_entry = ttk.Entry(clone, font=40)
    clone_entry.grid(row=0, column=1, ipadx=150)
    clone_exclude = ttk.Checkbutton(clone)
    clone_exclude_label = ttk.Label(
        clone,
        text="Exclude from update",
        font=("Ubuntu", 10, "bold"),
        justify=tk.CENTER,
        anchor="e",
        padding=(50, 0, 0, 0),
    )
    clone_exclude_label.grid(row=1, column=1, sticky="w")
    clone_exclude.grid(row=1, column=1, sticky="ne", ipadx=120)

    clone_download = ttk.Button(
        clone,
        text="Download",
        command=lambda: download(clone_entry.get(), tree, exclude_tree, clone_exclude),
    )
    clone_download.grid(row=2, column=1, ipadx=120)


def update_menu(update):
    """
    Create the update menu
    :param update: Frame
    :return: treeview
    """
    BASEDIR, VAULT = get_environment()
    update.grid_columnconfigure(0, weight=1)
    update.grid_columnconfigure(1, weight=0)

    tree = ttk.Treeview(update)
    tree.column("#0")
    tree.heading(
        "#0",
        text="Unselect all Snippets",
        anchor=tk.CENTER,
        command=lambda: switch(tree),
    )
    tree.insert("", "end", "Snippets")
    all_repo = [x for x in glob(os.path.join(str(BASEDIR), "**")) if os.path.isdir(x)]
    for i, name in enumerate(all_repo):
        tupled = (str(name),)
        repo_name = os.path.basename(name)
        tree.insert("", i, text=repo_name, values=tupled)
    tree.grid(column=0, row=2, sticky="ew")
    if len(all_repo) > 0:
        tree.selection_set(tree.get_children())
    update_all = ttk.Button(
        update, text="Update selected Snippets", command=lambda: update_selected(tree)
    )
    refresh = ttk.Button(update, text="Refresh Snippets", command=lambda: reload(tree))
    update_all.grid(column=0, row=3, sticky="ew")
    refresh.grid(column=0, row=3, sticky="ne")
    return tree


def exclude_menu(delete):
    """
    Create exclude menu
    :param delete: frame
    :return: exclude treeviewx
    """
    BASEDIR, VAULT = get_environment()
    delete.grid_columnconfigure(0, weight=1)
    delete.grid_columnconfigure(1, weight=0)
    all_repo = [x for x in glob(os.path.join(str(BASEDIR), "**")) if os.path.isdir(x)]

    exclude_tree = ttk.Treeview(delete)
    exclude_tree.column("#0")
    exclude_tree.heading(
        "#0",
        text="Unselect all Snippets",
        anchor=tk.CENTER,
        command=lambda: switch(exclude_tree),
    )
    exclude_tree.insert("", "end", "Snippets")
    for i, name in enumerate(all_repo):
        tupled = (str(name),)
        repo_name = os.path.basename(name)
        exclude_tree.insert("", i, text=repo_name, values=tupled)
    exclude_tree.grid(column=0, row=2, sticky="ew")
    if len(all_repo) > 0:
        exclude_tree.selection_set(exclude_tree.get_children())
    exclude_button = ttk.Button(
        delete,
        text="Add to excluded selected snippets",
        command=lambda: exclude_selected(exclude_tree),
    )
    refresh_exclude = ttk.Button(
        delete, text="Refresh Snippets", command=lambda: reload(exclude_tree)
    )
    exclude_button.grid(column=0, row=3, sticky="ew")
    refresh_exclude.grid(column=0, row=3, sticky="ne")
    return exclude_tree


def main():
    """
    Main function to create and call GUI
    :return: /
    """
    root = ThemedTk(theme="breeze")
    root.title("Obsidian Snippets Manager")
    image_path = os.path.join(manager.__path__[0], "src", "gui_bin", "hand.png")
    root.iconphoto(True, tk.PhotoImage(file=image_path))
    menu = ttk.Notebook(root)
    menu.grid()

    # Tab :
    # 1. Update (main)
    # 2. Clone - download
    # 3. Delete
    # 4. Configuration

    update = ttk.Frame(menu)
    update.grid()

    clone = ttk.Frame(menu)
    clone.grid()

    delete = ttk.Frame(menu)
    delete.grid()

    config = ttk.Frame(menu)
    config.grid()

    menu.add(update, text="Update")
    menu.add(clone, text="Clone")
    menu.add(delete, text="Exclude")
    menu.add(config, text="Configuration")

    configuration_menu(config)
    tree = update_menu(update)
    exclude_tree = exclude_menu(delete)
    clone_menu(clone, tree, exclude_tree)

    root.mainloop()


if __name__ == "__main__":
    main()
