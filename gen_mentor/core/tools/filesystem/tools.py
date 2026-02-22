"""File system tools: read, write, edit, list.

These tools directly inherit from LangChain's BaseTool for seamless integration.
"""

from pathlib import Path
from typing import Optional, Type

from langchain.tools import BaseTool
from pydantic import BaseModel, Field


def _resolve_path(path: str, workspace: Optional[Path] = None, allowed_dir: Optional[Path] = None) -> Path:
    """Resolve path against workspace (if relative) and enforce directory restriction.

    Args:
        path: The path to resolve
        workspace: The workspace directory for relative paths
        allowed_dir: The directory to restrict access to

    Returns:
        Resolved Path object

    Raises:
        PermissionError: If path is outside allowed_dir
    """
    p = Path(path).expanduser()
    if not p.is_absolute() and workspace:
        p = workspace / p
    resolved = p.resolve()
    if allowed_dir and not str(resolved).startswith(str(allowed_dir.resolve())):
        raise PermissionError(f"Path {path} is outside allowed directory {allowed_dir}")
    return resolved


# Input schemas
class ReadFileInput(BaseModel):
    """Input schema for ReadFileTool."""
    path: str = Field(description="The file path to read (relative to workspace or absolute)")


class WriteFileInput(BaseModel):
    """Input schema for WriteFileTool."""
    path: str = Field(description="The file path to write to")
    content: str = Field(description="The content to write to the file")


class EditFileInput(BaseModel):
    """Input schema for EditFileTool."""
    path: str = Field(description="The file path to edit")
    old_text: str = Field(description="The exact text to find and replace")
    new_text: str = Field(description="The text to replace with")


class ListDirInput(BaseModel):
    """Input schema for ListDirTool."""
    path: str = Field(description="The directory path to list")


class CreateDirInput(BaseModel):
    """Input schema for CreateDirTool."""
    path: str = Field(description="The directory path to create")


class DeleteFileInput(BaseModel):
    """Input schema for DeleteFileTool."""
    path: str = Field(description="The file path to delete")


# Tools
class ReadFileTool(BaseTool):
    """Tool to read file contents."""

    name: str = "read_file"
    description: str = "Read the contents of a file at the given path. Returns the file content as text."
    args_schema: Type[BaseModel] = ReadFileInput

    workspace: Optional[Path] = None
    allowed_dir: Optional[Path] = None

    def _run(self, path: str) -> str:
        """Read file contents.

        Args:
            path: Path to the file to read

        Returns:
            File contents or error message
        """
        try:
            file_path = _resolve_path(path, self.workspace, self.allowed_dir)
            if not file_path.exists():
                return f"Error: File not found: {path}"
            if not file_path.is_file():
                return f"Error: Not a file: {path}"

            content = file_path.read_text(encoding="utf-8")
            return content
        except PermissionError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error reading file: {str(e)}"

    async def _arun(self, path: str) -> str:
        """Async version of _run."""
        return self._run(path)


class WriteFileTool(BaseTool):
    """Tool to write content to a file."""

    name: str = "write_file"
    description: str = "Write content to a file at the given path. Creates parent directories if needed. Overwrites existing files."
    args_schema: Type[BaseModel] = WriteFileInput

    workspace: Optional[Path] = None
    allowed_dir: Optional[Path] = None

    def _run(self, path: str, content: str) -> str:
        """Write content to file.

        Args:
            path: Path to the file to write
            content: Content to write to the file

        Returns:
            Success message or error message
        """
        try:
            file_path = _resolve_path(path, self.workspace, self.allowed_dir)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            return f"Successfully wrote {len(content)} characters to {file_path}"
        except PermissionError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error writing file: {str(e)}"

    async def _arun(self, path: str, content: str) -> str:
        """Async version of _run."""
        return self._run(path, content)


class EditFileTool(BaseTool):
    """Tool to edit a file by replacing text."""

    name: str = "edit_file"
    description: str = "Edit a file by replacing old_text with new_text. The old_text must exist exactly in the file. If text appears multiple times, provide more context to make it unique."
    args_schema: Type[BaseModel] = EditFileInput

    workspace: Optional[Path] = None
    allowed_dir: Optional[Path] = None

    def _run(self, path: str, old_text: str, new_text: str) -> str:
        """Edit file by replacing text.

        Args:
            path: Path to the file to edit
            old_text: Text to find and replace
            new_text: Text to replace with

        Returns:
            Success message or error message
        """
        try:
            file_path = _resolve_path(path, self.workspace, self.allowed_dir)
            if not file_path.exists():
                return f"Error: File not found: {path}"

            content = file_path.read_text(encoding="utf-8")

            if old_text not in content:
                return f"Error: old_text not found in file. Make sure it matches exactly."

            # Count occurrences
            count = content.count(old_text)
            if count > 1:
                return f"Warning: old_text appears {count} times. Please provide more context to make it unique."

            new_content = content.replace(old_text, new_text, 1)
            file_path.write_text(new_content, encoding="utf-8")

            return f"Successfully edited {file_path}"
        except PermissionError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error editing file: {str(e)}"

    async def _arun(self, path: str, old_text: str, new_text: str) -> str:
        """Async version of _run."""
        return self._run(path, old_text, new_text)


class ListDirTool(BaseTool):
    """Tool to list directory contents."""

    name: str = "list_dir"
    description: str = "List the contents of a directory. Shows files and subdirectories with indicators."
    args_schema: Type[BaseModel] = ListDirInput

    workspace: Optional[Path] = None
    allowed_dir: Optional[Path] = None

    def _run(self, path: str) -> str:
        """List directory contents.

        Args:
            path: Path to the directory to list

        Returns:
            Directory listing or error message
        """
        try:
            dir_path = _resolve_path(path, self.workspace, self.allowed_dir)
            if not dir_path.exists():
                return f"Error: Directory not found: {path}"
            if not dir_path.is_dir():
                return f"Error: Not a directory: {path}"

            items = []
            for item in sorted(dir_path.iterdir()):
                prefix = "📁 " if item.is_dir() else "📄 "
                items.append(f"{prefix}{item.name}")

            if not items:
                return f"Directory {path} is empty"

            return "\n".join(items)
        except PermissionError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error listing directory: {str(e)}"

    async def _arun(self, path: str) -> str:
        """Async version of _run."""
        return self._run(path)


class CreateDirTool(BaseTool):
    """Tool to create a directory."""

    name: str = "create_dir"
    description: str = "Create a directory. Creates parent directories if needed."
    args_schema: Type[BaseModel] = CreateDirInput

    workspace: Optional[Path] = None
    allowed_dir: Optional[Path] = None

    def _run(self, path: str) -> str:
        """Create directory.

        Args:
            path: Path to the directory to create

        Returns:
            Success message or error message
        """
        try:
            dir_path = _resolve_path(path, self.workspace, self.allowed_dir)
            dir_path.mkdir(parents=True, exist_ok=True)
            return f"Successfully created directory: {dir_path}"
        except PermissionError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error creating directory: {str(e)}"

    async def _arun(self, path: str) -> str:
        """Async version of _run."""
        return self._run(path)


class DeleteFileTool(BaseTool):
    """Tool to delete a file."""

    name: str = "delete_file"
    description: str = "Delete a file. Use with caution - this cannot be undone."
    args_schema: Type[BaseModel] = DeleteFileInput

    workspace: Optional[Path] = None
    allowed_dir: Optional[Path] = None

    def _run(self, path: str) -> str:
        """Delete file.

        Args:
            path: Path to the file to delete

        Returns:
            Success message or error message
        """
        try:
            file_path = _resolve_path(path, self.workspace, self.allowed_dir)
            if not file_path.exists():
                return f"Error: File not found: {path}"
            if not file_path.is_file():
                return f"Error: Not a file: {path}"

            file_path.unlink()
            return f"Successfully deleted file: {file_path}"
        except PermissionError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error deleting file: {str(e)}"

    async def _arun(self, path: str) -> str:
        """Async version of _run."""
        return self._run(path)
