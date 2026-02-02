#!/usr/bin/env python3
"""
Local WIDOCO Documentation Generator
Simulates the GitHub Actions workflow for testing purposes
"""

import os
import subprocess
import sys
from pathlib import Path
import urllib.request

# Configuration
WIDOCO_VERSION = "1.4.25"
WIDOCO_JAR_URL = f"https://github.com/dgarijo/Widoco/releases/download/v{WIDOCO_VERSION}/widoco-{WIDOCO_VERSION}-jar-with-dependencies_JDK-17.jar"
WIDOCO_JAR_NAME = "widoco.jar"
ONTOLOGY_DIR = "ontology"
DOCS_DIR = "docs"

# WIDOCO options
WIDOCO_OPTIONS = [
    "-rewriteAll",
    "-includeImportedOntologies",
    "-webVowl",
    "-licensius"
]


def download_widoco():
    """Download WIDOCO jar if not already present"""
    if os.path.exists(WIDOCO_JAR_NAME):
        print(f"✓ WIDOCO jar already exists: {WIDOCO_JAR_NAME}")
        return True
    
    print(f"Downloading WIDOCO from {WIDOCO_JAR_URL}...")
    try:
        urllib.request.urlretrieve(WIDOCO_JAR_URL, WIDOCO_JAR_NAME)
        print(f"✓ Downloaded WIDOCO to {WIDOCO_JAR_NAME}")
        return True
    except Exception as e:
        print(f"✗ Failed to download WIDOCO: {e}")
        return False


def check_java():
    """Check if Java 17+ is installed"""
    try:
        result = subprocess.run(
            ["java", "-version"],
            capture_output=True,
            text=True
        )
        version_output = result.stderr  # Java outputs version to stderr
        print(f"✓ Java is installed")
        print(f"  {version_output.split(chr(10))[0]}")
        return True
    except FileNotFoundError:
        print("✗ Java is not installed or not in PATH")
        print("  Please install Java 17 or higher")
        return False


def find_ontology_files():
    """Find all ontology files in the ontology directory"""
    ontology_path = Path(ONTOLOGY_DIR)
    
    if not ontology_path.exists():
        print(f"✗ Ontology directory not found: {ONTOLOGY_DIR}")
        return []
    
    extensions = ['*.owl', '*.ttl', '*.rdf']
    ontology_files = []
    
    for ext in extensions:
        ontology_files.extend(ontology_path.rglob(ext))
    
    return sorted(ontology_files)


def generate_documentation(ontology_file):
    """Generate documentation for a single ontology file"""
    print(f"\nProcessing: {ontology_file}")
    
    # Extract relative path from ontology/
    relative_path = ontology_file.relative_to(ONTOLOGY_DIR)
    
    # Get directory path (module/version)
    dir_path = relative_path.parent
    
    # Get filename without extension
    base_name = ontology_file.stem
    
    # Create output directory
    output_dir = Path(DOCS_DIR) / dir_path
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"  Module/Version: {dir_path}")
    print(f"  Ontology name: {base_name}")
    print(f"  Output directory: {output_dir}")
    
    # Build WIDOCO command
    cmd = [
        "java", "-jar", WIDOCO_JAR_NAME,
        "-ontFile", str(ontology_file),
        "-outFolder", str(output_dir)
    ] + WIDOCO_OPTIONS
    
    print(f"  Running WIDOCO...")
    
    try:
        # Run WIDOCO
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print(f"  ✓ Documentation generated successfully")
            
            # Rename index-en.html to index.html
            index_en = output_dir / "index-en.html"
            index_html = output_dir / "index.html"
            
            if index_en.exists():
                index_en.rename(index_html)
                print(f"  ✓ Renamed index-en.html to index.html")
            
            return True
        else:
            print(f"  ✗ WIDOCO failed with return code {result.returncode}")
            if result.stderr:
                print(f"  Error output: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"  ✗ WIDOCO timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"  ✗ Error running WIDOCO: {e}")
        return False


def main():
    """Main execution function"""
    print("=" * 60)
    print("Local WIDOCO Documentation Generator")
    print("=" * 60)
    
    # Check prerequisites
    print("\n1. Checking prerequisites...")
    if not check_java():
        sys.exit(1)
    
    # Download WIDOCO
    print("\n2. Setting up WIDOCO...")
    if not download_widoco():
        sys.exit(1)
    
    # Find ontology files
    print(f"\n3. Finding ontology files in '{ONTOLOGY_DIR}/'...")
    ontology_files = find_ontology_files()
    
    if not ontology_files:
        print(f"✗ No ontology files found in '{ONTOLOGY_DIR}/'")
        print(f"  Please add .owl, .ttl, or .rdf files to the '{ONTOLOGY_DIR}/' directory")
        print(f"  Expected structure: {ONTOLOGY_DIR}/module/version/ontology.owl")
        sys.exit(1)
    
    print(f"✓ Found {len(ontology_files)} ontology file(s):")
    for f in ontology_files:
        print(f"  - {f}")
    
    # Generate documentation
    print(f"\n4. Generating documentation...")
    print("-" * 60)
    
    success_count = 0
    fail_count = 0
    
    for ontology_file in ontology_files:
        if generate_documentation(ontology_file):
            success_count += 1
        else:
            fail_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Total files processed: {len(ontology_files)}")
    print(f"✓ Successful: {success_count}")
    print(f"✗ Failed: {fail_count}")
    
    if success_count > 0:
        print(f"\n📁 Documentation generated in '{DOCS_DIR}/' directory")
        print(f"\nTo view the documentation:")
        print(f"  1. Navigate to the docs folder")
        print(f"  2. Open index.html files in your browser")
        print(f"\nExample:")
        # Find first generated index.html
        docs_path = Path(DOCS_DIR)
        index_files = list(docs_path.rglob("index.html"))
        if index_files:
            print(f"  open {index_files[0]}")
    
    if fail_count > 0:
        print(f"\n⚠️  Some documentation generation failed. Check the output above.")
        sys.exit(1)
    
    print("\n✓ All documentation generated successfully!")


if __name__ == "__main__":
    main()