# Open Source Definition reference feasibility

## Recommendation

Link to the canonical upstream definition from the repository presentation
guide. Keep the reference link-only and review upstream changes on demand.
The guide has a concrete use for the definition when reviewing whether public
README wording calls a project open source. It has no identified offline,
exact-version, or machine-readable dependency on the full text that would
justify a local copy or scheduled checks.

## Source and reuse evidence

Reviewed November 11, 2026 (America/New_York). The Open Source Initiative (OSI)
page identifies the definition as version 1.9 and dates that text March 22,
2007. The page's separate last-modified date is February 16, 2024. Treat page
timestamps as metadata and compare the criteria themselves for wording
changes. OSI credits the Debian Free Software Guidelines as the source from
which the definition was derived. [Canonical OSI definition](https://opensource.org/osd)

The live page footer applies CC BY 4.0 to website content authored by OSI and
distinguishes the third-party license texts it hosts. If a future mirror is
justified, verify the material in scope, credit OSI and the upstream source,
link the applicable license, and identify formatting changes.
[OSI reuse FAQ](https://opensource.org/faq/#reuse-osi-materials) ·
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## Manual comparison experiment

1. Fetch the [publisher's WordPress page representation](https://opensource.org/wp-json/wp/v2/pages/317?_fields=id,link,content).
   Verify page ID `317`, its canonical link, and that `content.protected` is
   false. Parse `content.rendered` as an HTML fragment. This field excludes
   site navigation, cookies, and footer chrome.
2. Extract the introduction and ten numbered criteria in order, ending at
   the article divider. Require the observed section IDs in order and a
   heading with at least one paragraph per criterion. Decode HTML entities,
   ignore allowed inline formatting, collapse whitespace, and retain ordered
   heading and paragraph boundaries. Unexpected structure goes to manual
   inspection before any digest is recorded.
3. Compare compact UTF-8 JSON arrays of the heading and paragraph texts by
   SHA-256. Two separate fetches produced
   `9d38c320f020b2ca0ceb5e5f2918d706223cb45e52cf404684ecc25e9abb06a3`.
   The digest records this experiment. A changed digest should prompt a human
   to inspect the upstream wording and open a review PR if it affects local
   documentation.

| Synthetic case | Observed result |
| --- | --- |
| `Sample text.` becomes `<em>Sample</em>   text.`, and the note after the divider changes | Same digest, no action |
| `Sample text.` becomes `Revised text.` inside a criterion | Different digest, review the wording |
| Criterion 1 repeats the heading number for criterion 2 | Reject the parse and inspect upstream |

Hygiene maintainers own any update to the presentation guide. Revisit the
link-only approach if a concrete consumer needs a reviewed offline or
versioned copy. [Feasibility issue](https://github.com/egohygiene/hygiene/issues/94)
