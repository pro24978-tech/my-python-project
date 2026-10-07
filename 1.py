import os
import shutil
from pathlib import Path
from datetime import datetime


# ================== ЧАСТЬ 1. КОПИРОВАНИЕ С ПЕРЕИМЕНОВАНИЕМ В .txt ==================

def copy_folder_as_txt(source_folder: str, dest_folder: str,
                       new_ext: str = ".txt",
                       skip_names=(".git", "__pycache__", ".venv", "venv",
                                   "node_modules", ".idea", ".mypy_cache",
                                   ".pytest_cache")):
    """
    Копирует всю папку source_folder в dest_folder,
    но ВСЕ скопированные файлы получают расширение new_ext (по умолчанию .txt).
    Оригинал не трогается.
    """
    src = Path(source_folder).resolve()
    dst = Path(dest_folder).resolve()

    if not src.exists() or not src.is_dir():
        raise ValueError(f"Папка-источник не найдена: {src}")

    # чистим старую копию, чтобы была ровно «в точь-в-точь»
    if dst.exists():
        print(f"⚠️  Удаляю старую копию: {dst}")
        shutil.rmtree(dst)

    dst.mkdir(parents=True, exist_ok=True)

    copied = 0
    renamed = 0

    for root, dirs, files in os.walk(src):
        # не заходим в служебные папки
        dirs[:] = [d for d in dirs if d not in skip_names]

        rel = Path(root).relative_to(src)
        target_dir = dst / rel
        target_dir.mkdir(parents=True, exist_ok=True)

        for name in files:
            src_file = Path(root) / name

            # --- формируем имя с расширением .txt ---
            stem = src_file.stem                 # имя без расширения
            new_name = stem + new_ext            # например "main" -> "main.txt"

            # если файл без имени (бывает .env, .gitignore) — добавляем префикс
            if not stem:
                new_name = name.lstrip(".") + new_ext

            dst_file = target_dir / new_name

            # защита от коллизий: если уже есть такой файл — добавим _1, _2 ...
            counter = 1
            while dst_file.exists():
                dst_file = target_dir / f"{stem}_{counter}{new_ext}"
                counter += 1

            try:
                shutil.copy2(src_file, dst_file)
                copied += 1
                if dst_file.suffix.lower() != src_file.suffix.lower():
                    renamed += 1
            except Exception as e:
                print(f"  [ошибка копирования] {src_file} -> {e}")

    print(f"✅ Скопировано файлов: {copied} (переименовано в {new_ext}: {renamed})")
    print(f"   Из: {src}")
    print(f"   В:  {dst}")
    return dst


# ================== ЧАСТЬ 2. ДАМП ВСЕХ .txt В ОДИН ФАЙЛ ==================

def collect_txt_to_one(source_folder: str, output_file: str,
                       max_file_size_mb: float = 5.0):
    """Собирает содержимое всех .txt файлов из папки в один общий txt."""
    source = Path(source_folder).resolve()
    output = Path(output_file).resolve()
    max_size = max_file_size_mb * 1024 * 1024

    if not source.exists() or not source.is_dir():
        raise ValueError(f"Папка не найдена: {source}")

    all_files = sorted(p for p in source.rglob("*.txt")
                       if p.resolve() != output)

    with open(output, 'w', encoding='utf-8') as out:
        out.write("=" * 80 + "\n")
        out.write(f"СОДЕРЖИМОЕ ПАПКИ: {source}\n")
        out.write(f"Дата: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
        out.write(f"Всего файлов: {len(all_files)}\n")
        out.write("=" * 80 + "\n")

        for i, file_path in enumerate(all_files, 1):
            rel = file_path.relative_to(source)
            size = file_path.stat().st_size

            out.write("\n" + "=" * 80 + "\n")
            out.write(f"[{i}/{len(all_files)}] ФАЙЛ: {rel}\n")
            out.write(f"Размер: {size} байт\n")
            out.write("=" * 80 + "\n\n")

            if size > max_size:
                out.write(f"[ПРОПУЩЕН — больше {max_file_size_mb} МБ]\n")
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    out.write(f.read())
            except UnicodeDecodeError:
                try:
                    with open(file_path, 'r', encoding='cp1251') as f:
                        out.write(f.read())
                except Exception:
                    out.write("[бинарный файл — пропущен]\n")
            except Exception as e:
                out.write(f"[ОШИБКА ЧТЕНИЯ: {e}]\n")

            out.write("\n")

    print(f"✅ Дамп собран: {len(all_files)} файлов -> {output}")


# ================== ЗАПУСК ==================

if __name__ == "__main__":
    SOURCE = Path(__file__).resolve().parent
    DEST   = SOURCE.parent / ("_COPY")
    OUTPUT_TXT = DEST / "ALL_IN_ONE.txt"

    print("=" * 60)
    print(f"Источник:        {SOURCE}")
    print(f"Копия (.txt):    {DEST}")
    print(f"Общий дамп:      {OUTPUT_TXT}")
    print("=" * 60)

    # 1) делаем копию, где все файлы = .txt
    copy_folder_as_txt(SOURCE, DEST, new_ext=".txt")

    # 2) из этой копии собираем всё в один большой txt
    collect_txt_to_one(str(DEST), str(OUTPUT_TXT), max_file_size_mb=5.0)