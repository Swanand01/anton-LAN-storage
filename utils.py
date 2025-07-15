import os


def get_unique_name(base_path, name):
    """Append (1), (2), etc. until a unique name is found."""
    candidate = name
    counter = 1
    while os.path.exists(os.path.join(base_path, candidate)):
        name_parts = os.path.splitext(name)
        if name_parts[1]:  # If it's a file with extension
            candidate = f"{name_parts[0]} ({counter}){name_parts[1]}"
        else:  # Folder
            candidate = f"{name} ({counter})"
        counter += 1
    return candidate


def get_icon_filename(filename, is_folder):
    if is_folder:
        return 'folder.svg'

    ext = os.path.splitext(filename)[1].lower()
    return {
        '.png': 'photo.svg',
        '.jpg': 'photo.svg',
        '.jpeg': 'photo.svg',
        '.gif': 'photo.svg',
        '.svg': 'photo.svg',
        '.pdf': 'document-text.svg',
        '.doc': 'document-text.svg',
        '.docx': 'document-text.svg',
        '.xls': 'document-text.svg',
        '.xlsx': 'document-text.svg',
        '.csv': 'document-text.svg',
        '.zip': 'archive-box.svg',
        '.rar': 'archive-box.svg',
        '.mp3': 'musical-note.svg',
        '.wav': 'musical-note.svg',
        '.mp4': 'video-camera.svg',
        '.mov': 'video-camera.svg',
        '.js': 'code-bracket.svg',
        '.ts': 'code-bracket.svg',
        '.py': 'code-bracket.svg',
        '.txt': 'document-text.svg',
    }.get(ext, 'document-text.svg')
