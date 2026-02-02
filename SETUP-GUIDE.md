# Ontology GitHub Repository Setup - Complete Package

This package contains everything you need to set up a GitHub repository that automatically generates ontology documentation using WIDOCO.

## What's Included

### 1. GitHub Actions Workflow (`.github/workflows/generate-docs.yml`)
- Automatically triggers on push to main/master branch when ontology files change
- Downloads WIDOCO (latest version 1.4.25)
- Generates documentation for all `.owl`, `.ttl`, and `.rdf` files in the `ontology/` directory
- Commits and pushes the generated documentation back to the repository
- Can also be triggered manually from the Actions tab

### 2. Example Ontology (`ontology/example.ttl`)
- A complete example ontology in Turtle format
- Demonstrates classes, properties, and proper annotations
- Can be used for testing the workflow before adding your own ontology
- Replace with your actual ontology files

### 3. Documentation Directory (`docs/`)
- Placeholder directory for generated documentation
- Will be populated automatically by the workflow
- Can be used with GitHub Pages for hosting documentation online

### 4. Configuration Files
- `.gitignore`: Excludes temporary files and WIDOCO jar files
- `README.md`: Comprehensive documentation for repository users
- `QUICKSTART.md`: Step-by-step setup instructions

## Installation Steps

### Option 1: Start Fresh with This Structure

```bash
# 1. Create a new GitHub repository (on GitHub.com)

# 2. Clone your new repository
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME

# 3. Copy these files into your repository
cp -r /path/to/ontology-github-setup/.github .
cp -r /path/to/ontology-github-setup/ontology .
cp -r /path/to/ontology-github-setup/docs .
cp /path/to/ontology-github-setup/.gitignore .
cp /path/to/ontology-github-setup/README.md .
cp /path/to/ontology-github-setup/QUICKSTART.md .

# 4. Add your ontology files
rm ontology/example.ttl  # Remove example
cp /path/to/your/ontology.owl ontology/

# 5. Commit and push
git add .
git commit -m "Initial setup with automated WIDOCO documentation"
git push origin main
```

### Option 2: Add to Existing Repository

```bash
# In your existing repository
cd your-existing-repo

# Copy workflow
mkdir -p .github/workflows
cp /path/to/ontology-github-setup/.github/workflows/generate-docs.yml .github/workflows/

# Create docs directory if it doesn't exist
mkdir -p docs

# Update .gitignore
cat /path/to/ontology-github-setup/.gitignore >> .gitignore

# Commit
git add .
git commit -m "Add automated WIDOCO documentation workflow"
git push
```

## Critical Configuration Steps

### 1. Enable GitHub Actions Write Permissions

**This is REQUIRED for the workflow to work!**

1. Go to your repository on GitHub
2. Navigate to: **Settings** → **Actions** → **General**
3. Scroll to **Workflow permissions**
4. Select: **Read and write permissions**
5. Check: **Allow GitHub Actions to create and approve pull requests**
6. Click **Save**

Without this, the workflow cannot commit the generated documentation.

### 2. Enable GitHub Pages (Optional)

To host your documentation online:

1. Go to: **Settings** → **Pages**
2. Under **Source**:
   - Branch: `main` (or `master`)
   - Folder: `/docs`
3. Click **Save**

Your documentation will be available at:
```
https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/
```

## How It Works

1. **Detection**: The workflow monitors the `ontology/` directory for changes to `.owl`, `.ttl`, or `.rdf` files

2. **Trigger**: When you push changes to these files, the workflow automatically starts

3. **Generation**: 
   - Downloads WIDOCO jar file
   - Runs WIDOCO on each ontology file
   - Generates comprehensive HTML documentation with:
     - Class and property hierarchies
     - Detailed descriptions
     - Visual diagrams (WebVOWL)
     - Cross-references
     - Namespace declarations

4. **Commit**: The generated documentation is committed back to the `docs/` directory

5. **Deploy**: If GitHub Pages is enabled, the documentation is automatically deployed

## Workflow Features

The workflow includes these WIDOCO options:

- **`-rewriteAll`**: Always regenerates all documentation (ensures consistency)
- **`-includeImportedOntologies`**: Includes documentation for imported ontologies
- **`-htaccess`**: Generates proper content negotiation files
- **`-webVowl`**: Includes WebVOWL interactive visualization
- **`-licensius`**: Adds license information section
- **`-ignoreIndividuals`**: Skips individual instances (can be removed if you need them)

## Customization Examples

### Change WIDOCO Version

In `.github/workflows/generate-docs.yml`, update the download URL:

```yaml
- name: Download WIDOCO
  run: |
    wget https://github.com/dgarijo/Widoco/releases/download/v1.4.26/widoco-1.4.26-jar-with-dependencies.jar -O widoco.jar
```

### Add Custom WIDOCO Parameters

Modify the `java -jar widoco.jar` command:

```yaml
java -jar widoco.jar \
  -ontFile "$ontology_file" \
  -outFolder docs/$base_name \
  -rewriteAll \
  -lang en-es \  # Add multiple languages
  -includeAnnotationProperties \
  -analytics UA-XXXXXXXX  # Add Google Analytics
```

### Process Only Specific Ontology Files

Replace the loop with specific files:

```yaml
- name: Generate documentation
  run: |
    java -jar widoco.jar \
      -ontFile ontology/main-ontology.owl \
      -outFolder docs/ \
      -rewriteAll
```

### Trigger on Pull Requests

Add PR trigger to the workflow:

```yaml
on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]
    paths:
      - 'ontology/**/*.owl'
```

## Testing the Setup

1. **First Test**: Push the example ontology to trigger the workflow
   ```bash
   git add ontology/example.ttl
   git commit -m "Test WIDOCO workflow"
   git push
   ```

2. **Monitor**: Go to the **Actions** tab on GitHub and watch the workflow run

3. **Verify**: Check that the `docs/` directory is populated with HTML files

4. **View**: If GitHub Pages is enabled, visit your documentation URL

## Troubleshooting

### "Permission denied" or "failed to push"
- **Solution**: Enable write permissions in Settings → Actions → General

### Workflow doesn't trigger
- **Check**: Are your files in `ontology/` with correct extensions (.owl, .ttl, .rdf)?
- **Check**: Did you push to main/master branch?
- **Check**: Is GitHub Actions enabled for your repository?

### WIDOCO fails with errors
- **Check**: Is your ontology file valid? Test it in Protégé
- **Check**: Are all namespace URIs accessible?
- **Try**: Remove some WIDOCO options to identify the issue

### Documentation generates but looks wrong
- **Check**: Ensure your ontology has proper metadata (dc:title, dc:description, etc.)
- **Try**: Add a WIDOCO configuration file for more control

### GitHub Pages shows 404
- **Wait**: Give it 2-3 minutes after first generation
- **Check**: Settings → Pages is pointing to `/docs` folder
- **Check**: `docs/` directory contains `index.html` or similar

## File Structure After Setup

```
your-repo/
├── .github/
│   └── workflows/
│       └── generate-docs.yml      # Workflow automation
├── ontology/
│   ├── your-ontology.owl          # Your ontology files
│   └── another-ontology.ttl       # Can have multiple
├── docs/
│   ├── your-ontology/
│   │   ├── index.html             # Main documentation page
│   │   ├── sections/              # Detailed sections
│   │   ├── resources/             # CSS, JS, images
│   │   └── webvowl/               # Interactive visualization
│   └── another-ontology/
│       └── ...
├── .gitignore
├── README.md
└── QUICKSTART.md
```

## Best Practices

1. **Use semantic versioning** in your ontology metadata
2. **Add meaningful annotations** (labels, comments) to all classes and properties
3. **Include license information** in your ontology
4. **Test changes locally** before pushing (if possible)
5. **Keep ontology files small** for faster documentation generation
6. **Use descriptive commit messages** when updating ontologies

## Additional Resources

- [WIDOCO GitHub Repository](https://github.com/dgarijo/Widoco)
- [WIDOCO Documentation](https://github.com/dgarijo/Widoco/wiki)
- [OWL 2 Primer](https://www.w3.org/TR/owl2-primer/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)

## Support

If you encounter issues:

1. Check the **Actions** tab for detailed error logs
2. Review WIDOCO's GitHub issues for similar problems
3. Validate your ontology syntax
4. Ensure all prerequisites are met (permissions, file locations)

## License

This setup template is provided as-is for use with your ontology projects. Modify as needed for your requirements.
