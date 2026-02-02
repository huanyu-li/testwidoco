# Ontology Repository with Automated Documentation

This repository hosts ontology files and automatically generates documentation using [WIDOCO](https://github.com/dgarijo/Widoco) whenever ontology files are updated.

## Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── generate-docs.yml         # GitHub Actions workflow
├── ontology/                          # Ontology files organized by module/version
│   ├── module1/
│   │   ├── 0.1/
│   │   │   └── ontology.owl
│   │   └── 0.2/
│   │       └── ontology.owl
│   └── module2/
│       └── 1.0/
│           └── ontology.ttl
├── docs/                              # Generated documentation (auto-generated)
│   ├── module1/
│   │   ├── 0.1/
│   │   │   └── index.html
│   │   └── 0.2/
│   │       └── index.html
│   └── module2/
│       └── 1.0/
│           └── index.html
├── generate_docs_local.py             # Local testing script
└── README.md                          # This file
```

### Folder Organization

Ontology files should be organized as: `ontology/{module}/{version}/{ontology-file}.{owl|ttl|rdf}`

This structure:
- Keeps different modules separated
- Maintains version history
- Generates documentation at: `docs/{module}/{version}/index.html`
- Creates clean URLs on GitHub Pages: `https://username.github.io/repo/module/version/`

## How It Works

1. **Add or update ontology files**: Place your ontology files (`.owl`, `.ttl`, or `.rdf`) in the `ontology/{module}/{version}/` directory structure
2. **Push to GitHub**: Commit and push your changes to the `main` or `master` branch
3. **Automatic documentation generation**: The GitHub Actions workflow will:
   - Detect changes to ontology files
   - Download WIDOCO (JDK-17 version)
   - Generate comprehensive documentation for each ontology
   - Maintain the module/version folder structure
   - Rename `index-en.html` to `index.html`
   - Commit and push the generated documentation to the `docs/` directory

Your documentation will be available at: `https://[username].github.io/[repo]/[module]/[version]/index.html`

## Setup Instructions

### 1. Initial Repository Setup

1. Create a new GitHub repository
2. Clone this repository structure to your local machine
3. Add your ontology files to the `ontology/` directory

### 2. Configure GitHub Actions Permissions

To allow the workflow to commit generated documentation:

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Actions** → **General**
3. Scroll down to **Workflow permissions**
4. Select **Read and write permissions**
5. Check **Allow GitHub Actions to create and approve pull requests**
6. Click **Save**

### 3. Enable GitHub Pages (Optional)

To host your documentation online:

1. Go to **Settings** → **Pages**
2. Under **Source**, select **Deploy from a branch**
3. Select the `main` or `master` branch and `/docs` folder
4. Click **Save**
5. Your documentation will be available at `https://[username].github.io/[repository-name]/`

## Local Testing

Before pushing to GitHub, you can test documentation generation locally using the provided Python script.

### Prerequisites

- Python 3.6+
- Java 17+ ([Download here](https://adoptium.net/))

### Usage

1. **Organize your ontology files** in the module/version structure:
   ```
   ontology/
   ├── module1/
   │   ├── 0.1/
   │   │   └── ontology.owl
   │   └── 0.2/
   │       └── ontology.owl
   └── module2/
       └── 1.0/
           └── ontology.ttl
   ```

2. **Run the test script**:
   ```bash
   python3 generate_docs_local.py
   ```

3. **View the documentation**:
   
   The script will offer to start a local web server automatically. Type `y` when prompted.
   
   Or manually start a server:
   ```bash
   cd docs
   python3 -m http.server 8000
   ```
   
   Then open in your browser: `http://localhost:8000/module/version/index.html`

### Important: CORS Restrictions

⚠️ **Do not open `index.html` files directly** (using `file://` protocol). WIDOCO documentation requires an HTTP server due to JavaScript cross-origin restrictions. Always use a web server for local viewing.

The local testing script:
- Downloads WIDOCO automatically
- Generates documentation with the same settings as GitHub Actions
- Maintains the module/version folder structure
- Renames `index-en.html` to `index.html`
- Offers to start a web server for immediate viewing

See `LOCAL-TESTING-README.md` and `VIEWING-DOCS-LOCALLY.md` for detailed instructions.

## Manual Trigger

You can also manually trigger the documentation generation:

1. Go to the **Actions** tab in your repository
2. Select **Generate Ontology Documentation**
3. Click **Run workflow**

## WIDOCO Configuration

The workflow uses the following WIDOCO options:

- `-rewriteAll`: Overwrites previous documentation
- `-webVowl`: Includes WebVOWL visualization
- `-licensius`: Adds license information

Note: The workflow generates documentation directly in `docs/{module}/{version}/` structure and automatically renames `index-en.html` to `index.html`.

## Customization

### Modify WIDOCO Parameters

Edit `.github/workflows/generate-docs.yml` and adjust the `java -jar widoco.jar` command parameters according to your needs. See [WIDOCO documentation](https://github.com/dgarijo/Widoco) for available options.

### Change Trigger Conditions

By default, the workflow triggers on:
- Push to `main` or `master` branch
- Changes to ontology files in the `ontology/` directory

You can modify the trigger conditions in the workflow file under the `on:` section.

### Use Different Ontology Formats

The workflow supports `.owl`, `.ttl`, and `.rdf` files by default. To add support for other formats, modify the file patterns in the workflow.

## Troubleshooting

### Documentation not generating

- Check the **Actions** tab for error logs
- Ensure GitHub Actions has write permissions
- Verify your ontology files are valid
- Check that files are in the correct directory

### Documentation not appearing on GitHub Pages

- Ensure GitHub Pages is configured to use the `/docs` folder
- Wait a few minutes for GitHub Pages to deploy
- Check that the `docs/` directory contains generated files

## Example Ontology

Here's a minimal example ontology you can use for testing:

```turtle
@prefix : <http://example.org/ontology#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<http://example.org/ontology> rdf:type owl:Ontology ;
    rdfs:label "Example Ontology" ;
    rdfs:comment "An example ontology for testing WIDOCO documentation generation" .

:ExampleClass rdf:type owl:Class ;
    rdfs:label "Example Class" ;
    rdfs:comment "An example class in the ontology" .
```

Save this in the proper structure:
```bash
mkdir -p ontology/example/0.1
# Save the above content as ontology/example/0.1/example.ttl
```

After pushing, documentation will be generated at `docs/example/0.1/index.html`

## Quick Start Example

```bash
# 1. Create module/version structure
mkdir -p ontology/mymodule/0.1

# 2. Add your ontology file
cp your-ontology.owl ontology/mymodule/0.1/

# 3. Test locally (optional)
python3 generate_docs_local.py

# 4. Commit and push
git add ontology/mymodule/
git commit -m "Add mymodule v0.1"
git push

# Documentation will be auto-generated at:
# https://[username].github.io/[repo]/mymodule/0.1/index.html
```

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]
