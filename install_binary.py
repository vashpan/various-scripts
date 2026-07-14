#!/usr/bin/env python3

# This script is installing executables from the web into the system
# 
# It checks if archive contains a single executable, and then copies it into /usr/local/bin
#

import os
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
import zipfile

from pathlib import Path, PurePosixPath
from typing import List, Optional, Tuple


DEFAULT_INSTALL_DIR = "/usr/local/bin"


def usage() -> None:
    print(f"Usage: {sys.argv[0]} [binary_name] URL", file=sys.stderr)


def parse_arguments() -> Tuple[Optional[str], str]:
    if len(sys.argv) == 2:
        return None, sys.argv[1]
    if len(sys.argv) == 3:
        binary_name = sys.argv[1]
        if binary_name in {"", ".", ".."} or Path(binary_name).name != binary_name:
            raise ValueError("binary name must be a filename, not a path")
        return binary_name, sys.argv[2]

    usage()
    raise SystemExit(1)


def download(url: str, destination: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "install_binary.py"})
    with urllib.request.urlopen(request) as response, destination.open("wb") as output:
        content_length = response.headers.get("Content-Length")
        try:
            total_size = int(content_length) if content_length else None
        except ValueError:
            total_size = None

        downloaded = 0
        last_percentage = -1
        status_width = len("Downloading: 0%")
        sys.stdout.write("Downloading: 0%")
        sys.stdout.flush()

        while True:
            chunk = response.read(64 * 1024)
            if not chunk:
                break
            output.write(chunk)
            downloaded += len(chunk)

            if total_size:
                percentage = min(100, downloaded * 100 // total_size)
                if percentage != last_percentage:
                    status = f"Downloading: {percentage}%"
                    sys.stdout.write(f"\r{status.ljust(status_width)}")
                    sys.stdout.flush()
                    status_width = max(status_width, len(status))
                    last_percentage = percentage
            else:
                status = f"Downloading: {downloaded:,} bytes"
                sys.stdout.write(f"\r{status.ljust(status_width)}")
                sys.stdout.flush()
                status_width = max(status_width, len(status))

        finished = "Downloading: 100% OK!"
        sys.stdout.write(f"\r{finished.ljust(status_width)}\n")
        sys.stdout.flush()


def validate_member_path(name: str) -> None:
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe path in archive: {name}")


def extract_archive(archive: Path, destination: Path) -> None:
    if zipfile.is_zipfile(archive):
        with zipfile.ZipFile(archive) as zip_archive:
            members = zip_archive.infolist()
            for member in members:
                validate_member_path(member.filename)
                mode = member.external_attr >> 16
                if stat.S_ISLNK(mode):
                    raise ValueError(f"symbolic links are not supported: {member.filename}")
            zip_archive.extractall(destination)
            for member in members:
                mode = member.external_attr >> 16
                permissions = stat.S_IMODE(mode)
                if member.create_system == 3 and permissions:
                    (destination / member.filename).chmod(permissions)
        return

    if tarfile.is_tarfile(archive):
        with tarfile.open(archive, "r:*") as tar_archive:
            for member in tar_archive.getmembers():
                validate_member_path(member.name)
                if member.issym() or member.islnk():
                    raise ValueError(f"links are not supported: {member.name}")
                if member.ischr() or member.isblk() or member.isfifo():
                    raise ValueError(f"special files are not supported: {member.name}")
            tar_archive.extractall(destination)
        return

    raise ValueError("the download is not a supported tar or ZIP archive")


def archive_files(directory: Path) -> List[Path]:
    return sorted(path for path in directory.rglob("*") if path.is_file())


def is_executable(path: Path) -> bool:
    return bool(path.stat().st_mode & 0o111)


def relative_names(files: List[Path], root: Path) -> List[str]:
    return [str(path.relative_to(root)) for path in files]


def ensure_install_directory(directory: Path) -> bool:
    if directory.is_dir() and os.access(directory, os.W_OK):
        return False

    if not directory.exists() and os.access(directory.parent, os.W_OK):
        directory.mkdir(parents=True)
        return False

    sudo = shutil.which("sudo")
    if sudo is None:
        raise PermissionError(f"cannot write to {directory} and sudo is unavailable")

    subprocess.run([sudo, "mkdir", "-p", str(directory)], check=True)
    return True


def install_single_file(source: Path, destination: Path) -> None:
    needs_sudo = ensure_install_directory(destination.parent)

    if needs_sudo:
        subprocess.run(
            ["sudo", "install", "-m", "0755", str(source), str(destination)],
            check=True,
        )
    else:
        shutil.copy2(source, destination)
        destination.chmod(0o755)


def copy_archive_contents(source: Path, destination: Path) -> None:
    needs_sudo = ensure_install_directory(destination)

    if needs_sudo:
        ditto = shutil.which("ditto")
        if ditto is None:
            raise RuntimeError("ditto is required for privileged directory installation")
        subprocess.run(["sudo", ditto, str(source), str(destination)], check=True)
    else:
        for item in source.iterdir():
            target = destination / item.name
            if item.is_dir():
                shutil.copytree(item, target, dirs_exist_ok=True)
            else:
                shutil.copy2(item, target)


def confirm_installation(files: List[Path], root: Path, destination: Path) -> bool:
    print(f"Archive contents: {', '.join(relative_names(files, root))}")
    try:
        reply = input(f"Proceed with installing to {destination}? [y/N] ")
    except EOFError:
        print()
        return False
    return reply.strip().lower() in {"y", "yes"}


def main() -> int:
    requested_name, url = parse_arguments()
    install_directory = Path(
        os.environ.get("BINARY_INSTALL_DIR", DEFAULT_INSTALL_DIR)
    ).expanduser()

    with tempfile.TemporaryDirectory(prefix="binary-install-") as temporary:
        temporary_path = Path(temporary)
        archive_path = temporary_path / "archive"
        extracted_path = temporary_path / "extracted"
        extracted_path.mkdir()

        print(f"Installing: {url}")
        download(url, archive_path)
        extract_archive(archive_path, extracted_path)

        files = archive_files(extracted_path)
        if not files:
            raise ValueError("the archive contains no files")

        executable_files = [path for path in files if is_executable(path)]
        if not executable_files:
            raise ValueError("the archive does not contain an executable file")

        if len(files) == 1:
            source = files[0]
            installed_name = requested_name or source.name
            installed_path = install_directory / installed_name
            print("Installing...")
            install_single_file(source, installed_path)
            print(f"Installed: {installed_path}")
            return 0

        if requested_name is not None:
            print("Note: binary_name is only applied to single-file archives.")

        if not confirm_installation(files, extracted_path, install_directory):
            print("Installation cancelled.")
            return 0

        installed_paths = [
            install_directory / path.relative_to(extracted_path)
            for path in executable_files
        ]
        print("Installing...")
        copy_archive_contents(extracted_path, install_directory)
        print(f"Installed: {', '.join(str(path) for path in installed_paths)}")
        return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInstallation cancelled.", file=sys.stderr)
        sys.exit(130)
