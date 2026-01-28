# CLAWED.md - Instructions for AI Assistants

## Changelog Fragments (MANDATORY)

Whenever you make changes to this codebase, you **MUST** create a towncrier news fragment. This applies to:

- New features
- Bug fixes
- Documentation changes
- Deprecations or removals
- Any other notable changes

### Creating a Fragment

Create a file in `changelog.d/` with the format `<identifier>.<type>`:

```bash
# For changes tied to a GitHub issue:
echo "Description of the change" > changelog.d/<issue-number>.<type>

# For changes without an issue (use + prefix):
echo "Description of the change" > changelog.d/+<short-description>.<type>
```

### Fragment Types

| Type | Suffix | Use for |
|------|--------|---------|
| Feature | `.feature` | New functionality |
| Bug fix | `.bugfix` | Bug fixes |
| Documentation | `.doc` | Documentation improvements |
| Removal | `.removal` | Deprecations and removals |
| Miscellaneous | `.misc` | Other changes (content hidden in changelog) |

### Examples

```bash
# New feature for issue #42
echo "Added support for sparse distance matrices" > changelog.d/42.feature

# Bug fix without an issue
echo "Fixed overflow in large matrix calculations" > changelog.d/+overflow-fix.bugfix

# Documentation update
echo "Improved installation instructions" > changelog.d/+install-docs.doc
```

### Guidelines

1. **One fragment per logical change** - Don't combine unrelated changes
2. **Write for users** - Describe what changed from the user's perspective
3. **Be concise** - One or two sentences is usually sufficient
4. **Use past tense** - "Added...", "Fixed...", "Removed..."

### Previewing the Changelog

To see how your fragments will appear in the changelog:

```bash
uv run towncrier build --draft --version 0.0.0
```
