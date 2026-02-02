# Quick Start Guide

## Setting Up Your Ontology Repository

### 1. Create Your GitHub Repository

```bash
# Create a new repository on GitHub, then clone it
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME

# Copy the repository structure files
cp -r ontology-repo-setup/.github .
cp -r ontology-repo-setup/ontology .
cp -r ontology-repo-setup/docs .
cp ontology-repo-setup/.gitignore .
cp ontology-repo-setup/README.md .
```

### 2. Configure GitHub Actions Permissions

Before the workflow can commit documentation, you need to enable write permissions:

1. Go to your repository on GitHub
2. Click **Settings** → **Actions** → **General**
3. Under **Workflow permissions**, select:
   - ✅ **Read and write permissions**
   - ✅ **Allow GitHub Actions to create and approve pull requests**
4. Click **Save**

### 3. Add Your Ontology

Replace the example ontology with your own:

```bash
# Remove example ontology
rm ontology/example.ttl

# Add your ontology file(s)
cp /path/to/your/ontology.owl ontology/
# or
cp /path/to/your/ontology.ttl ontology/
# or
cp /path/to/your/ontology.rdf ontology/
```

### 4. Push and Watch the Magic

```bash
git add .
git commit -m "Initial commit with ontology"
git push origin main
```

Go to the **Actions** tab in your GitHub repository to watch the documentation generation process.

### 5. Enable GitHub Pages (Optional but Recommended)

To make your documentation publicly accessible:

1. Go to **Settings** → **Pages**
2. Under **Source**, select:
   - Branch: `main` (or `master`)
   - Folder: `/docs`
3. Click **Save**

Your documentation will be available at:
```
https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/
```

## Updating Your Ontology

Simply edit your ontology file and push:

```bash
# Edit your ontology
vim ontology/your-ontology.owl

# Commit and push
git add ontology/
git commit -m "Update ontology: added new classes"
git push
```

The documentation will be automatically regenerated!

## Troubleshooting

### Workflow fails with "Permission denied"
- Check that you've enabled **Read and write permissions** in Settings → Actions → General

### Documentation not updating
- Check the **Actions** tab for error messages
- Ensure your ontology file is valid (test it with Protégé or an RDF validator)
- Make sure the file is in the `ontology/` directory

### GitHub Pages shows 404
- Wait 2-3 minutes after enabling GitHub Pages
- Check that the `docs/` directory contains generated files
- Verify the GitHub Pages source is set to `/docs` folder

## Advanced Configuration

### Custom WIDOCO Configuration File

You can create a `widoco.properties` file for more control:

```properties
ontologyTitle=My Ontology
ontologyPrefix=mo
ontologyNamespaceURI=http://example.org/myontology#
ontologyName=My Ontology
thisVersionURI=http://example.org/myontology/1.0.0
latestVersionURI=http://example.org/myontology/
previousVersionURI=http://example.org/myontology/0.9.0
dateOfRelease=2025-02-02
authors=Your Name;Another Author
authorsURI=http://example.org/person1;http://example.org/person2
authorsInstitution=Your Institution
```

Then update the workflow to use it:

```yaml
java -jar widoco.jar \
  -ontFile "$ontology_file" \
  -confFile widoco.properties \
  -outFolder docs/$base_name \
  -rewriteAll
```

### Process Multiple Ontologies Differently

If you have multiple ontologies that need different settings, you can modify the workflow to handle them individually:

```yaml
- name: Generate documentation for main ontology
  run: |
    java -jar widoco.jar \
      -ontFile ontology/main.owl \
      -outFolder docs/main \
      -rewriteAll \
      -includeImportedOntologies

- name: Generate documentation for secondary ontology
  run: |
    java -jar widoco.jar \
      -ontFile ontology/secondary.owl \
      -outFolder docs/secondary \
      -rewriteAll
```

## Getting Help

- [WIDOCO Documentation](https://github.com/dgarijo/Widoco)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [OWL 2 Web Ontology Language Primer](https://www.w3.org/TR/owl2-primer/)
