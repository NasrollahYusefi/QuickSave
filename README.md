<div align="center">
    <img src="https://i.imgur.com/NcSTdBc.jpg" alt="QuickSave Banner" style="width: auto; height: auto; max-height: 300px;">
</div>

# QuickSave

![Python Version](https://img.shields.io/pypi/pyversions/qsave)
![PyPI Version](https://img.shields.io/pypi/v/qsave)
![License](https://img.shields.io/pypi/l/qsave)
![Total Downloads](https://static.pepy.tech/badge/qsave)

QuickSave is a fast, memory-efficient, and lightweight key-value database designed for use in small applications. It operates as a pure Python solution, offering a dictionary-like interface for easy integration. QuickSave works efficiently without dependencies, but if you want to boost its performance even further, you can install `msgspec`, which significantly enhances its speed.

---

### [Documentation](https://nasrollahyusefi.github.io/QuickSave/)
## 📖 Table of Contents
- [Why QuickSave?](#why-quicksave)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Examples](#examples)
- [License](#license)

---

## Why QuickSave?

QuickSave stands out for its speed, memory efficiency, and simplicity. Here are some of the key reasons you should consider using it:

- 🚀 **High Performance**: QuickSave is designed to be fast, with minimal overhead.
- 💡 **Low Memory Usage**: The library is optimized for memory efficiency, making it a great choice for projects with limited resources.
- 🧵 **Thread-Safe**: It supports thread-safe operations, ensuring that it works reliably in concurrent environments.
- 🔀 **Both sync and async support**: You can use either sync or async version of QuickSave.
- 🏎️ **Boosted Performance with `msgspec`**: By installing the optional `msgspec` library, you can further enhance QuickSave's performance, especially when handling complex data types.
- 🔧 **No Dependencies**: QuickSave is a pure Python library, which means it has no external dependencies, making it easy to install and use in any Python project.

---

## Installation
Install QuickSave using pip:
```bash
pip install --upgrade qsave
```

Optionally, install `msgspec` to boost performance:
```bash
pip install msgspec==0.19.0
```

If you want use async version of QuickSave:
```bash
pip install qsave[async]
```

## Getting Started

To start using QuickSave, import it and initialize your database:
```python
from qsave import QuickSave

db = QuickSave(path="path/to/your/file.json", pretty=True)
```
The pretty argument beautifies the saved data for better readability (optional).

---

## Examples

#### Basic Usage
By default, changes are automatically saved when the `with` block ends:
```python
with db.session() as session:
    session["key"] = "value"
    print(session.get("key"))  # Output: None, not yet saved

# Exiting the block automatically commits changes
with db.session() as session:
    print(session.get("key"))  # Output: value
```

#### Manual Commit (commit_on_expire=False)
For full control over when changes are saved, use commit_on_expire=False:
```python
with db.session(commit_on_expire=False) as session:
    session["key"] = "manual_value"
    print(session.get("key"))  # Output: None, not yet saved
    session.commit()  # Now changes are saved
    print(session.get("key"))  # Output: manual_value

with db.session() as session:
    print(session.get("key"))  # Output: manual_value
```

#### Commit and Rollback
You can manually save or discard changes during a session:
```python
with db.session() as session:
    session["key"] = "temp_value"
    session.rollback()  # Discard changes
    print(session.get("key"))  # Output: None
```

#### Nested Data
```python
with db.session() as session:
    session["nested"] = {"key": [1, 2, 3]}
    session.commit()

with db.session() as session:
    print(session["nested"])  # Output: {"key": [1, 2, 3]}
```

#### Async version:
```python
from qsave.asyncio import AsyncQuickSave

db = AsyncQuickSave("path/to/your/file.json")

async def main():
    async with db.session(False) as session:
        print(len(session))
        await session.commit()
        await session.rollback()  # NOTE: after commit, rollback does nothing :(
        # only commit and rollback need to be awaited
        # other functionalities remain the same as sync version
```

---

## License
This repository is licensed under [MIT License](https://qsave.github.com/).
