source "https://rubygems.org"

gem "metanorma-cli", git: "https://github.com/metanorma/metanorma-cli", branch: "main" # fleet pins for the 1.3-era flavors
# metanorma 2.5.5 needs Metanorma::Core::Flavors; rubygems' metanorma-core 0.2.3 lacks it
gem "metanorma-core", git: "https://github.com/metanorma/metanorma-core", branch: "main"
gem "ffi"

gem "html2doc", git: "https://github.com/metanorma/html2doc", branch: "main"
gem "isodoc-i18n", git: "https://github.com/metanorma/isodoc-i18n", branch: "main"
gem "isodoc", git: "https://github.com/metanorma/isodoc", branch: "main"
gem "metanorma-standoc", git: "https://github.com/metanorma/metanorma-standoc", branch: "fix/sectioned-semantic"
gem "metanorma-document", git: "https://github.com/metanorma/metanorma-document", branch: "main"
gem "metanorma", git: "https://github.com/metanorma/metanorma", branch: "main"
gem "metanorma-iso", git: "https://github.com/metanorma/metanorma-iso", branch: "main"
gem "metanorma-plateau", git: "https://github.com/metanorma/metanorma-plateau", branch: "main"
# utils#55: GcBudget + in-place asciidoctor table cell buffer (asciidoctor 2.0.x
# rebuilds the whole cell buffer per appended line = O(N^2); asciidoctor is
# third-party so the fix is carried in our gem, self-disarming at their fix)
gem "metanorma-utils", git: "https://github.com/metanorma/metanorma-utils", branch: "perf/asciidoctor-table-buffer"
gem "mn-requirements", git: "https://github.com/metanorma/mn-requirements", branch: "main"
gem "debug"
gem "sassc-embedded"

# flavors referenced by the cg3 handbook corpus (citations to JIS/IEC/IEEE/ITU);
# their gemspecs omit the pubid-* runtime deps
gem "metanorma-iec"
gem "metanorma-ieee"
gem "metanorma-itu"
gem "metanorma-jis", git: "https://github.com/metanorma/metanorma-jis", branch: "fix/restore-1-2-numbering" # PR 523: 1.2.1 + pubid unpin

# hyperperformance line: git-main for the whole lutaml family
gem "lutaml-model", github: "lutaml/lutaml-model", branch: "main"
gem "moxml", github: "lutaml/moxml", branch: "fix/detached-parent-link" # 0.5.97 pin lifted (#308 fixed in 0.5.101); #317 branch until release (0.5.102 stale-parent-link crash)
gem "leptris" # 1.9.282.0 pin lifted - the malloc regression was moxml#308 (leptris-ruby#362 misattribution)
gem "ea", github: "lutaml/ea", ref: "a60688f" # bisect: pre-2216da0
gem "xmi", github: "lutaml/xmi", branch: "main"
gem "metanorma-plugin-lutaml", github: "metanorma/metanorma-plugin-lutaml", branch: "main"

# monogems: relaton + pubid at git main (the metanorma gems already depend on
# these names; released rubygems snapshots lag the monogem APIs)
gem "relaton", github: "relaton/relaton", branch: "main"
gem "relaton-cli", github: "relaton/relaton", branch: "main", glob: "gems/relaton-cli/relaton-cli.gemspec"
gem "pubid", github: "pubid/pubid", branch: "main"
# released relaton-render 1.3.0 still pulls the relaton-bib fragment, whose
# Relaton::RequestError redefinition clashes with the relaton monogem
# (superclass mismatch); render main depends on the monogem directly.
# PINNED to a959df8: render main @8b9ef85 (PR #88) dropped
# Relaton::Render::General, which isodoc main subclasses — NameError at boot
gem "relaton-render" # 1.3 line; 1.4.0.pre.alpha.2 blocked by isodoc main s ~> 1.3.0 floor
