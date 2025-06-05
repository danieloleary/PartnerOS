## [Unreleased]

## [2024-06-10]
- Implemented YAML frontmatter metadata in all template files
- Added cross-referencing "Related Templates" sections to all templates
- Added "How to Use This Template" instructions to all templates

## [2024-06-11]
### Added
- Web application for browsing the blueprint documents (`webapp/` directory).
- Document loading and display from markdown files.
- Sidebar with document list.
- Basic search functionality using Lunr.js.
- Document grouping into sections in the sidebar.
- PartnerOS logo.
- Welcome screen.

### Improved
- Enhanced markdown rendering with `marked`, `highlight.js`, and `DOMPurify`.
- Fixed file path handling for correct document loading (both initial and on link clicks).
- Refined overall styling of the web application (layout, typography, colors, spacing, code blocks, tables, blockquotes, links, search results).
- Added detailed console logging for debugging document loading and rendering.
- Added a basic file loading test script (`webapp/test.js`).

### Fixed
- Resolved 404 errors related to incorrect file paths.
- Corrected sidebar links and internal document links.
- Fixed issue with frontmatter displaying in document content.
- Adjusted search bar size.
- Ensured documents are correctly grouped into sections in the sidebar. 