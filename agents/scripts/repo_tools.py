import os
import json
import argparse
import fnmatch

# Configuration for "noise" reduction
EXCLUDE_DIRS = {'.git', 'node_modules', '__pycache__', 'venv', '.env', 'dist', 'build'}
TEXT_EXTENSIONS = {'.py', '.js', '.ts', '.go', '.c', '.cpp', '.java', '.md', '.txt', '.yaml', '.yml', '.json'}

class RepoAnalystTools:
    def __init__(self, root_dir="."):
        self.root_dir = root_dir
        self.build_index()

    def build_index(self):
        """Creates repo_manifest.json automatically on execution."""
        manifest = []
        # Exclude common noise
        exclude = {'.git', 'node_modules', '__pycache__', 'venv'}
        
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in exclude]
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.md', '.json')):
                    path = os.path.relpath(os.path.join(root, file), self.root_dir)
                    manifest.append({
                        "path": path,
                        "size_kb": round(os.path.getsize(os.path.join(root, file)) / 1024, 2)
                    })
        
        with open('repo_manifest.json', 'w') as f:
            json.dump(manifest, f, indent=2)
        return "Index updated."

    def get_context_safe_content(self, file_path, max_lines=100):
        """Requirement 2: Context management. Limits lines to prevent context blowing."""
        try:
            with open(os.path.join(self.root_dir, file_path), 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if len(lines) > max_lines:
                    return f"// [TRUNCATED] Showing first {max_lines} lines:\n" + "".join(lines[:max_lines])
                return "".join(lines)
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def search_symbols(self, query):
        """Requirement 3: Deterministic search (grep-like) instead of LLM guessing."""
        results = []
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for file in files:
                if any(file.endswith(ext) for ext in TEXT_EXTENSIONS):
                    path = os.path.join(root, file)
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        if query.lower() in f.read().lower():
                            results.append(os.path.relpath(path, self.root_dir))
        return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyst Agent CLI Tools")
    parser.add_argument("command", choices=["index", "read", "search"])
    parser.add_argument("--path", help="File path for 'read'")
    parser.add_argument("--query", help="Search term for 'search'")
    
    args = parser.parse_args()
    tools = RepoAnalystTools()

    if args.command == "index":
        print(tools.build_index())
    elif args.command == "read":
        print(tools.get_context_safe_content(args.path))
    elif args.command == "search":
        print(json.dumps(tools.search_symbols(args.query), indent=2)) 