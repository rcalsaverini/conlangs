import click 
import questionary as q
from pathlib import Path
from dataclasses import dataclass

BASE_DIRECTORY = Path("./languages/")
APRIORI_DIR = BASE_DIRECTORY / "apriori"
APOSTERIORI_DIR = BASE_DIRECTORY / "aposteriori"
SUBDIRECTORY_STRUCTURE = {
    "resources": {
        "type": "directory",
        "contents": {
            "words.csv": {
                "type": "file",
                "contents": ""
            },
            "phoneme_inventory.csv": {
                "type": "file",
                "contents": ""
            },
        }
    },
    "reference": {
        "type": "directory",
        "contents": {
            "main.md": {
                "type": "file",
                "contents": lambda language_name : (
                    f"# {language_name}"
                    f"\n"
                    f"This is the main reference document for *{language_name}*. For more information"
                    f"about the language, see the other files in this directory:\n"
                    f"- `proto_language.md`: a description of the proto-language from which *{language_name}* is descended\n"
                    f"- `evolution.md`: a description of the evolution of *{language_name}* from its proto-language\n"
                    f"- `phonology.md`: a description of the phonology of *{language_name}*\n"
                    f"- `grammar.md`: a description of the grammar of *{language_name}*\n"
                    f"- `lexicon.md`: a description of the lexicon of *{language_name}*\n"
                )
            },
            "proto_language.md": {
                "type": "file",
                "contents": ""
            },
            "evolution.md": {
                "type": "file",
                "contents": ""
            },
            "phonology.md": {
                "type": "file",
                "contents": ""
            },
            "grammar.md": {
                "type": "file",
                "contents": ""
            },
            "lexicon.md": {
                "type": "file",
                "contents": ""
            },
        }
    },
    "scripts": {
        "type": "directory",
        "contents": {
            "tests": {
                "type": "directory",
                "contents": {}
            },
            "analysis": {
                "type": "directory",
                "contents": {}
            },
            "generation": {
                "type": "directory",
                "contents": {}
            },
            "processing": {
                "type": "directory",
                "contents": {}
            },
            "evolution": {
                "type": "directory",
                "contents": {
                    "lexurgy_rules.lsc": {
                        "type": "file",
                        "contents": ""
                    },
                }
            },
            "doc_builder.py": {
                "type": "file",
                "contents": ""
            },
        }
    },
    "main.py": {
        "type": "file",
        "contents": ""
    }
}

def create_subdirectory_structure(root: Path, name: str, structure: dict):
    for directory_name, directory_contents in structure.items():
        directory_path = root / directory_name
        if directory_contents["type"] == "directory":
            click.echo(f"Creating directory {directory_path}...")
            directory_path.mkdir(parents=True, exist_ok=True)
            create_subdirectory_structure(directory_path, name, directory_contents["contents"])
        elif directory_contents["type"] == "file":
            click.echo(f"Creating file {directory_path}...")
            with open(directory_path, "w") as f:
                if callable(directory_contents["contents"]):
                    f.write(directory_contents["contents"](name))
                else:
                    f.write(directory_contents["contents"])

@dataclass
class Conlang:
    name: str

    @property
    def slug(self):
        return self.name.lower().replace(" ", "_")

    def create(self):
        pass

@dataclass
class APrioriConlang(Conlang):
    type: str = "a priori"
    is_vulgarlang_based: bool = False

    @property
    def directory(self):
        base_path = APRIORI_DIR if not self.is_vulgarlang_based else APRIORI_DIR / "vulgarlang"
        return base_path / self.slug

    def create(self):
        super().create()
        click.echo("Creating a priori conlang...")
        click.echo(f"Creating {self.directory}...")
        self.directory.mkdir(parents=True, exist_ok=True)
        create_subdirectory_structure(self.directory, self.name, SUBDIRECTORY_STRUCTURE)


@dataclass
class APosterioriConlang(Conlang):
    type: str = "a posteriori"
    root_family: str = None
    branch: str = None


@click.command()
def create():
    """
    Create a new conlang project with standard directories and files.
    
    ├── <language>/
    │   ├── resources/                    # files with computer-friendly resources for the language
    │   │   ├── words.csv
    │   │   ├── phoneme_inventory.csv
    │   ├── reference/                    # files with the reference grammar, lexicon, and phonology
    │   │   ├── main.md
    │   │   ├── proto_language.md
    │   │   ├── evolution.md
    │   │   ├── phonology.md
    │   │   ├── grammar.md
    │   │   ├── lexicon.md
    │   ├── scripts/
    │   │   ├── doc_builder.py
    │   │   ├── analysis/
    │   │   ├── generation/
    │   │   ├── processing/
    │   │   ├── evolution/
    │   │   │   ├── lexurgy_rules.lsc
    │   │    ├── tests/
    │   ├── <language>.py                # main file for language commands
    """
    language_name = q.text("What is the name of your conlang?").ask()
    language_type = q.select("What type of conlang is it?", choices=["a priori", "a posteriori"]).ask()

    if language_type == "a priori":
        is_vulgarlang_based = q.confirm("Is your conlang based on Vulgarlang?").ask()
        conlang = APrioriConlang(name=language_name, is_vulgarlang_based=is_vulgarlang_based)
    
    elif language_type == "a posteriori":
        root_family = q.text("What is the root family of your conlang?").ask()
        branch = q.text("What is the branch of your conlang?").ask()
        conlang = APosterioriConlang(name=language_name, root_family=root_family, branch=branch)

    conlang.create()