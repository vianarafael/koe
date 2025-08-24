#!/usr/bin/env python3
import sys
import json
import jsonpatch

def main():
    if len(sys.argv) != 3:
        print("Usage: apply_patch.py <source_of_truth.json> <patch.json>")
        sys.exit(1)

    source_path = sys.argv[1]
    patch_path = sys.argv[2]

    try:
        with open(source_path, 'r') as f:
            source = json.load(f)
        with open(patch_path, 'r') as f:
            patch = json.load(f)

        patched = jsonpatch.apply_patch(source, patch)

        with open(source_path, 'w') as f:
            json.dump(patched, f, indent=2)

        print(f"Patch applied successfully to {source_path}")
    except (json.JSONDecodeError, jsonpatch.JsonPatchException) as e:
        print(f"Error applying patch: {e}")
        sys.exit(2)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(3)

if __name__ == "__main__":
    main()
