import shutil
import uuid
from normalize import normalize
from pathlib import Path

CATEGORIES = {"Pictures": ['.JPEG', '.PNG', '.JPG', '.SVG'],
              "Video": ['.AVI', '.MP4', '.MOV', '.MKV'],
              "Documents": ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX', '.RTF'],
              "Audio": ['.MP3', '.OGG', '.WAV', '.AMR'],
              "Archives": ['.ZIP', '.GZ', '.TAR'],
              "Torrent": ['.TORRENT']}

resulted_by_categories = {}
file_cats = set()
other_cats = set()


def unpack_archives(file: Path, root_dir: Path, category: str) -> None:
    path_to_unpack = root_dir.joinpath(f"{category}\\{normalize(file.stem)}")
    shutil.unpack_archive(file, path_to_unpack)
    print(f'File {file} unpacked to directory {path_to_unpack} and deleted.')
    resulted_by_categories[category] = resulted_by_categories.get(
        category, []) + [file.name]
    file.unlink()


def move_file(file: Path, root_dir: Path, category: str) -> None:
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
    new_name = target_dir.joinpath(f"{normalize(file.stem)}{file.suffix}")
    if new_name.exists():
        new_name = new_name.with_name(
            f"{new_name.stem}-{uuid.uuid4()}{file.suffix}")
    file.rename(new_name)
    print(f'File {new_name} moved in directory {target_dir}')
    resulted_by_categories[category] = resulted_by_categories.get(
        category, []) + [new_name.name]


def get_categories(file: Path) -> str:
    ext = file.suffix.upper()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            file_cats.add(ext)
            return cat
    other_cats.add(ext)
    return "Other"


def sort_folder(path: Path) -> None:
    for item in path.glob("**/*"):
        print(item)
        if item.is_file():
            cat = get_categories(item)
            if cat == "Archives":
                unpack_archives(item, path, cat)
            else:
                move_file(item, path, cat)


def delete_folders(path: Path) -> None:
    for item in path.iterdir():
        if item.is_dir():
            delete_folders(item)
        try:
            item.rmdir()
            print(f'{item} was removed')
        except:
            continue


def print_results():
    for i in resulted_by_categories:
        print()
        print(f'    Files moved in folder "{i}"":')
        print(*resulted_by_categories[i], sep='\n')

    if file_cats:
        print()
        print('     Known file categories:')
        print(*file_cats)

    if other_cats:
        print()
        print('     Unknown file categories:')
        print(*other_cats)
        print()


def sort():
    try:
        user_input = input(
            '\nEnter valid path to folder or enter "exit" to leave program \n>>>'
        )

        if user_input == "exit":
            return "End of program!\n"
        if user_input == "":
            print("\nPath cannot be empty!")
            return sort()

        path = Path(user_input)
    except:
        return "No path to folder"

    if not path.exists():
        return f'Folder path {path} do not exists.'

    sort_folder(path)

    delete_folders(path)

    print_results()

    return "Folders sorted"


if __name__ == "__main__":
    sort()
