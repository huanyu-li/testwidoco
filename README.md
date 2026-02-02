# Ontology Repository with Automated Documentation

This repository hosts ontology files and automatically generates documentation using [WIDOCO](https://github.com/dgarijo/Widoco) whenever ontology files are updated.

## Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── generate-docs.yml    # GitHub Actions workflow for documentation generation
├── ontology/                     # Place your ontology files here (.owl, .ttl, .rdf)
├── docs/                         # Generated documentation (auto-generated, do not edit manually)
└── README.md                     # This file
```

## How It Works

1. **Add or update ontology files**: Place your ontology files (`.owl`, `.ttl`, or `.rdf`) in the `ontology/` directory
2. **Push to GitHub**: Commit and push your changes to the `main` or `master` branch
3. **Automatic documentation generation**: The GitHub Actions workflow will:
   - Detect changes to ontology files
   - Download WIDOCO
   - Generate comprehensive documentation for each ontology
   - Commit and push the generated documentation to the `docs/` directory

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

## Manual Trigger

You can also manually trigger the documentation generation:

1. Go to the **Actions** tab in your repository
2. Select **Generate Ontology Documentation**
3. Click **Run workflow**

## WIDOCO Configuration

The workflow uses the following WIDOCO options:

- `-rewriteAll`: Overwrites previous documentation
- `-includeImportedOntologies`: Includes imported ontologies in documentation
- `-htaccess`: Generates .htaccess file for proper content negotiation
- `-webVowl`: Includes WebVOWL visualization
- `-licensius`: Adds license information
- `-ignoreIndividuals`: Skips individual instances (can be removed if needed)

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

Save this as `ontology/example.ttl` and push to see the documentation generation in action.

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]
